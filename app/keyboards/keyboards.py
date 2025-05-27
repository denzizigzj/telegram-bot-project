from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_main_menu_keyboard(is_active: bool):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="📚 Каталог"))
    keyboard.add(KeyboardButton(text="ℹ️ О боте"))
    if is_active:
        keyboard.add(KeyboardButton(text="🛑 Стоп"))
    else:
        keyboard.add(KeyboardButton(text="▶️ Старт"))
    keyboard.adjust(2, 1)
    return keyboard.as_markup(resize_keyboard=True)

def get_categories_keyboard(categories, page, total_pages):
    builder = InlineKeyboardBuilder()

    for category in categories:
        button_text = f"📚 {category.title}"
        callback_data = f"select_category:{category.id}"
        builder.button(text=button_text, callback_data=callback_data)

    builder.adjust(1)

    navigation_buttons = []
    if page > 1:
        prev_callback = f"navigate_categories:{page - 1}"
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=prev_callback))
    if page < total_pages:
        next_callback = f"navigate_categories:{page + 1}"
        navigation_buttons.append(InlineKeyboardButton(text="Следующая ➡️", callback_data=next_callback))

    if navigation_buttons:
        builder.row(*navigation_buttons)

    return builder.as_markup()

def get_courses_keyboard(courses, category_id, page, total_pages):
    builder = InlineKeyboardBuilder()

    for course in courses:
        button_text = f"🎓 {course.title}"
        callback_data = f"view_course:{category_id}:{course.id}"
        builder.button(text=button_text, callback_data=callback_data)

    builder.adjust(1)

    navigation_buttons = []
    if page > 1:
        prev_callback = f"navigate_courses:{category_id}:{page - 1}"
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=prev_callback))
    if page < total_pages:
        next_callback = f"navigate_courses:{category_id}:{page + 1}"
        navigation_buttons.append(InlineKeyboardButton(text="Следующая ➡️", callback_data=next_callback))

    back_callback = "back_to_categories"
    navigation_buttons.append(InlineKeyboardButton(text="🔙 Назад к категориям", callback_data=back_callback))

    if navigation_buttons:
        builder.row(*navigation_buttons)

    return builder.as_markup() 