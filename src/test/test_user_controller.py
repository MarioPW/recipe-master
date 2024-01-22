from fastapi import HTTPException
import pytest
from datetime import datetime
from src.db.models import UserRole, User
from src.api.components.users.schemas import UserRegister
from src.api.components.users import controller
from src.api.components.users.service import UserService
from src.middleware.role_auth import roles_required

user_service = UserService()

#### MOCKS ####
@pytest.fixture
def user():
    return User(
        user_id = "e0c33d6b-f2f4-4cc2-b907-1bb083c6af7b",
        name = "Guido",
        email = "guido@gmail.com",
        password_hash = "aa9b1d4a-1c4d-4e67-ad2c-dbf36bdf1b8e",
        creation_date = datetime.now,
        role = UserRole.user,
        confirmation_code = 1
    )

@pytest.fixture
def user2():
    return User(
        user_id = "e0c33d6b-f2f4-4cc2-b907-1bb083c6af7",
        name = "Mario",
        email = "mario@gmail.com",
        password_hash = "aa9b1d4a-1c4d-4e67-ad2c-dbf36bdf1b81",
        creation_date = datetime.now,
        role = UserRole.unconfirmed,
        confirmation_code = 1234
    )

@pytest.fixture
def token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZDM0NDZkYTQtMjc4NC00Njc2LTgzNjItNGFkMmFhMTI2OGQwIiwibmFtZSI6Im1hcmlvIiwicm9sZSI6IjVjZmJlNDlhLWM5ODUtNGQxMS05NGY3LTdhNzI0MGYxYWQzNSIsImV4cGlyZSI6IjIwMjQtMDEtMjFUMDU6MDQ6NTkuMzUxNDgwIn0.KevG8dbqqgk0Ub7Nq4GeWu00CDeEBu8o19D4brPPyKw"

@pytest.fixture
def user_register():
    return UserRegister(
        user_name = "Guido",
        email = "guido@gmail.com",
        password = "123",
        password_confirm = "123"
    )

@pytest.fixture
def login_data():
    return {
        "access_token": "token",
        "token_type": "bearer"
        }

#### TESTS #### 
@pytest.mark.asyncio
async def test_get_all_users(mocker, user, user2, token):

    mock_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None
    mock_get_all_users.return_value = [user, user2]

    result = await controller.get_all_users(token)

    assert mock_get_all_users.called_once
    assert mock_service_roles_required.called_once
    assert result == [user, user2]

@pytest.mark.asyncio
async def test_get_all_users_role_fail(mocker, token):
    mock_service_roles_required = mocker.patch('src.middleware.role_auth.roles_required')
    mock_service_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')
    with pytest.raises(HTTPException) as exception:
        await controller.get_all_users(token) 
    assert mock_service_roles_required.called_once
    assert not mock_service_get_all_users.called
    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'

@pytest.mark.asyncio
async def test_get_all_users_fail(mocker, token):
    mock_service_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None    
    mock_service_get_all_users.return_value = None
    with pytest.raises(HTTPException) as exception:
        await controller.get_all_users(token)   
    assert mock_service_get_all_users.called_once
    assert exception.value.status_code == 500
    assert exception.value.detail == "Error getting all users in controller"

@pytest.mark.asyncio
async def test_get_user_by_id(mocker, token, user):
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None    
    mock_service_get_user_by_id.return_value = user
    result = await controller.get_user_by_id("e0c33d6b-f2f4-4cc2-b907-1bb083c6af7b", token)
    assert result == user
    assert mock_service_get_user_by_id.called_once
    assert mock_service_roles_required.called_once

@pytest.mark.asyncio
async def test_get_user_by_id_role_fail(mocker, token):
    mock_service_roles_required = mocker.patch('src.middleware.role_auth.roles_required')
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')
    with pytest.raises(HTTPException) as exception:
        await controller.get_all_users(token) 

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    assert mock_service_roles_required.called_once
    assert not mock_service_get_user_by_id.called

@pytest.mark.asyncio
async def test_get_user_by_id_fail(mocker, token):
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exception:
        await controller.get_user_by_id(token)   
    assert mock_service_get_user_by_id.called_once
    assert exception.value.status_code == 500
    assert exception.value.detail == "Error getting user by id incontroller"

