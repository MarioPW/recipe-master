from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .schemas import UserUpdateReq, UserRegister, ResetPasswordReq
from src.db.models import User, UserRole, ResetPasswordToken
from .repository import UserRepository
from pydantic import EmailStr
from src.db.database import session
import uuid
from datetime import datetime, timedelta
from src.utils.email_handler import EmailHandler
from src.utils.password_hash import get_password_hash, verify_password
from src.utils.jwt_handler import create_access_token

class UserService(UserRepository):

    def __init__(self):
        self.user_repository = UserRepository(session)

    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def get_user_by_confirmation_code(self, code):
        return self.user_repository.get_user_by_confirmation_code(code)

    def confirm_user(self, unconfirmed_user: User):      
        try:      
            confirmed_user = {
                "role": UserRole.user,
                "confirmation_code": 1
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Something went wrong confirming submition in service: {e}")
        return self.user_repository.update_user(unconfirmed_user.user_id, confirmed_user)
    
    def create_register_submition(self, data: UserRegister):                
        email_handler = EmailHandler(data.email)
        email_handler.send_verification_email()
        try:
            user = User( 
                user_id = str(uuid.uuid4()),
                name = data.user_name,
                email = data.email,
                role = UserRole.unconfirmed,
                password_hash = get_password_hash(data.password),
                confirmation_code = email_handler.get_verification_code()
                )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating register submition in service: {e}")
        success = self.user_repository.create_user(user)
        if success:
            return JSONResponse(status_code=200, content=f"Verification email sent to {data.email}")
        
    def login(self, user_data):          
        user_db = self.user_repository.get_user_by_email(user_data.username)
        if not user_db:
            raise HTTPException(status_code=400, detail=f"User {user_data.username} not found")
        verified_password = verify_password(user_data.password, user_db.password_hash)
        if not verified_password:
            raise HTTPException(status_code=400, detail="Incorrect User or Password")
        try:    
            user_data_token = {
                "user_id": user_db.user_id,
                "name": user_db.name,
                "role": user_db.role
                }
            return {
                    "access_token": create_access_token(user_data_token),
                    "token_type": "bearer"
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating user token: {e}")
        
    def forgot_password(self, email):
        user_exist = self.user_repository.get_user_by_email(email)
        if not user_exist:
            raise HTTPException(status_code=404, detail=f'User "{email}" not found')
        
        update_attempts_to_change_password = {"attempts_to_change_password": user_exist.attempts_to_change_password + 1}
        self.user_repository.update_user(user_exist.user_id, update_attempts_to_change_password)

        email_handler = EmailHandler(email)
        email_handler.send_change_password_email()
        reset_password_code = email_handler.get_reset_password_code()

        try: 
            reset_password_token = ResetPasswordToken(
                user_id = user_exist.user_id,
                token = reset_password_code,
                created_at = datetime.now(),
                expires_at = datetime.now() + timedelta(minutes=10),
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Couldn't create reset_passwor_token in /users/service: {e}")

        self.user_repository.save_reset_password_token(reset_password_token)
        return JSONResponse(status_code=200, content={"message": f'Email to "{email}" sent successfully.'})
        
    def reset_password(self, reset_password_req: ResetPasswordReq):
        token_exist: ResetPasswordToken = self.user_repository.get_reset_password_token(reset_password_req.token)
        if not token_exist:
            raise HTTPException(status_code=404, detail=f'Ghange password token for "{reset_password_req.email}" not found')
        elif token_exist.expires_at < datetime.now():
            raise HTTPException(status_code=404, detail=f'Token has expired')
        
        password_update = {
            "password_hash": get_password_hash(reset_password_req.password1)
        }
        return self.user_repository.update_user(token_exist.user_id, password_update)           

    def get_user_by_id(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, user_email: EmailStr): 
        return self.user_repository.get_user_by_email(user_email)

    def update_user(self, user_id: str, user_updates: UserUpdateReq):
        user: User = self.user_repository.get_user_by_id(user_id)
        verified_password = verify_password(user_updates.current_password, user.password_hash)
        if not verified_password:
            raise HTTPException(status_code=400, detail=f"Incorrect password")
        try:
            updated_user = {
                "name": user_updates.name,
                "email": user_updates.email,
                "password_hash": get_password_hash(user_updates.new_password)
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Something went wrong updating user in service: {e}")
        return self.user_repository.update_user(user.user_id, updated_user)           

    def delete_user(self, user_id: str):
        return self.user_repository.delete_user(user_id)