from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

from models.user import User as PydanticUser, UserData

DATABASE_URL = "mysql+aiomysql://root:@localhost/fastapi"

# Async Engine from MySQL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async database session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Create database
database = Database(DATABASE_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    password = Column(String)

    def to_pydantic(self):
        return PydanticUser(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            email=self.email,
            password=self.password,
        )


async def fetch_all_users(db: AsyncSession):
    result = await db.execute(select(User))

    return result.scalars().all()


async def create_user_in_db(db: AsyncSession, user_data: UserData):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        email=user_data.email,
        password=user_data.password,
    )

    db.add(user)
    await db.commit()

    return user


async def fetch_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))

    return result.scalars().first()


async def update_user_in_db(db: AsyncSession, user: User, user_data: dict):
    for field, value in user_data.items():
        setattr(user, field, value)

    await db.commit()

    return user


async def delete_user_in_db(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit()
