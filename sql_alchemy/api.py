import json

from fastapi import APIRouter, Depends
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from .db import async_session, fetch_all_users, create_user_in_db, fetch_user, update_user_in_db, delete_user_in_db, \
    fetch_latest_user
from models.user import User, UserData

users_router = APIRouter(prefix="/v2/users")


async def get_db():
    async with async_session() as session:
        yield session


@users_router.get("")
async def get_users(db: AsyncSession = Depends(get_db)) -> list[User]:
    results = await fetch_all_users(db)

    users = []

    for result in results:
        user = User(
            id=result.id,
            first_name=result.first_name,
            last_name=result.last_name,
            phone_number=result.phone_number,
            email=result.email,
            password=result.password,
        )
        users.append(user)

    return users


@users_router.post("", response_model=User)
async def create_user(user_data: UserData, db: AsyncSession = Depends(get_db)):
    user = await create_user_in_db(db, user_data)

    return Response(user.to_pydantic().model_dump_json(), status_code=201)


@users_router.put("/{user_id}")
async def update_user(user_id: int, user_data: UserData, db: AsyncSession = Depends(get_db)):
    user = await fetch_user(db, user_id)

    if not user:
        return Response(status_code=404)

    await update_user_in_db(db, user, user_data.dict())

    return user


@users_router.patch("/{user_id}")
async def partial_update_user(user_id: int, user_data: dict, db: AsyncSession = Depends(get_db)):
    user = await fetch_user(db, user_id)

    if not user:
        return Response(status_code=404)

    await update_user_in_db(db, user, user_data)

    return user


@users_router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await fetch_user(db, user_id)

    if not user:
        return Response(status_code=404)

    await delete_user_in_db(db, user)

    return Response(status_code=204)


@users_router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await fetch_user(db, user_id)

    if not user:
        return Response(json.dumps({"error": "Not Found"}), status_code=404)

    return user


@users_router.get("/latest")
async def get_latest_user(db: AsyncSession = Depends(get_db)):
    user = await fetch_latest_user(db)

    if not user:
        return Response(status_code=404, content={"error": "User not Found"})

    return user.to_pydantic()
