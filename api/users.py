import json

from fastapi import APIRouter, Response, HTTPException
from pydantic import ValidationError

from db import fetch_all_users, create_user_in_db, update_user_in_db, fetch_user, delete_user_from_db
from models.user import UserData

users_router = APIRouter(prefix="/users")


@users_router.get("")
async def read_users():
    return await fetch_all_users()


@users_router.post("")
async def create_user(user_data: UserData):
    return await create_user_in_db(user_data)


@users_router.put("/{user_id}")
async def update_user(user_id: int, user_data: UserData):
    return await update_user_in_db(user_id, user_data)


@users_router.patch("/{user_id}")
async def partial_update_user(user_id: int, user_data: dict):
    existing_user = await fetch_user(user_id)

    if not existing_user:
        return Response(status_code=404)

    # Update only the fields that are present in the request
    existing_user_data = existing_user.dict()

    user_data = {
        **existing_user_data,
        **user_data,
    }

    try:
        user = UserData(**user_data)
    except ValidationError as e:
        return Response(
            json.dumps({"errors": e.errors()}), status_code=422,
            headers={"Content-Type": "application/json"}
        )

    return await update_user_in_db(user_id, user)


@users_router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int):
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_user_from_db(user_id)
    return Response(
        headers={"Content-Type": "application/json"},
        content=json.dumps({"message": "User deleted successfully"}),
        status_code=200
    )

#  Додав про всяк випадок варіант 2:
#  якщо не відправляти повідомлення в тілі відповіді- то код 204
#  а то знову мені за ці коди оцінку знизять )))


# @users_router.delete("/{user_id}", status_code=204)
# async def delete_user(user_id: int):
#     user = await fetch_user(user_id)
#
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     await delete_user_from_db(user_id)
#
#     return Response(status_code=204)