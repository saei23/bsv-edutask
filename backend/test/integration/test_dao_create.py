import pytest
import pymongo
from unittest.mock import Mock, patch
from pymongo.errors import WriteError, DuplicateKeyError

from src.util.dao import DAO
from src.util.validators import getValidator


class TestDAOCreate:
    @pytest.fixture
    def dao(self, monkeypatch):
        """
        Fixture that sets MONGO_URL and returns a DAO for a test collection.
        Drops the collection before and after each test to avoid interference.
        """
        # # Set the environment variable for MongoDB URL
        # monkeypatch.setenv("MONGO_URL", "mongodb://localhost:27017")

        # # Define the test collection
        # test_collection = "user" # matches src/static/validators/user.json
        
        # # Create DAO instance and reset before/after the test
        # dao = DAO(test_collection)
        # dao.drop() # Drop collection before test if it exists
        # yield dao
        # dao.drop() # Drop collection after the test
        monkeypatch.setenv("MONGO_URL", "mongodb://localhost:27017")

        test_collection = "user"

        # Koppla direkt till databasen och skapa om collectionen med validering
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.edutask
        db.drop_collection(test_collection)

        validator = getValidator(test_collection)

        db.create_collection(
            test_collection,
            validator=validator,
            validationLevel='strict',
            validationAction='error'
        )

        db[test_collection].create_index("email", unique=True)

        # Skapa DAO efter att collectionen är korrekt konfigurerad
        dao = DAO(test_collection)

        yield dao

        # Rensa efter test
        dao.drop()
    
    def test_create_valid_object(self, dao):
        """Test creating a valid document in the collection."""
        # Arrange
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "isActive": True
        }
        # Act
        result = dao.create(data)
        # Assert
        assert result is not None
        assert "_id" in result
        assert result["firstName"] == data["firstName"]
        assert result["lastName"] == data["lastName"]
        assert result["email"] == data["email"]
        assert result["isActive"] == data["isActive"]

    def test_create_missing_field(self, dao):
        """Test creating a document with a missing required property."""
        # Arrange
        data = {
            "firstName": "John",
            "lastName": "Doe",
            # "email" is missing
        }

        # Act & Assert: Expect WriteError due to missing required field
        with pytest.raises(WriteError):
            dao.create(data)

    def test_create_invalid_type(self, dao):
        """Test creating a document with an invalid data type."""
        data = {
            "firstName": "John",
            "lastName": 123, # Invalid type for lastName    
            "email": "john.doe@example.com",
            "isActive": "not a boolean"
        }

        # Act & Assert: Expect WriteError due to invalid data types        
        with pytest.raises(WriteError):
            dao.create(data)

    def test_create_duplicate_unique(self, dao):
        """Test creating a document with a duplicate unique value."""
        doc1 = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "duplicate@example.com"
        }

        doc2 = {
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "duplicate@example.com" # same email as doc1
        }

        dao.create(doc1)
        # Act & Assert: Expect WriteError due to missing required field
        with pytest.raises(WriteError):
            dao.create(doc2)

    def test_create_database_connection_error(self, dao):
        """Test handling a database error during creation."""
        # Use patch to simulate a database error
        with patch.object(dao.collection, 'insert_one', side_effect=Exception("Database error")):
            # Arrange 
            data = {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com"
            }
            
            # Act & Assert
            with pytest.raises(Exception) as excinfo:
                dao.create(data)
            
            assert "Database error" in str(excinfo.value)
