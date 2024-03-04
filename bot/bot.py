import asyncio
import logging
from os import getenv
from dotenv import load_dotenv

from .handlers import basic_cmd, cities

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s |%(levelname)s| - %(name)s: %(message)s"
    )
    load_dotenv()

    bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(basic_cmd.router, cities.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
