from dotenv import load_dotenv
from os import getenv

from aiohttp import ClientSession


async def get_json_weather(city_name: str) -> dict | list:
    load_dotenv(dotenv_path=r"..\.env")

    url = "https://api.openweathermap.org/data/2.5/weather?" +\
        f"q={city_name}&appid={getenv('WEATHER_TOKEN')}&units=metric&lang=ru"

    async with ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()

            return json_data
