import asyncio
import logging
from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command

from app.config.config import bot
from app.handlers.handlers import (
    cmd_start, cmd_stop,
    handle_main_menu,
    callback_query_handler
)
from app.utils.newsletter import send_newsletter

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize dispatcher
dp = Dispatcher()

# Register handlers
dp.message.register(cmd_start, CommandStart())
dp.message.register(cmd_stop, Command("stop"))
dp.message.register(cmd_start, F.text == "▶️ Старт")
dp.message.register(cmd_stop, F.text == "🛑 Стоп")
dp.message.register(handle_main_menu, F.text)
dp.callback_query.register(callback_query_handler)

async def main():
    # Start newsletter task
    newsletter_task = asyncio.create_task(send_newsletter())
    
    try:
        # Start polling
        await dp.start_polling(bot)
    finally:
        # Cancel newsletter task when bot stops
        newsletter_task.cancel()
        try:
            await newsletter_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped gracefully") 