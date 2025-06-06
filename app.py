import asyncio
import os
# import logging

from aiogram import Bot, Dispatcher, types
from handlers import register, bus_list, bus_check
from database.db import init_db 

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message','edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(register.router)
dp.include_router(bus_list.router)
dp.include_router(bus_check.router)



async def main():
    await init_db() # инициализация таблицы
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаление кнопок меню
    #await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    # )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен нажатием Ctrl+C")