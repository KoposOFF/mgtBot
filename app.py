import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from handlers import register

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message','edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
        await message.answer("Привет! Я бот. 😊")

dp.include_router(register.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаление кнопок меню
    #await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await dp.include_router(CommandStart())

asyncio.run(main())