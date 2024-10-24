import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

# config

EXPECTED_CONFIG_RESPONSE = {
    # dependency graph plugin
    "dependency_keys": [
        "readme.derived_from.uuid",
        "annotations.source_dataset_uuid"
    ],
    "dynamic_dependency_keys": True,
    "enable_dependency_view": True,
    "force_rebuild_dependency_view": False,
    "mongo_dependency_view_bookkeeping": "dep_views",
    "mongo_dependency_view_cache_size": 10,
    "mongo_dependency_view_prefix": "dep:",
    # direct mongo plugin
    "allow_direct_aggregation": True,
    "allow_direct_query": True,
    # other
    "jsonify_prettyprint_regular": True,
    "jwt_algorithm": "RS256",
    "jwt_header_name": "Authorization",
    "jwt_header_type": "Bearer",
    "jwt_public_key": "",
    "jwt_token_location": "headers",
    "sqlalchemy_track_modifications": False,
}

EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_CONFIG_RESPONSE)
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["jwt_public_key"] = False
# EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["dserver_direct_mongo_plugin"]["allow_direct_aggregation"] = False


# version info

EXPECTED_DEFAULT_VERSIONS_RESPONSE = {
    "dservercore": "0.17.2",
    "dserver_dependency_graph_plugin": "0.1.6.dev24",
    "dserver_direct_mongo_plugin": "0.1.5.dev35",
    "dserver_notification_plugin": "0.2.3.dev19",
    "dserver_retrieve_plugin_mongo": "0.1.0",
    "dserver_search_plugin_mongo": "0.1.0"
}


EXPECTED_DEFAULT_VERSIONS_RESPONSE_IMMUTABLE_MARKER = {
    "dservercore": False,
    "dserver_dependency_graph_plugin": False,
    "dserver_direct_mongo_plugin": False,
    "dserver_notification_plugin": False,
    "dserver_retrieve_plugin_mongo": False,
    "dserver_search_plugin_mongo": False,
}


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_get_config():
    """Will send a request for configuration info to the server."""
    from dtool_lookup_api.synchronous import get_config

    logger = logging.getLogger(__name__)

    response = get_config()
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
def test_get_versions():
    """Will send a request for versions to the server."""
    from dtool_lookup_api.synchronous import get_versions

    logger = logging.getLogger(__name__)

    response = get_versions()
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_VERSIONS_RESPONSE,
        EXPECTED_DEFAULT_VERSIONS_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares
