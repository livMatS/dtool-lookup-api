"""Test synchronous lookup api base URI and permissions management."""

import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

# permission info
DEFAULT_PERMISSION_INFO_BASE_URI = 'smb://test-share'
EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE = {
    'base_uri': 'smb://test-share',
    'users_with_register_permissions': [],
    'users_with_search_permissions': ['testuser']
}
EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE)


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_get_base_uri():
    """Will send a permission info request to the server."""
    from dtool_lookup_api.synchronous import get_base_uri

    logger = logging.getLogger(__name__)

    response = get_base_uri(DEFAULT_PERMISSION_INFO_BASE_URI)
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