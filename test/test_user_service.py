from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest
from fastapi.security import  OAuth2PasswordRequestForm

from src.db.models import UserRole, User
from src.api.components.users.service import UserService
from src.utils.email_handler import EmailHandler

#### MOCKS ####

@pytest.fixture
def user_service_instance():
    return UserService()

@pytest.fixture
def mock_OAuth2PasswordRequestForm():
    return OAuth2PasswordRequestForm(username="test@example.com",
            password="password123")

@pytest.fixture
def fake_user():
    return User(user_id="1", name="test_user", email="test@example.com", attempts_canching_password = 0)

#### TEST ####

class TestUserService:

    def test_get_all_users(self, user_service_instance, mocker):
        mock_get_all_users = mocker.patch.object(user_service_instance.user_repository, 'get_all_users', return_value=["user1", "user2", "user3"])
        result = user_service_instance.get_all_users()
        mock_get_all_users.assert_called_once()
        assert result == ["user1", "user2", "user3"]

    def test_get_user_by_confirmation_code(self, user_service_instance, mocker):
        confirmation_code = 1234
        mock_get_user_by_confirmation_code = mocker.patch.object(
            user_service_instance.user_repository,
            'get_user_by_confirmation_code',
            return_value={"user_id": 1, "name": "test_user", "confirmation_code": confirmation_code}
        )
        result = user_service_instance.get_user_by_confirmation_code(confirmation_code)
        mock_get_user_by_confirmation_code.assert_called_once_with(confirmation_code)
        assert result == {"user_id": 1, "name": "test_user", "confirmation_code": confirmation_code}

    def test_confirm_user(self, user_service_instance, mocker):
        unconfirmed_user = User(user_id='abcd', name="test_user", role=UserRole.unconfirmed, confirmation_code=1234)
        confirmed_user = {
            "role": UserRole.user,
            "confirmation_code": 1
        }
        mock_update_user = mocker.patch.object(
            user_service_instance.user_repository,
            'update_user',
            return_value=confirmed_user
        )
        result = user_service_instance.confirm_user(unconfirmed_user)
        mock_update_user.assert_called_once_with(unconfirmed_user.user_id, confirmed_user)

        assert result == confirmed_user

    def test_login(self, user_service_instance, mocker, mock_OAuth2PasswordRequestForm):
        user_data = mock_OAuth2PasswordRequestForm
        user_db = User(user_id=1, email="test@example.com", name="Test User", role="user", password_hash="hashed_password")

        mocker.patch.object(user_service_instance.user_repository, 'get_user_by_email', return_value=user_db)

        mock_verify_password = mocker.patch("src.api.components.users.service.verify_password")
        mock_create_access_token = mocker.patch("src.api.components.users.service.create_access_token")

        mock_verify_password.return_value = True
        mock_create_access_token.return_value="fake_access_token"

        result = user_service_instance.login(user_data)

        user_service_instance.user_repository.get_user_by_email.assert_called_once_with(user_data.username)
        mock_verify_password.assert_called_once_with(user_data.password, user_db.password_hash)

        mock_create_access_token.assert_called_once_with({
            "user_id": user_db.user_id,
            "name": user_db.name,
            "role": user_db.role
        })
        expected_result = {
            "access_token": "fake_access_token",
            "token_type": "bearer"
        }
        assert result == expected_result

    def test_forgot_password(self, user_service_instance, fake_user, mocker):

        mocker.patch.object(user_service_instance.user_repository, 'get_user_by_email', return_value=fake_user)

        mocker.patch.object(EmailHandler, 'send_change_password_email')

        result = user_service_instance.forgot_password(fake_user.email)
        user_service_instance.user_repository.get_user_by_email.assert_called_once_with(fake_user.email)
        EmailHandler.send_change_password_email.assert_called_once()

        expected_result = JSONResponse(status_code=200, content={"message": f'Email to {fake_user.email} sent successfully.'})
        assert result.status_code == expected_result.status_code
        assert result.body ==  b'{"message":"Email to test@example.com sent successfully."}'

    def test_forgot_password_user_exist_Exception(self, user_service_instance, mocker):
        email = "test@example.com"
        mocker.patch.object(user_service_instance.user_repository, 'get_user_by_email', return_value=None)
        mocker.patch.object(EmailHandler, 'send_change_password_email')
        with pytest.raises(HTTPException) as exc_info:
            user_service_instance.forgot_password(email)
        assert exc_info.value.detail == f'User "{email}" not found'
        assert exc_info.value.status_code == 404
        EmailHandler.send_change_password_email.assert_not_called()

    def test_forgot_password_exception_EmailHandler(self, user_service_instance, fake_user, mocker):
        mocker.patch.object(user_service_instance.user_repository, 'get_user_by_email', return_value=fake_user)
        email_handler = mocker.patch.object(EmailHandler, 'send_change_password_email')
        email_handler.side_effect = HTTPException(status_code=400, detail=f"Error sending change password email:")
        with pytest.raises(HTTPException) as exc_info:
            user_service_instance.forgot_password(fake_user.email)
        user_repository_save_reset_password_token = mocker.patch.object(user_service_instance.user_repository, 'save_reset_password_token')

        user_repository_save_reset_password_token.assert_not_called()
        assert exc_info.value.detail == "Error sending change password email:"
 
