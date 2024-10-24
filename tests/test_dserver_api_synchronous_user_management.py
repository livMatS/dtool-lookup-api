"""Test synchronous lookup api user management."""

import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

ASCENDING = 1
DESCENDING = -1

# user info

DEFAULT_USER_INFO_USER_NAME = "testuser"
EXPECTED_DEFAULT_USER_INFO_RESPONSE = {
    "is_admin": True,
    "register_permissions_on_base_uris": [],
    "search_permissions_on_base_uris": ["smb://test-share", "s3://test-bucket"],
    "username": "testuser",
}
EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_USER_INFO_RESPONSE
)
# ordering not guaranteed
EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER[
    "search_permissions_on_base_uris"
] = [False, False]

# list users

EXPECTED_DEFAULT_LIST_USERS_RESPONSE = [{"is_admin": True, "username": "testuser"}]
EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_LIST_USERS_RESPONSE
)

# sorted by username

EXPECTED_DEFAULT_DESCENDING_USER_RESPONSE = [
    {"is_admin": True, "username": "testuser"},
    {"is_admin": True, "username": "evil-witch"},
    {"is_admin": False, "username": "dopey"},
]

EXPECTED_DEFAULT_DESCENDING_USER_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_DESCENDING_USER_RESPONSE)

EXPECTED_DEFAULT_ASCENDING_USER_RESPONSE = [{'is_admin': False, 'username': 'dopey'}, {
    'is_admin': True, 'username': 'evil-witch'}, {'is_admin': True, 'username': 'testuser'}]
EXPECTED_DEFAULT_ASCENDING_USER_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_ASCENDING_USER_RESPONSE)

# summary

EXPECTED_DEFAULT_SUMMARY_RESPONSE = {
    "base_uris": ["s3://test-bucket", "smb://test-share"],
    "creator_usernames": ["jotelha"],
    "datasets_per_base_uri": {"s3://test-bucket": 1, "smb://test-share": 283},
    "datasets_per_creator": {"jotelha": 284},
    "datasets_per_tag": {"first-half": 140, "second-third": 94},
    "number_of_datasets": 284,
    "tags": ["first-half", "second-third"],
}

EXPECTED_DEFAULT_SUMMARY_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_SUMMARY_RESPONSE
)

# me

EXPECTED_DEFAULT_ME_RESPONSE = {
    "is_admin": True,
    "register_permissions_on_base_uris": [],
    "search_permissions_on_base_uris": ["smb://test-share", "s3://test-bucket"],
    "username": "testuser",
}

EXPECTED_DEFAULT_ME_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_ME_RESPONSE
)
# ordering not guaranteed
EXPECTED_DEFAULT_ME_RESPONSE_IMMUTABLE_MARKER["search_permissions_on_base_uris"] = [
    False,
    False,
]

# get my summary

EXPECTED_DEFAULT_MY_SUMMARY_RESPONSE = EXPECTED_DEFAULT_SUMMARY_RESPONSE

EXPECTED_DEFAULT_MY_SUMMARY_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_MY_SUMMARY_RESPONSE
)

# mark to run early in order to not have any other users registered in database by other tests
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
        EXPECTED_DEFAULT_USER_INFO_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares


# mark to run early in order to not have any other users registered in database by other tests
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
        EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_register_user():
    """Will send a register user request to the server."""
    from dtool_lookup_api.synchronous import (
        get_user,
        register_user,
        delete_user,
        get_users,
    )

    logger = logging.getLogger(__name__)

    users = [{"username": "evil-witch", "is_admin": True}, {"username": "dopey"}]

    expected_responses = [
        {
            "username": "evil-witch",
            "is_admin": True,
            "register_permissions_on_base_uris": [],
            "search_permissions_on_base_uris": [],
        },
        {
            "username": "dopey",
            "is_admin": False,
            "register_permissions_on_base_uris": [],
            "search_permissions_on_base_uris": [],
        },
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

    # Check for sorted user listing

    response_descending = get_users(sort_fields=["username"], sort_order=[DESCENDING])

    logger.debug("Response Descending:")
    _log_nested_dict(logger.debug, response_descending)

    compares_response_descending = _compare(
        response_descending,
        EXPECTED_DEFAULT_DESCENDING_USER_RESPONSE,
        EXPECTED_DEFAULT_DESCENDING_USER_RESPONSE_IMMUTABLE_MARKER
    )

    assert compares_response_descending

    response_ascending = get_users(sort_fields=["username"], sort_order=[ASCENDING])

    logger.debug("Response Ascending:")
    _log_nested_dict(logger.debug, response_ascending)

    compares_response_ascending = _compare(
        response_ascending,
        EXPECTED_DEFAULT_ASCENDING_USER_RESPONSE,
        EXPECTED_DEFAULT_ASCENDING_USER_RESPONSE_IMMUTABLE_MARKER
    )

    assert compares_response_ascending

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


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_summary():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_summary

    logger = logging.getLogger(__name__)

    response = get_summary(username="testuser")
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_SUMMARY_RESPONSE,
        EXPECTED_DEFAULT_SUMMARY_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_me():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_me

    logger = logging.getLogger(__name__)

    response = get_me()
    assert response is not None

    logger.debug("Response:")

    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_ME_RESPONSE,
        EXPECTED_DEFAULT_ME_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_my_summary():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_my_summary

    logger = logging.getLogger(__name__)

    response = get_my_summary()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_MY_SUMMARY_RESPONSE,
        EXPECTED_DEFAULT_MY_SUMMARY_IMMUTABLE_MARKER,
    )

    assert compares
