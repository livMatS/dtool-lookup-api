"""Test fixtures."""

# TODO: Tests for different authentication mechanisms

import pytest

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
    "DSERVER_VERIFY_SSL": True,
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

        from dtool_lookup_api.synchronous import (
            delete_base_uri,
            delete_dataset
        )

        datasets = [
            "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
            "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe678",
            "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe679"
        ]

        for dataset in datasets:
            delete_dataset(dataset)

        base_uris = [
            "s3://test-1",
            "s3://test_uri_1",
            "s3://test_uri_2",
            "s3://testsorting1"
        ]

        for base_uri in base_uris:
            delete_base_uri(base_uri)
