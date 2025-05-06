from typing import Optional, Dict
import aiosqlite

DB_NAME = "users.db"

# Инициализация базы данных (создание таблицы)
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT,
            employee_id INTEGER
        )
        """)
        await db.commit()

# Добавление или обновление пользователя
async def add_user(telegram_id: int, name: str, employee_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR REPLACE INTO users (telegram_id, name, employee_id)
        VALUES (?, ?, ?)
        """, (telegram_id, name, employee_id))
        await db.commit()

# Получение пользователя в виде строки
async def get_user(telegram_id: int) -> Optional[aiosqlite.Row]:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return await cursor.fetchone()

# Получение пользователя в виде словаря
async def get_user_dict(telegram_id: int) -> Optional[Dict]:
    row = await get_user(telegram_id)
    if row:
        return dict(row)
    return None
