import pytest
from unittest.mock import Mock, patch
import re
from src.controllers.usercontroller import UserController

# Arrange: setup all preconditions of the test
# Act: let the system under test perform an operation
# Assert: compare the systems response to the expected response

# Unit tests should contain only one assert statement
# Simular test cases will contain a lot of redundant setup code, this code can be extracted into fixtures.
# We can evaluate the quality of our test by calculating test coverage:
# pytest --cov=src/util --cov-report term-missing

# Creating a pytest.ini file in the root directory of the backend, whih allows you to configure the
# execution of the pytest command.

# We can ensure that a unit works reliably by mocking its logic
# Avoid control structures (conditions, loops) in unit tests


# Variable fixtures: fixtures encapsulate the setup of the SUT, but a variable parameter makes fixtures difficult
# If you want to see hoe pytest handles fixture setup: run pytest command with -setup-show
# Debugging with prints: -capture=no will allow you to print the console

class TestUserController:

    @pytest.fixture
    def user_controller(self):
        """Create user controller with mocked DAO"""
        controller = Usercontroller()
        controller.dao = Mock()
        return controller


    def test_valid_email_one_user(self, user_controller):
        """test case 1: valid email one user found"""

    
    def test_valid_email_no_users(self, user_controller):
        """test case 2: valid email no users found"""


    def test_valid_email_multiple_users(self, user_controller, capfd):
        """test case 3: valid email multiple users found"""

    def test_empty_string_email(self, user_controller):
        """test case 4: empty string email"""


    def test_invalid_email(self, user_controller):
        """test case 5: invalid email"""


    def test_case_variation_email(self, user_controller):
        """test case 6: case variation email"""

    
    def test_none_as_email(self, user_controller):
        """test case 7: None as email"""

    def test_dao_raises_exception(self, user_controller):
        """test case 8: DAO raises exception"""
