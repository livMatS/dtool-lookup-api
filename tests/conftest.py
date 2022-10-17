"""Test fixtures."""

# TODO: Tests for different authentication mechnanisms

import pytest

from environ import TemporaryOSEnviron

DTOOL_LOOKUP_SERVER_ADDRESS_AND_CREDENTIALS = {
    "DTOOL_LOOKUP_SERVER_URL": "https://localhost:5100",
    "DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL": "https://localhost:5101/token",
    "DTOOL_LOOKUP_SERVER_USERNAME": "testuser",
    "DTOOL_LOOKUP_SERVER_PASSWORD": "test_password",
    "DTOOL_LOOKUP_SERVER_VERIFY_SSL": False,
}


# TODO: dtool-lookup-server testing instance provision not handled
@pytest.fixture(scope="session")
def dtool_lookup_server(request):
    pass  # stub


@pytest.fixture
def dtool_config(monkeypatch):
    """Provide default dtool config."""
    dtool_config = DTOOL_LOOKUP_SERVER_ADDRESS_AND_CREDENTIALS

    with TemporaryOSEnviron(env=dtool_config):
        yield dtool_config
