from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import datetime


class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    password_hash: str
    creation_date: datetime
    role: str
    confirmation_code: int

class UserRegister(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    password_confirm: str
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        password = self.password
        password_confirm = self.password_confirm
        if password is not None and password_confirm is not None and password != password_confirm:
            raise ValueError('PASSWORDS MUST MATCH')
        elif len(self.user_name) <= 0:
            raise ValueError("Name is Required")
        elif len(self.email) <= 0:
            raise ValueError("Email is Required")
        else:
            return self

class UserUpdateReq(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    current_password: str
    new_password: Optional[str]
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserUpdateReq':
        current_password = self.current_password
        new_password = self.new_password
        if current_password is not None and new_password is not None and current_password == new_password:
            raise ValueError('Invalid password')
        return self

class ConfirmationCode(BaseModel):
    code: int
    @model_validator(mode='after')
    def code_must_be_greater_than_one(self) -> 'ConfirmationCode':
        if self.code <= 1:
            raise ValueError("Code must have four digits.")
        return self.code