# database/db.py
import sqlite3

# Подключение к БД (создаётся, если её нет)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    employee_id INTEGER
)
""")
conn.commit()

# Функция для добавления нового пользователя
def add_user(telegram_id: int, name: str, employee_id: int):
    cursor.execute("INSERT OR REPLACE INTO users (telegram_id, name, employee_id) VALUES (?, ?, ?)",
                   (telegram_id, name, employee_id))
    conn.commit()

# Функция для получения пользователя по Telegram ID
def get_user(telegram_id: int):
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()
