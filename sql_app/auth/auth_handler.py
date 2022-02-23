import time
from typing import Dict

import jwt
from decouple import config

# Secret for algorithm
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# How to return the token
def token_response(token: str):
    return {"access_token": token}


# Tokenizing with JWT
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


# Decoding JWT token
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
