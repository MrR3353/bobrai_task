import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from settings import TG_TOKEN, OWM_API_KEY
from owm_api import get_weather, get_weather_icon_url
from db import log_request, get_cached_log

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command(commands=['start']))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я тестовый бот для компании BobrAi. Чтобы узнать погоду, введи команду /weather <город>.")


@dp.message(Command(commands=['weather']))
async def weather_handler(message: Message):
    city = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not city:
        await message.answer("Пожалуйста, укажите город. Например, /weather Москва")
        return

    try:
        cached_log = get_cached_log(message.text.lower())
        if cached_log is not None:
            response = cached_log.response
            icon_url = cached_log.icon_url
        else:
            weather_data = get_weather(city, OWM_API_KEY)
            icon_url = get_weather_icon_url(weather_data['icon'])
            response = (f"Погода в {city}:\n"
                        f"Температура: {weather_data['temp']}°C\n"
                        f"Ощущается как: {weather_data['feels_like']}°C\n"
                        f"Описание: {weather_data['description']}\n"
                        f"Влажность: {weather_data['humidity']}%\n"
                        f"Скорость ветра: {weather_data['wind_speed']} м/с")

        if icon_url:
            await bot.send_photo(chat_id=message.chat.id, photo=icon_url)
        await message.answer(response)

    except Exception as e:
        print(e)
        icon_url = None
        response = str(e) if str(e) == "Такого города не существует" else "Произошла ошибка. Попробуйте еще раз позже"
        await message.answer(response)

    try:
        log_request(message.from_user.id, message.text.lower(), response, icon_url)
    except Exception as e:
        print(e)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
