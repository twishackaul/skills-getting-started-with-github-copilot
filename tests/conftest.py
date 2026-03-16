"""Pytest configuration and fixtures for FastAPI testing."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before each test."""
    original = copy.deepcopy(app.activities)
    yield
    app.activities = original


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    with TestClient(app) as client:
        yield client
