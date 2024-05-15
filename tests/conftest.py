"""Test fixtures."""

# TODO: Tests for different authentication mechanisms

import pytest
import os

from environ import TemporaryOSEnviron


def pytest_addoption(parser):
    """Add command line argument to pytest for selecting dserver configuration to test against."""
    parser.addoption(
        "--dserver-config", action="store", default="remote", help="local or remote"
    )


REMOTE_DSERVER_ADDRESS_AND_CREDENTIALS = {
    "DSERVER_URL": "https://demo.dtool.dev/lookup",
    "DSERVER_TOKEN_GENERATOR_URL": "https://demo.dtool.dev/token",
    "DSERVER_USERNAME": "testuser",
    "DSERVER_PASSWORD": "test_password",
    "DSERVER_VERIFY_SSL": False,
}

LOCAL_DSERVER_ADDRESS_AND_CREDENTIALS = {
    "DSERVER_URL": "http://localhost:5000",
    "DSERVER_TOKEN_GENERATOR_URL": "http://localhost:5001/token",
    "DSERVER_USERNAME": "test-user",
    "DSERVER_PASSWORD": "test-password",
    "DSERVER_VERIFY_SSL": False,
}

@pytest.fixture
def dserver_config_cli_argument(request):
    return request.config.getoption("--dserver-config")


# TODO: dserver testing instance provision not handled
@pytest.fixture(scope="session")
def dserver(request):
    pass  # stub


@pytest.fixture
def dtool_config(monkeypatch, dserver_config_cli_argument):
    """Provide default dtool config."""
    if dserver_config_cli_argument == "remote":
        dtool_config = REMOTE_DSERVER_ADDRESS_AND_CREDENTIALS
    else:
        dtool_config = LOCAL_DSERVER_ADDRESS_AND_CREDENTIALS

    with TemporaryOSEnviron(env=dtool_config):
        yield dtool_config
