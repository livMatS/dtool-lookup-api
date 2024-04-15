"""Test synchronous lookup api."""

import logging
import pytest
import yaml

from utils import _log_nested_dict, _compare, NoDatesSafeLoader

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
    DEFAULT_USER_INFO_USER_NAME, EXPECTED_DEFAULT_USER_INFO_RESPONSE, EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER,EXPECTED_DEFAULT_VERSIONS_RESPONSE,
    EXPECTED_DEFAULT_VERSIONS_RESPONSE_IMMUTABLE_MARKER,PAGINATION_PARAMETERS
)


@pytest.mark.usefixtures("dserver", "dtool_config")
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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_aggregation():
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


@pytest.mark.usefixtures("dserver", "dtool_config")
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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_lookup():
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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_manifest():
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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_query():
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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_readme():
    """Will send an empty search request to the server."""
    from dtool_lookup_api.synchronous import readme

    logger = logging.getLogger(__name__)

    response = readme(DEFAULT_README_URI)
    assert response is not None

    logger.debug("Response:")
    logger.debug(response)

    logger.debug("Parsed:")
    parsed_readme = yaml.load(response, Loader=NoDatesSafeLoader)
    _log_nested_dict(logger.debug, parsed_readme)

    compares = _compare(
        parsed_readme,
        EXPECTED_DEFAULT_README_RESPONSE,
        EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
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
        sorted(response, key=lambda r: r['uri']),
        EXPECTED_DEFAULT_SEARCH_RESPONSE,
        EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_pagination():

    from dtool_lookup_api.synchronous import search



    # Using ** to unpack dictionary values as function arguments
    dataset_list = search(**PAGINATION_PARAMETERS)

    # Validate that pagination dict was populated
    pagination = PAGINATION_PARAMETERS["pagination"]
    assert pagination

    # Here, we only check the keys that are present in the pagination dictionary
    if 'total' in pagination:
        assert pagination['total'] >= 0

    if 'page' in pagination and 'total_pages' in pagination:
        # Ensure current page is less than or equal to total pages
        assert pagination['page'] <= pagination['total_pages']

        # If on the first page, ensure that `first_page` is equivalent to the current page
        if pagination['page'] == 1 and 'first_page' in pagination:
            assert pagination['first_page'] == 1

        # If on the last page, ensure there isn't a next_page and that `last_page` is equivalent to the current page
        if pagination['page'] == pagination['total_pages']:
            assert 'next_page' not in pagination
            if 'last_page' in pagination:
                assert pagination['last_page'] == pagination['page']

    # Check if `next_page` makes sense, given the total pages and the current page
    if 'next_page' in pagination and 'total_pages' in pagination:
        assert pagination['next_page'] <= pagination['total_pages']
        assert pagination['next_page'] > pagination.get('page', 0)

    # Print out keys that were not present for debugging or information
    expected_keys = ['total', 'total_pages', 'first_page', 'last_page', 'page', 'next_page']
    missing_keys = [key for key in expected_keys if key not in pagination]
    for key in missing_keys:
        print(f"Optional key {key} is not present in pagination")

# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dserver", "dtool_config")
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
@pytest.mark.usefixtures("dserver", "dtool_config")
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
# @pytest.mark.usefixtures("dserver", "dtool_config")
# def test_default_register_user():
#    """Will send a register user request to the server."""
#    from dtool_lookup_api.synchronous import register_user
#
#    logger = logging.getLogger(__name__)
#
#    # mimic https://github.com/jic-dtool/dserver/blob/12baba73eebc668b4998ae2c2ea43946dc3bf856/tests/test_admin_user_routes.py#L14
#    users = [
#        {"username": "evil-witch", "is_admin": True},
#        {"username": "dopey"}
#    ]
#
#    # TODO: check for nonexistence of not yet registered users on server
#
#    for user in users:
#        response = register_user(**user)
#        assert response == True
#        logger.debug("Response:")
#        _log_nested_dict(logger.debug, response)
#
#    # Ensure idempotent.
#    for user in users:
#        response = register_user(**user)
#        assert response == True
#        logger.debug("Response:")
#        _log_nested_dict(logger.debug, response)
#
#    # TODO: check for existence of registered users on server


# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dserver", "dtool_config")
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
# @pytest.mark.usefixtures("dserver", "dtool_config")
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

@pytest.mark.usefixtures("dserver", "dtool_config")
def test_versions():
    """Will send a request for versions to the server."""
    from dtool_lookup_api.synchronous import versions

    logger = logging.getLogger(__name__)

    response = versions()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_VERSIONS_RESPONSE,
        EXPECTED_DEFAULT_VERSIONS_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares
