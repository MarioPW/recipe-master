from src.utils.jwt import verify_token
from src.api.components.users.repository import UserRepository
from src.db.database import session

user_repository = UserRepository(session)

def roles_required(allowed_roles, token=None, code=None):
    user = None       
    if token:
        decoded_user = verify_token(token)
        if decoded_user:
            user = user_repository.get_user_by_name(decoded_user["name"])
    elif code:
        user = user_repository.get_user_by_code(code)     
    return user is not None and user.role in allowed_roles