"""Fixtures for tests."""

import pytest

@pytest.fixture(name="runner")
def fixture_tuple() -> tuple:
    """Tuple fixture for testing."""
    return (1, 2, 3)


