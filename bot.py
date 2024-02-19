import logging
import asyncio
from os import getenv
from dotenv import load_dotenv

from aiohttp import ClientSession

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.formatting import Bold, Italic, Text

load_dotenv()
logging.basicConfig(level=logging.INFO)  # enable logging

_was_started = False
bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def get_json_weather(city_name: str) -> dict:
    async with ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather?" +
            f"q={city_name}&appid={getenv('WEATHER_TOKEN')}&units=metric&lang=ru"
        ) as response:
            json_data = await response.json()

            return json_data


@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    global _was_started
    full_name = message.from_user.full_name

    default_content = Text(
        "Привет, ", Bold(full_name), ". Введи название города, чтобы узнать там погоду"
    )

    soon_content = Text(
        "Кажется, мы уже виделись, ", Bold(Italic(full_name))
    )

    if not _was_started:
        await message.answer(**default_content.as_kwargs())
    else:
        await message.answer(**soon_content.as_kwargs())

    _was_started = True


@dp.message(F.text)
async def cities_handler(message: types.Message) -> None:
    json_weather = await get_json_weather(message.text)

    if int(json_weather['cod']) > 226:  # bad request
        await message.reply(
            f"Что-то пошло не так, <b>{json_weather['cod']}: {json_weather['message']}</b>",
            parse_mode="HTML"
        )
    else:  # ok request
        await message.reply(
            f"<b>{json_weather['main']['temp']:.0f}С°</b>, "
            f"<b>{json_weather['weather'][0]['description']}</b>, "
            f"ветер <b>{json_weather['wind']['speed']}м/с</b>",
            parse_mode="HTML"
        )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
