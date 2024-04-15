"""Test fixtures."""

# TODO: Tests for different authentication mechnanisms

import pytest

from environ import TemporaryOSEnviron

DSERVER_ADDRESS_AND_CREDENTIALS = {
    "DSERVER_URL": "https://localhost:5000",
    "DSERVER_TOKEN_GENERATOR_URL": "https://localhost:5001/token",
    "DSERVER_USERNAME": "testuser",
    "DSERVER_PASSWORD": "test_password",
    "DSERVER_VERIFY_SSL": False,
}


# TODO: dserver testing instance provision not handled
@pytest.fixture(scope="session")
def dserver(request):
    pass  # stub


@pytest.fixture
def dtool_config(monkeypatch):
    """Provide default dtool config."""
    dtool_config = DSERVER_ADDRESS_AND_CREDENTIALS

    with TemporaryOSEnviron(env=dtool_config):
        yield dtool_config
