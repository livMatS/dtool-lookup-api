"""Test fixtures."""

import importlib
import os

import pytest

from environ import TemporaryOSEnviron

_HERE = os.path.dirname(__file__)


DTOOL_LOOKUP_SERVER_ADDRESS_AND_CREDENTIALS = {
    "DTOOL_LOOKUP_SERVER_URL": "https://localhost:5000",
    "DTOOL_LOOKUP_SERVER_TOKEN": "http://localhost:5001/token",
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
        import dtool_lookup_api.core.config
        importlib.reload(dtool_lookup_api.core.config)
        from dtool_lookup_api.core.config import Config

        # ugly workaround for making patched config values take effect in every test

        import dtool_lookup_api.asynchronous
        import dtool_lookup_api.core.LookupClient

        def mockinit(obj):
            dtool_lookup_api.core.LookupClient.LookupClient.__init__(
                obj,
                lookup_url=Config.lookup_url, auth_url=Config.auth_url,
                username=Config.username, password=Config.password,
                verify_ssl=Config.verify_ssl)

        monkeypatch.setattr(
            dtool_lookup_api.asynchronous.ConfiguredLookupClient, '__init__', mockinit)

        # from dtool_lookup_api.asynchronous import ConfiguredLookupClient
        # logger.debug("clc %s" % ConfiguredLookupClient().verify_ssl)
        # from dtool_lookup_api.config import Config
        yield dtool_config
