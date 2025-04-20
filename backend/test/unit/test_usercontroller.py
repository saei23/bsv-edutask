import pytest
from unittest.mock import Mock, patch
import re
from src.controllers.usercontroller import UserController

class TestUserController:
    @pytest.fixture
    def user_controller(self):
        """Fixture that creates a UserController with a mocked DAO."""
        # Create a mock object to simulate the DAO (database access)
        mocked_dao = Mock()
        # Return a UserController that uses the mocked DAO
        return UserController(dao=mocked_dao)
    
    def test_valid_email_one_user(self, user_controller):
        """test case 1: valid email one user found"""
        # Mock the DAO to return one user
        mocked_user = {"email": "test@example.com", "name": "Test User"}

        # Mock the DAO to return a list containing the mocked user
        user_controller.dao.find.return_value = [mocked_user]

        # Use patch to mock function to always return True
        # This is done to simulate a valid email format
        with patch('src.controllers.usercontroller.re.fullmatch') as mocked_regex:
            mocked_regex.return_value = True

            # Call the function with a test email
            result = user_controller.get_user_by_email("test@example.com")
            
            # Assert that the result is the mocked user object
            assert result == mocked_user

    def test_valid_email_no_users(self, user_controller):
        """test case 2: valid email no users found"""
        # Mock the DAO to return an empty list (no users found)
        user_controller.dao.find.return_value = []

        # Use patch to mock function to always return True
        # This is done to simulate a valid email format        
        with patch('src.controllers.usercontroller.re.fullmatch') as mocked_regex:
            mocked_regex.return_value = True

            # Call the function with a test email
            result = user_controller.get_user_by_email("test@example.com")

            # Assert that the function returns None when no user is found
            assert result is None

    def test_valid_email_multiple_users(self, user_controller, capfd):
        """test case 3: valid email multiple users found"""
        # Mock the DAO to return a list with multiple users
        mocked_user_1 = {"email": "test@example.com", "name": "Test User 1"}
        mocked_user_2 = {"email": "test@example.com", "name": "Test User 2"}
        user_controller.dao.find.return_value = [mocked_user_1, mocked_user_2]

        # Use patch to mock function to always return True
        # This is done to simulate a valid email format        
        with patch('src.controllers.usercontroller.re.fullmatch') as mocked_regex:
            mocked_regex.return_value = True

            # Call the function with a test email
            result = user_controller.get_user_by_email("test@example.com")

            # # Assert that the result is the first user object
            assert result == mocked_user_1

            # Capture printed output
            out, _ = capfd.readouterr()

            # Assert: some warning was printed (without assuming exact wording)
            assert out.strip() != ""

    def test_empty_string_email(self, user_controller):
        """test case 4: empty string email"""
        # Assert that the function raises a ValueError for an empty email
        with pytest.raises(ValueError):
            user_controller.get_user_by_email("")

    def test_invalid_email(self, user_controller):
        """test case 5: invalid email"""
        # Assert that the function raises a ValueError for an invalid email
        with pytest.raises(ValueError):
            user_controller.get_user_by_email("bajskorv")

    def test_dao_raises_exception(self, user_controller):
        """test case 6: DAO raises exception"""
        # Mock the DAO to raise an exception when find() is called
        user_controller.dao.find.side_effect = Exception() # Simulate database failure

        # Patch regex to simulate valid email
        with patch("src.controllers.usercontroller.re.fullmatch") as mocked_regex:
            mocked_regex.return_value = True

            # Assert that get_user_by_email raises an Exception
            with pytest.raises(Exception):
                user_controller.get_user_by_email("test@example.com")
