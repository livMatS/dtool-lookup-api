"""Test synchronous lookup api."""

import logging
import pytest

from utils import _log_nested_dict, _compare
from metadata import (
    EXPECTED_DEFAULT_ALL_RESPONSE, EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_AGGREGATION, EXPECTED_DEFAULT_AGGREGATION_RESPONSE, EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER,
    EXPECTED_CONFIG_RESPONSE, EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_LOOKUP_UUID, EXPECTED_DEFAULT_LOOKUP_RESPONSE, EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_MANIFEST_URI, EXPECTED_DEFAULT_MANIFEST_RESPONSE, EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_QUERY, EXPECTED_DEFAULT_QUERY_RESPONSE, EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_README_URI, EXPECTED_DEFAULT_README_RESPONSE, EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER,
    DEFAULT_SEARCH_TEXT, EXPECTED_DEFAULT_SEARCH_RESPONSE, EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER,
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

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_SEARCH_RESPONSE,
        EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares
