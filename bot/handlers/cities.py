from aiogram import Router, F
from aiogram.types import Message

from ..utils import get_json_weather

router = Router()


@router.message(F.text)
async def cities_handler(message: Message) -> None:
    json_weather = await get_json_weather(message.text.strip())
    username = message.from_user.username

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
