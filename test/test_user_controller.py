from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest
from datetime import datetime
from src.db.models import UserRole, User
from src.api.components.users.schemas import UserRegister
from src.api.components.users import controller
from src.api.components.users.service import UserService

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
def unconfirmed_user():
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
def admin_user():
    return User(
        user_id = "e0c33d6b-f2f4-4cc2-b907-1bb083c6af7",
        name = "Mario",
        email = "mario@gmail.com",
        password_hash = "aa9b1d4a-1c4d-4e67-ad2c-dbf36bdf1b81",
        creation_date = datetime.now,
        role = UserRole.admin,
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

@pytest.fixture
def user_email():
    return "guido@gmail.com"

@pytest.fixture
def confirmation_code():
    return 1234

@pytest.fixture
def mock_roles_required(mocker):
    return mocker.patch('src.api.components.users.controller.roles_required')


#### TESTS #### 
@pytest.mark.anyio
def test_get_all_users(mocker, user, unconfirmed_user, token, mock_roles_required):
    mock_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')
    mock_roles_required.return_value = None
    mock_get_all_users.return_value = [user, unconfirmed_user]

    result = controller.get_all_users(token)

    mock_get_all_users.assert_called_once()
    mock_roles_required.assert_called_once_with([UserRole.admin], token)
    assert result == [user, unconfirmed_user]


@pytest.mark.anyio
def test_get_all_users_role_fail(mocker, token, mock_roles_required):
    mock_service_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')
    mock_roles_required.side_effect = HTTPException(status_code=403, detail="Unauthorized")

    with pytest.raises(HTTPException) as exception_info:
        controller.get_all_users(token)

    mock_roles_required.assert_called_once_with([UserRole.admin], token)
    mock_service_get_all_users.assert_not_called()

    assert exception_info.value.status_code == 403
    assert exception_info.value.detail == "Unauthorized"

    mock_service_get_all_users.assert_not_called()


@pytest.mark.anyio
def test_get_all_users_fail(mocker, token, mock_roles_required):
    mock_service_get_all_users = mocker.patch('src.api.components.users.controller.user_service.get_all_users')

    mock_roles_required.return_value = None    
    mock_service_get_all_users.return_value = None
    controller.get_all_users(token)

    mock_service_get_all_users.assert_called_once()
    mock_roles_required.assert_called_once_with([UserRole.admin], token)

@pytest.mark.anyio
def test_get_user_by_id(mocker, token, user,mock_roles_required):
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')

    mock_roles_required.return_value = None    
    mock_service_get_user_by_id.return_value = user
    result = controller.get_user_by_id("e0c33d6b-f2f4-4cc2-b907-1bb083c6af7b", token)
    assert result == user
    mock_service_get_user_by_id.assert_called_once()
    mock_roles_required.assert_called_once_with([UserRole.admin], token)

@pytest.mark.anyio
def test_get_user_by_id_role_fail(mocker, token, mock_roles_required, user):
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')
    mock_roles_required.side_effect = HTTPException(status_code=403, detail="Access denied")

    with pytest.raises(HTTPException) as exception:
        controller.get_user_by_id(user.user_id, token) 

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    mock_service_get_user_by_id.assert_not_called()
    mock_roles_required.assert_called_once_with([UserRole.admin], token)

@pytest.mark.anyio
def test_get_user_by_id_fail(mocker, token, mock_roles_required):
    mock_service_get_user_by_id = mocker.patch('src.api.components.users.controller.user_service.get_user_by_id')

    mock_service_get_user_by_id.return_value = None
    mock_roles_required.return_value = None

    controller.get_user_by_id(token)   
    mock_service_get_user_by_id.assert_called_once()

@pytest.mark.anyio
def test_get_user_by_email(mocker, token, admin_user, mock_roles_required):
    mock_service_get_user_by_email = mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    mock_service_get_user_by_email.return_value = admin_user

    result = controller.get_user_by_email(admin_user.email, token)   
    
    mock_roles_required.assert_called_once_with([UserRole.admin], token)
    mock_roles_required.return_value = None
    mock_service_get_user_by_email.assert_called_once_with(admin_user.email)
    assert result == admin_user

@pytest.mark.anyio
def test_get_user_by_email_role_fail(mocker, token, mock_roles_required, user_email):
    mock_service_get_user_by_email = mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    mock_roles_required.side_effect = HTTPException(status_code=403, detail="Access denied")

    with pytest.raises(HTTPException) as exception:
        controller.get_user_by_email(user_email) 

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    mock_service_get_user_by_email.assert_not_called()

@pytest.mark.anyio
def test_get_user_by_email_fail(mocker, token, user_email, mock_roles_required):
    mock_service_get_user_by_email =  mocker.patch('src.api.components.users.controller.user_service.get_user_by_email')
    mock_service_get_user_by_email.return_value = None
    controller.get_user_by_email(user_email, token)
    mock_roles_required.assert_called_once_with([UserRole.admin], token)
    mock_service_get_user_by_email.assert_called_once_with(user_email)

@pytest.mark.anyio
def test_create_register_submition(mocker, user_register):
    mock_service_create_register_submition = mocker.patch('src.api.components.users.controller.user_service.create_register_submition', return_value = "Verification email sent to guido@gmail.com")
    result = controller.create_register_submition(user_register)
    assert mock_service_create_register_submition.called_once
    assert result == "Verification email sent to guido@gmail.com"

@pytest.mark.anyio
def test_create_register_submition_email_exists(mocker, user_register, user):
    mock_service_get_user_by_email = mocker.patch('src.api.components.users.controller.user_service.get_user_by_email', return_value = user)
    mock_service_create_register_submition = mocker.patch('src.api.components.users.controller.user_service.create_register_submition')
    with pytest.raises(HTTPException) as exception_info:
        controller.create_register_submition(user_register)

    mock_service_get_user_by_email.assert_called_once_with(user_register.email)
    mock_service_create_register_submition.assert_not_called()
    assert exception_info.value.status_code == 409
    assert exception_info.value.detail == "User with mail guido@gmail.com already exists."

@pytest.mark.anyio
def test_confirm_user(mocker, unconfirmed_user, mock_roles_required):

    EXISTING_USER = unconfirmed_user
    confirmationCode = 1234

    mock_get_user_by_confirmation_code = mocker.patch('src.api.components.users.controller.user_service.get_user_by_confirmation_code')
    mock_user_service_confirm_user = mocker.patch('src.api.components.users.controller.user_service.confirm_user')

    mock_response = JSONResponse(status_code=200, content={"message": "User Mario updated successfully."})
    mock_get_user_by_confirmation_code.return_value = EXISTING_USER
    mock_user_service_confirm_user.return_value = mock_response
   
    result = controller.confirm_user(1234)
  
    mock_roles_required.assert_called_once_with([UserRole.admin, UserRole.unconfirmed], code=confirmationCode)
  
    mock_get_user_by_confirmation_code.assert_called_once_with(confirmationCode)
   
    mock_user_service_confirm_user.assert_called_once_with(EXISTING_USER)

    assert result.status_code == 200
    assert result.body == b'{"message":"User Mario updated successfully."}'

@pytest.mark.anyio
def test_confirm_user_role_fail(mocker, confirmation_code, mock_roles_required):
    mock_service_confirm_user = mocker.patch('src.api.components.users.controller.user_service.confirm_user')

    mock_roles_required.side_effect = HTTPException(status_code=403, detail="Access denied")

    with pytest.raises(HTTPException) as exception:
        controller.confirm_user(confirmation_code)

    assert exception.value.status_code == 403
    assert exception.value.detail == 'Access denied'
    mock_roles_required.assert_called_once_with([UserRole.admin, UserRole.unconfirmed], code=confirmation_code)
    mock_service_confirm_user.assert_not_called()

@pytest.mark.anyio
def test_confirm_user_fail(mocker, confirmation_code, mock_roles_required):
    user_service_confirm_user = mocker.patch('src.api.components.users.controller.user_service.confirm_user')
    mock_user_service_get_user_by_confirmation_code = mocker.patch('src.api.components.users.controller.user_service.get_user_by_confirmation_code')
    
    mock_user_service_get_user_by_confirmation_code.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        controller.confirm_user(confirmation_code)
    mock_roles_required.assert_called_once_with([UserRole.admin, UserRole.unconfirmed], code=confirmation_code)
    user_service_confirm_user.assert_not_called()
    assert isinstance(exception_info.value, HTTPException)
    assert exception_info.value.detail == "Incorrect code"
    assert exception_info.value.status_code == 400

@pytest.mark.anyio
def test_login(mocker, login_data, token):
    service_login_mock = mocker.patch('src.api.components.users.controller.user_service.login')
    user_data = {
                "access_token": token,
                "token_type": "bearer"
                }
    service_login_mock.return_value = user_data
    result = controller.login(login_data)
    assert result == user_data

@pytest.mark.anyio
def test_forgot_password(mocker, user_email):
    mock_service_forgot_password = mocker.patch('src.api.components.users.controller.user_service.forgot_password')
    result = controller.forgot_password(user_email)
    mock_service_forgot_password.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])
