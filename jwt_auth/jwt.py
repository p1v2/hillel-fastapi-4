from datetime import timedelta, datetime

import jwt

ALGORITHM = "RS256"



def create_access_token(data: dict, expires_delta: timedelta) -> str:
    private_key = open("private_key.pem").read()

    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    public_key = open("public_key.pem").read()

    try:
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
