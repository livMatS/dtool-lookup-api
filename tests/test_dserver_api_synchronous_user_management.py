"""Test synchronous lookup api user management."""

import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

# user info

DEFAULT_USER_INFO_USER_NAME = 'testuser'
EXPECTED_DEFAULT_USER_INFO_RESPONSE = {
    'is_admin': True,
    'register_permissions_on_base_uris': [],
    'search_permissions_on_base_uris': ['smb://test-share', 's3://test-bucket'],
    'username': 'testuser'
}
EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_USER_INFO_RESPONSE)

# list users

EXPECTED_DEFAULT_LIST_USERS_RESPONSE = [{
    'is_admin': True,
    'username': 'testuser'
}]
EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_LIST_USERS_RESPONSE)


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


# mark to run early in order to not have any other users registered in database by other tests
@pytest.mark.first
@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_users():
    """Will send a list users request to the server."""
    from dtool_lookup_api.synchronous import get_users

    logger = logging.getLogger(__name__)

    response = get_users()
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
@pytest.mark.skip(reason="User management currently broken.")
@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_register_user():
    """Will send a register user request to the server."""
    from dtool_lookup_api.synchronous import get_user, register_user, delete_user

    logger = logging.getLogger(__name__)

    # mimic https://github.com/jic-dtool/dserver/blob/12baba73eebc668b4998ae2c2ea43946dc3bf856/tests/test_admin_user_routes.py#L14
    users = [
        {"username": "evil-witch", "is_admin": True},
        {"username": "dopey"}
    ]

    expected_responses = [
        {
            'username': 'evil-witch',
            'is_admin': True,
            'register_permissions_on_base_uris': [],
            'search_permissions_on_base_uris': [],
         },
         {
            'username': 'dopey',
            'is_admin': False,
            'register_permissions_on_base_uris': [],
            'search_permissions_on_base_uris': [],
         }
    ]

    # assure users do not yet exist
    for user in users:
        response = get_user(user["username"])
        assert "code" in response and response["code"] == 404

    # create users
    for user in users:
        response = register_user(**user)
        assert response == True

    # assure users exist
    for user, expected_response in zip(users, expected_responses):
        response = get_user(user["username"])
        assert response == expected_response

    # ensure idempotent
    for user in users:
        response = register_user(**user)
        assert response == True

    # assure users still exist
    for user, expected_response in zip(users, expected_responses):
        response = get_user(user["username"])
        assert response == expected_response

    # delete users
    for user in users:
        response = delete_user(user["username"])
        assert response == True

    # assure users don't exist anymore
    for user in users:
        response = get_user(user["username"])
        assert "code" in response and response["code"] == 404

    # TODO: check for existence of registered users on server

