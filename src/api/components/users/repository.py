from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import  Dict
from pydantic import EmailStr
from src.db.models import User, UserRole

class UserRepository:
    def __init__(self, session):
        self.sess = session
    
    def get_all_users(self):
        try:
            all_users: [] = self.sess.query(User).all()
            if len(all_users) <= 0:
                return JSONResponse(content={"message": "No users found"}, status_code=404)
            return all_users
        except Exception as e:
            raise HTTPException(status_code=404, deltail=f"Error getting all users: {e}")
    
    def get_user_by_confirmation_code(self, code):
        user = self.sess.query(User).filter(User.confirmation_code == code).first()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with code {code} not found")
        try:
            return user
        except Exception as e:
            self.sess.rollback()
            raise HTTPException(status_code=404, deltail=f"User with code {code} not found in repository: {e}")
        
    def create_user(self, signup:User):
        try:
            self.sess.add(signup)
            self.sess.commit()
            return signup
        except Exception as e:
            self.sess.rollback()
            raise HTTPException(status_code=500, deltail=f"Error creating user in repository: {e}")
        
    def get_user_by_id(self,user_id:str):
        try:
            return self.sess.query(User).filter(User.user_id==user_id).first()
        except Exception as e:
            raise HTTPException(status_code=404, deltail=f"User not found: {e}")

    def get_user_by_email(self, email:EmailStr):
        try:
            return self.sess.query(User).filter(User.email==email).first()
        except Exception as e:
            raise HTTPException(status_code=404, deltail=f"User with email {email} not found: {e}")

    def update_user(self, id: str, data: Dict):
        try:
            self.sess.query(User).filter(User.user_id == id).update(data)
            self.sess.commit()
            updated_user: User = self.get_user_by_id(id) 
            return JSONResponse (status_code=200, content={"message": f"User {updated_user.name} updated successfully."})
        except Exception as e:
            raise HTTPException(status_code=500, deltail=f"Error updating user: {e}")

    # SOFT DELETION
    def delete_user(self, id:str):
        try:
            user: User = self.get_user_by_id(id)            
            if not user:
                raise HTTPException(status_code=404, deltail=f"User not found: {e}")                  
            user.role = UserRole.deleted
            self.sess.commit()             
            return JSONResponse (status_code=200, content={"message": f"User {user.name} deleted successfully."})

        except Exception as e:
            raise HTTPException(status_code=500, deltail=f"Error deleting user: {e}")