@pytest.mark.asyncio
async def test_get_user_by_email(mocker, token, user):
    mock_get_user_by_email = mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None
    mock_get_user_by_email.return_value = user
    result = await controller.get_user_by_email(token)   
    assert mock_get_user_by_email.called_once
    assert result == user

@pytest.mark.asyncio
async def test_get_user_by_email_role_fail(mocker, token):
    mock_service_roles_required = mocker.patch('src.middleware.role_auth.roles_required')
    mock_service_get_user_by_email = mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    with pytest.raises(HTTPException) as exception:
        await controller.get_all_users(token) 

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    assert mock_service_roles_required.called_once
    assert not mock_service_get_user_by_email.called

@pytest.mark.asyncio
async def test_get_user_by_email_fail(mocker, token):
    mock_service_get_user_by_email =  mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None
    mock_service_get_user_by_email.return_value = None
    with pytest.raises(HTTPException) as exception:
        await controller.get_user_by_email(token)   
    assert mock_service_get_user_by_email.called_once
    assert exception.value.status_code == 500
    assert exception.value.detail == "Error getting user by email incontroller"

@pytest.mark.asyncio
async def test_create_register_submition(mocker, user_register):
    mock_service_create_register_submition = mocker.patch('src.api.components.users.service.UserService.create_register_submition', return_value = "We've sended a verification Email to guido@gmail.com")
    result = await controller.create_register_submition(user_register)
    assert mock_service_create_register_submition.called_once
    assert result == "We've sended a verification Email to guido@gmail.com"

@pytest.mark.asyncio
async def test_create_register_submition_email_exists(mocker, user_register):
    mock_service_create_register_submition = mocker.patch('src.api.components.users.service.UserService.create_register_submition', return_value = "User with email guido@gmail.com already exists.")
    result = await controller.create_register_submition(user_register)
    assert mock_service_create_register_submition.called_once
    assert result == "User with email guido@gmail.com already exists."

@pytest.mark.asyncio
async def test_create_register_submition_fail(mocker, user_register):
    # Mocks
    mocker.patch('src.api.components.users.controller.user_service.create_register_submition', side_effect=Exception)
    with pytest.raises(HTTPException) as exception_info:
        await controller.create_register_submition(user_register)
    assert isinstance(exception_info.value, HTTPException)
    assert exception_info.value.detail == "Opss Couldn't send email to guido@gmail.com in controller: "
    assert exception_info.value.status_code == 422

@pytest.mark.asyncio
async def test_create_user(mocker):
    mocker.patch('src.api.components.users.controller.user_service.create_user', return_value = True)
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None 
    confirmation_code = 1234
    result = await controller.create_user(confirmation_code)
    assert result == True

@pytest.mark.asyncio
async def test_create_user_role_fail(mocker, token):
    mock_service_roles_required = mocker.patch('src.middleware.role_auth.roles_required')
    mock_service_create_user = mocker.patch('src.api.components.users.controller.user_service.create_user')

    with pytest.raises(HTTPException) as exception:
        await controller.get_all_users(token)

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    assert mock_service_roles_required.called_once
    assert not mock_service_create_user.called

@pytest.mark.asyncio
async def test_create_user_fail(mocker):
    mocker.patch('src.api.components.users.controller.user_service.create_user', side_effect=Exception)
    mock_service_roles_required = mocker.patch('src.api.components.users.controller.roles_required')
    mock_service_roles_required.return_value = None
    with pytest.raises(HTTPException) as exception_info:
        await controller.create_user(1234)
    assert isinstance(exception_info.value, HTTPException)
    assert exception_info.value.detail == "Error creating user in controller"
    assert exception_info.value.status_code == 422

@pytest.mark.asyncio
async def test_login(mocker, login_data, token):
    login_mock = mocker.patch('src.api.components.users.controller.user_service.login')
    user_data = {
                "access_token": token,
                "token_type": "bearer"
                }
    login_mock.return_value = user_data

    result = await controller.login(login_data)

    assert result == user_data


if __name__ == "__main__":
    pytest.main([__file__])
