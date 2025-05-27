import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config.config import bot, GROUP_CHAT_ID

async def send_newsletter():
    while True:
        try:
            # Create inline keyboard with link
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Перейти к боту", url="https://t.me/mptu_dpo_bot")]
                ]
            )
            
            # Send newsletter message
            await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text="🎓 ЛУЧШИЕ КУРСЫ повышения квалификации, ПЕРЕХОДИ по ССЫЛКЕ",
                reply_markup=keyboard
            )
            
            # Wait for 6 hours before next newsletter
            await asyncio.sleep(6 * 60 * 60)  # 6 hours in seconds
            
        except Exception as e:
            print(f"Error sending newsletter: {e}")
            # Wait for 5 minutes before retrying in case of error
            await asyncio.sleep(5 * 60) 