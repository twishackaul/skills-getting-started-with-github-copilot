"""Tests for the Mergington High School API."""

import pytest


class TestActivitiesEndpoints:
    """Tests for /activities endpoint."""

    def test_get_activities_returns_activity_list(self, client):
        # Arrange: nothing special, use default state
        
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "participants" in data["Chess Club"]


class TestSignupEndpoints:
    """Tests for the signup endpoint."""

    def test_signup_success(self, client):
        # Arrange
        email = "testuser1@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        email = "duplicate@mergington.edu"
        activity = "Chess Club"

        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        email = "someone@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRemoveParticipantEndpoints:
    """Tests for removing participants."""

    def test_remove_participant_success(self, client):
        # Arrange
        email = "remove-me@mergington.edu"
        activity = "Chess Club"

        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

    def test_remove_nonexistent_participant_returns_400(self, client):
        # Arrange
        email = "not-a-user@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        # Arrange
        email = "someone@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
