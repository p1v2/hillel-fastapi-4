from pydantic import BaseModel, Field, EmailStr


class UserData(BaseModel):
    first_name: str
    last_name: str
    # Ukrainian number
    phone_number: str = Field(pattern=r'^(\+38)?0\d{9}$')
    email: EmailStr = Field()
    password: str


class User(UserData):
    id: int
