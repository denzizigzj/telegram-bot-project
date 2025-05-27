from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from emoji import emojize

from app.config.config import bot, bot_active
from app.keyboards.keyboards import get_main_menu_keyboard, get_categories_keyboard, get_courses_keyboard
from app.database.operations import (
    get_categories, get_total_categories,
    get_courses, get_total_courses,
    get_course
)

# Command handlers
async def cmd_start(message: Message):
    bot_active[message.chat.id] = True
    keyboard = get_main_menu_keyboard(is_active=True)
    photo = FSInputFile("photo/mospy.jpg")
    await message.answer_photo(photo, caption="Привет! Я помогу тебе найти интересующие курсы.",
                             reply_markup=keyboard)

async def cmd_stop(message: Message):
    bot_active[message.chat.id] = False
    keyboard = get_main_menu_keyboard(is_active=False)
    await message.answer("Бот остановлен. Чтобы начать снова, нажмите '▶️ Старт'.", reply_markup=keyboard)

# Message handlers
async def handle_main_menu(message: Message):
    if not bot_active.get(message.chat.id, True):
        await message.answer("Бот остановлен. Чтобы начать снова, нажмите '▶️ Старт'.",
                           reply_markup=get_main_menu_keyboard(is_active=False))
        return
    
    if message.text == "📚 Каталог":
        await send_categories(message.chat.id, page=1)
    elif message.text == "ℹ️ О боте":
        await message.answer(
            "Этот бот предназначен для просмотра курсов ДПО Московского политеха. "
            "Вы можете просматривать категории и курсы, а также получать информацию о них.",
            reply_markup=get_main_menu_keyboard(is_active=True)
        )
    elif message.text == "🛑 Стоп":
        await cmd_stop(message)
    elif message.text == "▶️ Старт":
        await cmd_start(message)
    else:
        await message.answer(
            "Пожалуйста, выберите действие с помощью клавиатуры ниже.",
            reply_markup=get_main_menu_keyboard(is_active=bot_active.get(message.chat.id, True))
        )

# Helper functions
async def send_categories(chat_id: int, page: int):
    categories = await get_categories(page)
    total_categories = await get_total_categories()
    total_pages = (total_categories + 5 - 1) // 5

    keyboard = get_categories_keyboard(categories, page, total_pages)
    await bot.send_message(chat_id, emojize("🏷️ <b>Выберите категорию:</b>"),
                          reply_markup=keyboard, parse_mode='HTML')

async def send_courses(chat_id: int, category_id: int, page: int):
    courses = await get_courses(category_id, page)
    total_courses = await get_total_courses(category_id)
    total_pages = (total_courses + 5 - 1) // 5

    keyboard = get_courses_keyboard(courses, category_id, page, total_pages)
    await bot.send_message(chat_id, emojize("📋 <b>Выберите курс:</b>"),
                          reply_markup=keyboard, parse_mode='HTML')

async def send_course_details(chat_id: int, course_id: int, category_id: int):
    course = await get_course(course_id)
    if course:
        message_text = emojize(f"🎓 <b>{course.title}</b>\n\n")
        message_text += f"📖 Тип: {course.type}\n"
        if course.durations:
            message_text += f"⏳ Длительность: {course.durations}\n"
        if course.format:
            message_text += f"📝 Формат: {course.format}\n"
        if course.cost:
            message_text += f"💰 Стоимость: {course.cost}\n"

        keyboard = get_courses_keyboard([], category_id, 1, 1)
        await bot.send_message(chat_id, message_text, reply_markup=keyboard, parse_mode='HTML')

# Callback handler
async def callback_query_handler(callback_query: CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data.startswith("select_category:"):
        category_id = int(data.split(":")[1])
        await send_courses(chat_id, category_id, page=1)
    
    elif data.startswith("view_course:"):
        _, category_id, course_id = data.split(":")
        await send_course_details(chat_id, int(course_id), int(category_id))
    
    elif data.startswith("navigate_categories:"):
        page = int(data.split(":")[1])
        await send_categories(chat_id, page)
    
    elif data.startswith("navigate_courses:"):
        _, category_id, page = data.split(":")
        await send_courses(chat_id, int(category_id), int(page))
    
    elif data == "back_to_categories":
        await send_categories(chat_id, page=1)
    
    await callback_query.answer() 