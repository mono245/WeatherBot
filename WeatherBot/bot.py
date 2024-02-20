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

bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def get_json_weather(city_name: str) -> dict | list:
    async with ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather?" +
            f"q={city_name}&appid={getenv('WEATHER_TOKEN')}&units=metric&lang=ru"
        ) as response:
            json_data = await response.json()

            return json_data


@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    content = Text(
        "Привет, ", Bold(message.from_user.full_name), ". Введи название города, чтобы узнать там погоду"
    )

    
    await message.answer(**content.as_kwargs())


@dp.message(F.text)
async def cities_handler(message: types.Message) -> None:
    json_weather = await get_json_weather(message.text)

    if int(json_weather['cod']) > 226:  # bad request
        await message.reply(
            f"Что-то пошло не так, \n<b>{json_weather['cod']}: {json_weather['message']}</b>"
        )
    else:  # ok request
        await message.reply(
            f"<b>{json_weather['main']['temp']:.0f}С°</b>, "
            f"<b>{json_weather['weather'][0]['description']}</b>, "
            f"ветер <b>{json_weather['wind']['speed']}м/с</b>"
        )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
