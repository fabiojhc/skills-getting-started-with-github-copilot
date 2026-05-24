import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesEndpoints:
    """Test suite for activities API endpoints using AAA pattern"""

    def test_get_activities(self):
        """Test GET /activities returns all activities"""
        # Arrange
        # No specific setup needed - activities are predefined in app

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        # Arrange
        activity = "Chess Club"
        email = "test_signup@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]

    def test_signup_for_nonexistent_activity(self):
        """Test signup for activity that doesn't exist"""
        # Arrange
        nonexistent_activity = "Non Existent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_success(self):
        """Test successful unregistration from an activity"""
        # Arrange
        activity = "Chess Club"
        email = "delete_test@mergington.edu"
        
        # First, sign up the student
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_unregister_not_registered(self):
        """Test unregistering a student who isn't registered"""
        # Arrange
        activity = "Chess Club"
        email = "not_registered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not registered" in response.json()["detail"]

    def test_unregister_nonexistent_activity(self):
        """Test unregistering from activity that doesn't exist"""
        # Arrange
        nonexistent_activity = "Non Existent"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_root_redirects_to_static(self):
        """Test root endpoint redirects to /static/index.html"""
        # Arrange
        expected_redirect = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect
