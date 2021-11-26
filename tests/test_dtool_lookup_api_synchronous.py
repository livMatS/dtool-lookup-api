"""Test synchronous lookup api."""

import logging
import pytest

from utils import _log_nested_dict, _compare

# TODO: in need for more elegant way to outsource default queries and expected responses
from metadata import (
    EXPECTED_DEFAULT_ALL_RESPONSE, EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_AGGREGATION, EXPECTED_DEFAULT_AGGREGATION_RESPONSE, EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER,
    EXPECTED_CONFIG_RESPONSE, EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_LOOKUP_UUID, EXPECTED_DEFAULT_LOOKUP_RESPONSE, EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_MANIFEST_URI, EXPECTED_DEFAULT_MANIFEST_RESPONSE, EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_QUERY, EXPECTED_DEFAULT_QUERY_RESPONSE, EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_README_URI, EXPECTED_DEFAULT_README_RESPONSE, EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_SEARCH_TEXT, EXPECTED_DEFAULT_SEARCH_RESPONSE, EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER,
    EXPECTED_DEFAULT_LIST_USERS_RESPONSE, EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER,
    # EXPECTED_DEFAULT_REGISTER_USER_RESPONSE, EXPECTED_DEFAULT_REGISTER_USER_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_PERMISSION_INFO_BASE_URI, EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE, EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE_IMMUTABLE_MARKER,
    # EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE, EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_USER_INFO_USER_NAME, EXPECTED_DEFAULT_USER_INFO_RESPONSE, EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER,
)


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_all():
    from dtool_lookup_api.synchronous import all
    """Will send a request to list all registered datasets to the server."""

    logger = logging.getLogger(__name__)

    response = all()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_ALL_RESPONSE,
        EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_defaut_aggregation():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import aggregate

    logger = logging.getLogger(__name__)

    response = aggregate(DEFAULT_AGGREGATION)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_AGGREGATION_RESPONSE,
        EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_config():
    """Will send an request for configuration info to the server."""
    from dtool_lookup_api.synchronous import config

    logger = logging.getLogger(__name__)

    response = config()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_CONFIG_RESPONSE,
        EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_defaut_lookup():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import lookup

    logger = logging.getLogger(__name__)

    response = lookup(DEFAULT_LOOKUP_UUID)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_defaut_manifest():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import manifest

    logger = logging.getLogger(__name__)

    response = manifest(DEFAULT_MANIFEST_URI)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_defaut_query():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import query

    logger = logging.getLogger(__name__)

    response = query(DEFAULT_QUERY)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_QUERY_RESPONSE,
        EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_default_readme():
    """Will send an empty search request to the server."""
    from dtool_lookup_api.synchronous import readme

    logger = logging.getLogger(__name__)

    response = readme(DEFAULT_README_URI)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_README_RESPONSE,
        EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_default_search():
    """Will send an empty search request to the server."""
    from dtool_lookup_api.synchronous import search

    logger = logging.getLogger(__name__)

    response = search(DEFAULT_SEARCH_TEXT)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 2

    compares = _compare(
        response,
        EXPECTED_DEFAULT_SEARCH_RESPONSE,
        EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_user_info():
    """Will send a user info request to the server."""
    from dtool_lookup_api.synchronous import user_info

    logger = logging.getLogger(__name__)

    response = user_info(DEFAULT_USER_INFO_USER_NAME)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_USER_INFO_RESPONSE,
        EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


# admin routes

# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_default_list_users():
    """Will send a list users request to the server."""
    from dtool_lookup_api.synchronous import list_users

    logger = logging.getLogger(__name__)

    response = list_users()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_LIST_USERS_RESPONSE,
        EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


# TODO: clean up, i.e. delete users after use
@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_default_register_user():
    """Will send a register user request to the server."""
    from dtool_lookup_api.synchronous import register_user

    logger = logging.getLogger(__name__)

    # mimic https://github.com/jic-dtool/dtool-lookup-server/blob/12baba73eebc668b4998ae2c2ea43946dc3bf856/tests/test_admin_user_routes.py#L14
    users = [
        {"username": "evil-witch", "is_admin": True},
        {"username": "dopey"}
    ]

    # TODO: check for nonexistence of not yet registered users on server

    for user in users:
        response = register_user(**user)
        assert response == True
        logger.debug("Response:")
        _log_nested_dict(logger.debug, response)

    # Ensure idempotent.
    for user in users:
        response = register_user(**user)
        assert response == True
        logger.debug("Response:")
        _log_nested_dict(logger.debug, response)

    # TODO: check for existence of registered users on server


# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
def test_default_permission_info():
    """Will send a permission info request to the server."""
    from dtool_lookup_api.synchronous import permission_info

    logger = logging.getLogger(__name__)

    response = permission_info(DEFAULT_PERMISSION_INFO_BASE_URI)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 3

    compares = _compare(
        response,
        EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE,
        EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


# TODO: test for update_permissions
# @pytest.mark.usefixtures("dtool_lookup_server", "dtool_config")
# def test_default_update_permissions():
#     """Will send a permission info request to the server."""
#     from dtool_lookup_api.synchronous import update_permissions
#
#     logger = logging.getLogger(__name__)
#
#     response = update_permissions()
#     assert response is not None
#
#     logger.debug("Response:")
#     _log_nested_dict(logger.debug, response)
#
#     assert len(response) == 1
#
#     compares = _compare(
#         response,
#         EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE,
#         EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE_IMMUTABLE_MARKER
#     )
#     assert compares
