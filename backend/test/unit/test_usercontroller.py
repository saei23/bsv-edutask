import pytest
from src.util.helpers import hasAttribute

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
