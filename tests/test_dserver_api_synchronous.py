"""Test synchronous lookup api."""

import logging
import pytest
import yaml

from utils import _log_nested_dict, _compare, NoDatesSafeLoader, _make_marker


# all

ALL_METADATA = sorted([
    {
        'base_uri': 's3://test-bucket',
        'created_at': 1604860720.736,
        'creator_username': 'jotelha',
        'dtoolcore_version': '3.17.0',
        'frozen_at': 1637950453.869,
        'name': 'simple_test_dataset',
        'tags': [],
        'type': 'dataset',
        'uri': 's3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675',
        'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'
    },
    {
        'base_uri': 'smb://test-share',
        'created_at': 1604860720.736,
        'creator_username': 'jotelha',
        'dtoolcore_version': '3.17.0',
        'frozen_at': 1637950390.648,
        'name': 'simple_test_dataset',
        'tags': [],
        'type': 'dataset',
        'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
        'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'
    }
], key=lambda r: r['uri'])

ALL_METADTA_IMMUTABLE_MARKER = _make_marker(ALL_METADATA)
for dataset in ALL_METADTA_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "dtoolcore_version": False,
            "frozen_at": False,
        }
    )

EXPECTED_DEFAULT_ALL_RESPONSE = [
    {
        'base_uri': 'smb://test-share',
        'created_at': 1604860720.736269,
        'creator_username': 'jotelha',
        'frozen_at': 1604921621.719575,
        'name': 'simple_test_dataset',
        'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
        'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'
    },
    {
        'base_uri': 's3://test-bucket',
        'created_at': 1604860720.736269,
        'creator_username': 'jotelha',
        'frozen_at': 1637950453.869,
        'name': 'simple_test_dataset',
        'uri': 's3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675',
        'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'
    }
]

EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_ALL_RESPONSE)
for dataset in EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "frozen_at": False,
        }
    )

# aggregate

DEFAULT_AGGREGATION = [
    {
        '$match': {
            'base_uri': 'smb://test-share',
            'name': {'$regex': 'test'},
        }
    }, {
        '$count': "matches"
    }
]

EXPECTED_DEFAULT_AGGREGATION_RESPONSE = [{'matches': 1}]
EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_AGGREGATION_RESPONSE)

# lookup

DEFAULT_LOOKUP_UUID = "1a1f9fad-8589-413e-9602-5bbd66bfe675"
EXPECTED_DEFAULT_LOOKUP_RESPONSE = sorted([
    {
        'base_uri': 's3://test-bucket',
        'created_at': 1604860720.736269,
        'creator_username': 'jotelha',
        'frozen_at': 1604864525.691079,
        'name': 'simple_test_dataset',
        'uri': 's3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675',
        'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'
    }, {
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604921621.719575,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675"
    }
], key=lambda r: r["uri"])
EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_LOOKUP_RESPONSE)
for dataset in EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "frozen_at": False,
        }
    )

# query

DEFAULT_QUERY = {
    'base_uri': 's3://test-bucket',
    'uuid': {'$regex': '1a1f9fad-.*-5bbd66bfe675'},
    'name': {'$regex': 'test'},
}
EXPECTED_DEFAULT_QUERY_RESPONSE = [ALL_METADATA[0]]
EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER = [ALL_METADTA_IMMUTABLE_MARKER[0]]

# search

DEFAULT_SEARCH_TEXT = "simple_test_dataset"
EXPECTED_DEFAULT_SEARCH_RESPONSE = EXPECTED_DEFAULT_LOOKUP_RESPONSE
EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER = EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER

PAGINATION_PARAMETERS = {
        "keyword": "test",
        "page_number": 1,
        "page_size": 10,
        "pagination": {}
    }

# dataset entry retrieval

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
def test_default_get_datasets_by_uuid():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_datasets_by_uuid

    logger = logging.getLogger(__name__)

    response = get_datasets_by_uuid(DEFAULT_LOOKUP_UUID)
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
