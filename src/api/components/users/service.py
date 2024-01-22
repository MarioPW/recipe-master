from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .schemas import UserUpdateReq, UserRegister
from src.db.models import User, UserRole
from .repository import UserRepository
from pydantic import EmailStr
from src.db.database import session
import uuid
from src.utils.verify_email import SendEmailVerify
from src.utils.password_hash import get_password_hash, verify_password
from src.utils.jwt import create_access_token, verify_token

class UserService(UserRepository):

    def __init__(self):
        self.user_repository = UserRepository(session)

    async def get_all_users(self):
        try:
            return self.user_repository.get_all_users()
        except:
            raise HTTPException(status_code=500, detail=f"Something went wrong getting all users in service")
    
    async def create_user(self, code):
        try:
            exist_user = self.user_repository.get_user_by_confirmation_code(code)
            if not exist_user:
                content = {"message": "Incorrect code."}
                return content
            confirmed_user = {
                "role": UserRole.user,
                "confirmation_code": 1
                }
            return self.user_repository.update_user(exist_user.user_id, confirmed_user)
        except Exception as error:
            return f"Something went wrong creating register submition in service: {error}"

    async def create_register_submition(self, data: UserRegister):

        email_exists = self.user_repository.get_user_by_email(data.email)
   
        if email_exists != None:
            return f"User with email {data.email} already exists."
        try:          
            email = SendEmailVerify(data.email)
            verify_code = email.create_verify_code()
            email.sendVerify(verify_code)
        except Exception:
            return Exception()          
        hash_password = get_password_hash(data.password)
        uu_id = str(uuid.uuid4())
        user = User( 
                user_id = uu_id,
                name = data.user_name,
                email = data.email,
                password_hash = hash_password,
                confirmation_code = verify_code
                )
        try:
            unconfirmed_user = self.user_repository.create_register_submition(user)
            if unconfirmed_user == None:
                raise HTTPException(status_code=409, detail="Error")
            return f"We've sended a verification Email to {data.email}"
            
        except Exception as error:
                return f"Something went wrong in service: {error}"

    async def  login(self, data):
        try:           
            user_db = self.user_repository.get_user_by_email(data.username)
            if not user_db:
                raise HTTPException(status_code=400, detail=f"User {data.username} not found")
            verified_password = verify_password(data.password, user_db.password_hash)
            if not verified_password:
                raise HTTPException(status_code=400, detail="Incorrect User or Password")
            data = {
                "user_id": user_db.user_id,
                "name": user_db.name,
                "role": user_db.role
                }
            return {
                "access_token": create_access_token(data),
                "token_type": "bearer"
                }
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Something went wrong in service: {error}")

    async def user_main_page(self, token):
        try:
            decoded_user = verify_token(token)
            if not decoded_user:
                raise HTTPException(status_code=401, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
            user_db = self.user_repository.get_user_by_name(decoded_user["name"])
            if not user_db:
                raise HTTPException(status_code=404, detail="User not Found")
            logued_user = {
                "name": user_db.name,
                "role": user_db.role,
                "expire": decoded_user['expire']
            }
            return logued_user
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Something went wrong in service: {error}")

    async def get_user_by_id(self, user_id: str):
        try:
            user =  self.user_repository.get_user_by_id(user_id)
            if not user:                
                return f"Couldn't find user {user_id}"
            return user
        except Exception as error:
            return f"Something went wrong: {error}"
    
    async def get_user_by_email(self, user_email: EmailStr):
        try:
            user = self.user_repository.get_user_by_email(user_email)
            if not user:           
                return f"Couldn't find user {user_email}"
            return user
        except Exception as error:
            return f"Something went wrong getting user by email in service: {error}"

    async def update_user(self, user_id: str, user_updates: UserUpdateReq):
        try:
            user: User = self.user_repository.get_user_by_id(user_id)
            verified_password = verify_password(user_updates.current_password, user.password_hash)
            if not verified_password:
                return f"Incorrect password"
            updated_user = {
                "name": user_updates.name,
                "email": user_updates.email,
                "password_hash": get_password_hash(user_updates.new_password)
                }
            return self.user_repository.update_user(user.user_id, updated_user)              
        except Exception as error:
            return f"Something went wrong in service...{error}"

    async def delete_user(self, user_id: str):
        try:
            return self.user_repository.delete_user(user_id)
        except ValueError as error:
            return f"Something went wrong in service... {error}"
