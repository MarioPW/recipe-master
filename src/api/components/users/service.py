from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .schemas import UserUpdateReq, UserRegister
from src.db.models import User, UserRole
from .repository import UserRepository
from pydantic import EmailStr
from src.db.database import session
import uuid
from src.utils.email_handler import EmailHandler
from src.utils.password_hash import get_password_hash, verify_password
from src.utils.jwt_handler import create_access_token

class UserService(UserRepository):

    def __init__(self):
        self.user_repository = UserRepository(session)

    def get_all_users(self):
        try:
            return self.user_repository.get_all_users()
        except:
            raise HTTPException(status_code=500, detail=f"Something went wrong getting all users in service")
    
    def confirm_user(self, code):
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

    def create_register_submition(self, data: UserRegister):
        email_exists = self.user_repository.get_user_by_email(data.email)
        if email_exists != None:
            return f"User with email {data.email} already exists."
        try:          
            email_handler = EmailHandler(data.email)
            email_handler.send_verification_email()
        except Exception as e:
            return f"Error sending email: {e}"
        user = User( 
                user_id = str(uuid.uuid4()),
                name = data.user_name,
                email = data.email,
                password_hash = get_password_hash(data.password),
                confirmation_code = email_handler.get_verification_code()
                )
        try:
            unconfirmed_user = self.user_repository.create_user(user)
            if unconfirmed_user == None:
                raise HTTPException(status_code=409, detail="Error")
            return f"We've sended a verification Email to {data.email}"
            
        except Exception as e:
                return f"Something went wrong in service: {e}"

    def login(self, user_data):
        try:           
            user_db = self.user_repository.get_user_by_email(user_data.username)
            if not user_db:
                raise HTTPException(status_code=400, detail=f"User {user_data.username} not found")
            verified_password = verify_password(user_data.password, user_db.password_hash)
            if not verified_password:
                raise HTTPException(status_code=400, detail="Incorrect User or Password")
            user_data_token = {
                "user_id": user_db.user_id,
                "name": user_db.name,
                "role": user_db.role
            }
            return {
                "access_token": create_access_token(user_data_token),
                "token_type": "bearer"
                }
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong in service: {e}")
        
    def forgot_password(self, email):
        user = self.user_repository.get_user_by_email(email)
        if type(user) != User:
            raise HTTPException(status_code=404, detail={"message": f'User "{email}" not found.'})
        email_handler = EmailHandler(user.email)
        try:
            email_handler.send_change_password_email()
            return JSONResponse(status_code=200, content={"message": f'Email to {email} sended successfully.'})
        except Exception as e:
            raise HTTPException(status_code=503, content={"message": f'Service Unavailable: {e}'})

    def get_user_by_id(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, user_email: EmailStr):
        try:
            user = self.user_repository.get_user_by_email(user_email)
            if not user:           
                return f"Couldn't find user {user_email}"
            return user
        except Exception as error:
            return f"Something went wrong getting user by email in service: {error}"

    def update_user(self, user_id: str, user_updates: UserUpdateReq):
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

    def delete_user(self, user_id: str):
        return self.user_repository.delete_user(user_id)
    
