"""Test fixtures."""

# TODO: Tests for different authentication mechanisms

import pytest

from environ import TemporaryOSEnviron

DSERVER_ADDRESS_AND_CREDENTIALS = {
    "DSERVER_URL": "https://demo.dtool.dev/lookup",
    "DSERVER_TOKEN_GENERATOR_URL": "https://demo.dtool.dev/token",
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
