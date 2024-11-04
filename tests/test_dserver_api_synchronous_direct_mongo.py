import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

ASCENDING = 1
DESCENDING = -1

# aggregate

DEFAULT_AGGREGATION = [
    {
        "$match": {
            "base_uri": "smb://test-share",
            "name": {"$regex": "test"},
        }
    },
    {"$count": "matches"},
]

EXPECTED_DEFAULT_AGGREGATION_RESPONSE = [{"matches": 1}]
EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_AGGREGATION_RESPONSE
)

# query

DEFAULT_QUERY = {
    "base_uri": "s3://test-bucket",
    "uuid": {"$regex": "1a1f9fad-.*-5bbd66bfe675"},
    "name": {"$regex": "test"},
}
EXPECTED_DEFAULT_QUERY_RESPONSE = [
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736,
        "creator_username": "jotelha",
        "dtoolcore_version": "3.17.0",
        "frozen_at": 1637950453.869,
        "name": "simple_test_dataset",
        "tags": [],
        "type": "dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    },
]
EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_QUERY_RESPONSE)
for dataset in EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "dtoolcore_version": False,
            "frozen_at": False,
        }
    )


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_datasets_by_mongo_aggregation():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_datasets_by_mongo_aggregation

    logger = logging.getLogger(__name__)

    response = get_datasets_by_mongo_aggregation(DEFAULT_AGGREGATION)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_AGGREGATION_RESPONSE,
        EXPECTED_DEFAULT_AGGREGATION_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_datasets_by_mongo_query():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_datasets_by_mongo_query

    logger = logging.getLogger(__name__)

    response = get_datasets_by_mongo_query(query=DEFAULT_QUERY)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    assert len(response) == 1

    compares = _compare(
        response,
        EXPECTED_DEFAULT_QUERY_RESPONSE,
        EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares