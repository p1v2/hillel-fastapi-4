# db.py
import aiosqlite
from models.user import User, UserData
import os

DATABASE_URL = os.path.join(os.getcwd(), "test.db")

async def connect():
    return await aiosqlite.connect("test.db")


async def fetch_all_users() -> list[User]:
    async with aiosqlite.connect(DATABASE_URL) as connection:
        cursor = await connection.execute("SELECT * FROM user")
        records = await cursor.fetchall()
        users = [User(
            id=record[0],
            first_name=record[1],
            last_name=record[2],
            phone_number=record[3],
            email=record[4],
            password=record[5],
        ) for record in records]
        return users


async def create_user_in_db(user_data: UserData) -> User:
    async with aiosqlite.connect(DATABASE_URL) as connection:
        cursor = await connection.execute(
            "INSERT INTO user (first_name, last_name, phone_number, email, password) VALUES (?, ?, ?, ?, ?)",
            (user_data.first_name, user_data.last_name, user_data.phone_number, user_data.email, user_data.password)
        )
        await connection.commit()
        user_id = cursor.lastrowid
        return User(id=user_id, **user_data.dict())


async def update_user_in_db(user_id: int, user_data: UserData) -> User:
    async with aiosqlite.connect(DATABASE_URL) as connection:
        await connection.execute(
            "UPDATE user SET first_name=?, last_name=?, phone_number=?, email=?, password=? WHERE id=?",
            (user_data.first_name, user_data.last_name, user_data.phone_number, user_data.email, user_data.password, user_id)
        )
        await connection.commit()
        return User(id=user_id, **user_data.dict())


async def fetch_user(user_id: int) -> User | None:
    async with aiosqlite.connect(DATABASE_URL) as connection:
        cursor = await connection.execute("SELECT * FROM user WHERE id=?", (user_id,))
        record = await cursor.fetchone()
        if record is None:
            return None
        return User(id=record[0], first_name=record[1], last_name=record[2], phone_number=record[3], email=record[4], password=record[5])


async def delete_user_in_db(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_URL) as connection:
        cursor = await connection.execute("DELETE FROM user WHERE id=?", (user_id,))
        await connection.commit()
        return cursor.rowcount > 0