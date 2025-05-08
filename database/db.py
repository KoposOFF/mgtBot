from typing import Optional, Dict
from datetime import datetime
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
            table_id INTEGER
        )
        """)
        await db.commit()

# Добавление или обновление пользователя
async def add_user(telegram_id: int, name: str, table_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR REPLACE INTO users (telegram_id, name, table_id)
        VALUES (?, ?, ?)
        """, (telegram_id, name, table_id))
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

# Внесение записи об автобусе
async def get_bus(bus_number: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR REPLACE INTO buses (bus_number)
        VALUES (?)
        """, (bus_number, ))
        await db.commit()



async def add_bus_report(bus_id: int, problems: list[str], pluses: list[str], submitted_by: int):
    problems_str = ", ".join(problems)
    pluses_str = ", ".join(pluses)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO bus_reports (bus_id, problems, pluses, datetime, submitted_by)
        VALUES (?, ?, ?, ?, ?)
        """, (bus_id, problems_str, pluses_str, now, submitted_by))
        await db.commit()


# Получение автобуса по номеру
async def get_bus_by_number(bus_number: str):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM buses WHERE bus_number = ?", (bus_number,))
        return await cursor.fetchone()

# Получение всех записей по автобусу
async def get_bus_reports(bus_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
        SELECT * FROM bus_reports WHERE bus_id = ?
        ORDER BY datetime DESC
        """, (bus_id,))
        return await cursor.fetchall()


async def add_bus_record(bus_number: str, problem: str, pluses: str, created_at: str, created_by: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO bus_reports (bus_number, problem, pluses, created_at, created_by)
        VALUES (?, ?, ?, ?, ?)
        """, (bus_number, problem, pluses, created_at, created_by))
        await db.commit()

async def insert_bus_report(bus_number: int, problems: str, pluses: str, submitted_by: int, datetime_str: str):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        # Получаем ID автобуса по номеру
        cursor = await db.execute("SELECT id FROM buses WHERE bus_number = ?", (bus_number,))
        row = await cursor.fetchone()

        if not row:
            return False  # Автобус с таким номером не найден

        bus_id = row["id"]

        # Вставляем отчет
        await db.execute("""
            INSERT INTO bus_reports (bus_id, problems, pluses, datetime, submitted_by)
            VALUES (?, ?, ?, ?, ?)
        """, (bus_id, problems, pluses, datetime_str, submitted_by))

        await db.commit()
        return True


