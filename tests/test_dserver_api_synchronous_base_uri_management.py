"""Test synchronous lookup api base URI and permissions management."""

import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

ASCENDING = 1
DESCENDING = -1

DEFAULT_BASE_URI = "s3://test-bucket"

EXPECTED_DEFAULT_BASE_URI_RESPONSE = {
    "base_uri": "s3://test-bucket",
    "users_with_register_permissions": [],
    "users_with_search_permissions": ["testuser"],
}

EXPECTED_DEFAULT_BASE_URI_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_BASE_URI_RESPONSE
)

# base_uris

EXPECTED_DEFAULT_BASE_URIS_RESPONSE = [
    {"base_uri": "s3://test-bucket"},
    {"base_uri": "smb://test-share"},
]

EXPECTED_DEFAULT_BASE_URIS_DESCENDING_RESPONSE = [
    {"base_uri": "smb://test-share"},
    {"base_uri": "s3://test-bucket"},
]

EXPECTED_DEFAULT_BASE_URIS_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_BASE_URIS_RESPONSE
)


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_base_uri():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_base_uri

    logger = logging.getLogger(__name__)

    response = get_base_uri(DEFAULT_BASE_URI)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_BASE_URI_RESPONSE,
        EXPECTED_DEFAULT_BASE_URI_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_base_uris():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_base_uris

    logger = logging.getLogger(__name__)
    response = get_base_uris()
    assert response is not None

    # Checking for descending order response

    response_2 = get_base_uris(sort_fields=["base_uri"], sort_order=[DESCENDING])
    assert response_2 == EXPECTED_DEFAULT_BASE_URIS_DESCENDING_RESPONSE

    # Checking for ascending  order response
    response_3 = get_base_uris(sort_fields=["base_uri"], sort_order=[ASCENDING])
    assert response_3 == EXPECTED_DEFAULT_BASE_URIS_RESPONSE

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_BASE_URIS_RESPONSE,
        EXPECTED_DEFAULT_BASE_URIS_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_register_base_uri():
    """Test the registration of base URIs."""
    from dtool_lookup_api.synchronous import (
        get_base_uri,
        register_base_uri,
        delete_base_uri,
    )

    base_uris = [
        {
            "base_uri": "s3://test_uri_1",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        },
        {
            "base_uri": "smb://test_uri_2",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        },
    ]

    expected_responses = [
        {
            "base_uri": "s3://test_uri_1",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        },
        {
            "base_uri": "smb://test_uri_2",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        },
    ]

    # Ensure base URIs do not yet exist
    for base_uri in base_uris:
        response = get_base_uri(base_uri["base_uri"])
        assert "code" in response and response["code"] == 404

    # Register base URIs
    for base_uri in base_uris:
        response = register_base_uri(**base_uri)
        assert response == True

    # Ensure base URIs exist
    for base_uri, expected_response in zip(base_uris, expected_responses):
        response = get_base_uri(base_uri["base_uri"])
        assert response == expected_response

    # Ensure idempotent behavior
    for base_uri in base_uris:
        response = register_base_uri(**base_uri)
        assert response == True

    # Ensure base URIs still exist after re-registration
    for base_uri, expected_response in zip(base_uris, expected_responses):
        response = get_base_uri(base_uri["base_uri"])
        assert response == expected_response

    # Delete base URIs
    for base_uri in base_uris:
        response = delete_base_uri(base_uri["base_uri"])
        assert response == True

    # Ensure base URIs don't exist anymore
    for base_uri in base_uris:
        response = get_base_uri(base_uri["base_uri"])
        assert "code" in response and response["code"] == 404

    # TODO: Check for the existence of registered base URIs on the server
