from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message) -> None:
    content = Text(
        "Привет, ", Bold(message.from_user.full_name), ". Введи название города, чтобы узнать там погоду"
    )
    
    await message.answer(**content.as_kwargs())


@router.message(Command("src"))
async def src(message: Message) -> None:
    await message.reply(
        "Исходный код <a href=\"https://github.com/mono245/WeatherBot\">здесь</a>",
        disable_web_page_preview=True
    )
