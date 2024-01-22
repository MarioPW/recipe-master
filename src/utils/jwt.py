from passlib.context import  CryptContext
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv()

jwt_key = getenv("JWT_SECRET")
algorithm = getenv("ALGORITHM")
token_expire = int(getenv("ACCESS_TOKEN_EXPIRE_SEC"))

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 
# save token to oauth2_scheme
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="user/signin")

# create Token
def create_access_token(data: dict):   
    expiration = datetime.utcnow() + timedelta(minutes=token_expire)
    expiration_str = expiration.isoformat()
    data["expire"] = expiration_str   
    token = jwt.encode(claims=data, key=jwt_key, algorithm=algorithm)
    return token
    
def verify_token(token) -> dict:
    try:
        payload = jwt.decode(token,key=jwt_key)
        return payload
    except JWTError as ex:
        print(str(ex))
        raise HTTPException(status_code=401, detail="Invalid Token", headers={"WWW-Authenticate":"Bearer"})

# Just to try out
if __name__ == "__main__":
    user = {
        "name": "Guido",
        "role": "5cfbe49a-c985-4d11-94f7-7a7240f1ad35",
        "expire": "2023-09-14T21:36:28.984719"
        }
    token = create_access_token(user)
    decoded = verify_token(token)
    print(token)