import aiomysql

from models.user import User, UserData

connect = lambda : aiomysql.connect(
    host="localhost",
    user="root",
    db="fastapi",
)

async def fetch_all_users() -> list[User]:
    async with connect() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM user")
            records = await cursor.fetchall()

            users = []

            for record in records:
                user = User(
                    id=record[0],
                    first_name=record[1],
                    last_name=record[2],
                    phone_number=record[3],
                    email=record[4],
                    password=record[5],
                )
                users.append(user)

            return users


async def create_user_in_db(user_data: UserData) -> User:
    async with connect() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO user (first_name, last_name, phone_number, email, password) VALUES (%s, %s, %s, %s, %s)",
                (user_data.first_name, user_data.last_name, user_data.phone_number, user_data.email, user_data.password)
            )
            await connection.commit()

            user_id = cursor.lastrowid

            return User(
                id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone_number=user_data.phone_number,
                email=user_data.email,
                password=user_data.password,
            )


async def update_user_in_db(user_id, user_data: UserData) -> User:
    async with connect() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "UPDATE user SET first_name=%s, last_name=%s, phone_number=%s, email=%s, password=%s WHERE id=%s",
                (user_data.first_name, user_data.last_name, user_data.phone_number, user_data.email, user_data.password, user_id)
            )
            await connection.commit()

            return User(
                id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone_number=user_data.phone_number,
                email=user_data.email,
                password=user_data.password,
            )


async def fetch_user(user_id: int) -> User | None:
    async with connect() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
            record = await cursor.fetchone()

            if record is None:
                return None

            return User(
                id=record[0],
                first_name=record[1],
                last_name=record[2],
                phone_number=record[3],
                email=record[4],
                password=record[5],
            )
