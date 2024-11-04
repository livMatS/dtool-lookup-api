"""Test synchronous lookup api."""

import logging
import pytest
import yaml
from utils import _log_nested_dict, _compare, _make_marker

ASCENDING = 1
DESCENDING = -1

ALL_METADATA = sorted(
    [
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
        {
            "base_uri": "smb://test-share",
            "created_at": 1604860720.736,
            "creator_username": "jotelha",
            "dtoolcore_version": "3.17.0",
            "frozen_at": 1637950390.648,
            "name": "simple_test_dataset",
            "tags": [],
            "type": "dataset",
            "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
            "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        },
    ],
    key=lambda r: r["uri"],
)

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
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604921621.719575,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    },
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1637950453.869,
        "name": "simple_test_dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    },
]

EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_ALL_RESPONSE
)
for dataset in EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "frozen_at": False,
        }
    )

# lookup

DEFAULT_LOOKUP_UUID = "1a1f9fad-8589-413e-9602-5bbd66bfe675"
EXPECTED_DEFAULT_LOOKUP_RESPONSE = sorted(
    [
        {
            "base_uri": "s3://test-bucket",
            "created_at": 1604860720.736269,
            "creator_username": "jotelha",
            "frozen_at": 1604864525.691079,
            "name": "simple_test_dataset",
            "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
            "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        },
        {
            "base_uri": "smb://test-share",
            "created_at": 1604860720.736269,
            "creator_username": "jotelha",
            "frozen_at": 1604921621.719575,
            "name": "simple_test_dataset",
            "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
            "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        },
    ],
    key=lambda r: r["uri"],
)
EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_LOOKUP_RESPONSE
)
for dataset in EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER:
    dataset.update(
        {
            "created_at": False,
            "frozen_at": False,
        }
    )

EXPECTED_DEFAULT_LOOKUP_RESPONSE_DESCENDING_BASE_URI = [
    {
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691079,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "number_of_items": 1,
        "size_in_bytes": 17,
    },
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691079,
        "name": "simple_test_dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "number_of_items": 1,
        "size_in_bytes": 17,
    },
]

EXPECTED_DEFAULT_LOOKUP_RESPONSE_DESCENDING_BASE_URI_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_LOOKUP_RESPONSE_DESCENDING_BASE_URI
)

EXPECTED_DEFAULT_LOOKUP_RESPONSE_ASCENDING_BASE_URI = [
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691079,
        "name": "simple_test_dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "number_of_items": 1,
        "size_in_bytes": 17,
    },
    {
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691079,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "number_of_items": 1,
        "size_in_bytes": 17,
    },
]

EXPECTED_DEFAULT_LOOKUP_RESPONSE_ASCENDING_BASE_URI_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_LOOKUP_RESPONSE_ASCENDING_BASE_URI
)

# dataset
DEFAULT_DATASET = "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675"
EXPECTED_DEFAULT_DATASET_RESPONSE = {
    "base_uri": "s3://test-bucket",
    "created_at": 1604860720.736269,
    "creator_username": "jotelha",
    "frozen_at": 1604864525.691079,
    "name": "simple_test_dataset",
    "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
    "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
}
EXPECTED_DEFAULT_DATASET_RESPONSE_IMMUTABLE_MARKER = (
    EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER[0]
)


# datasets
DEFAULT_DATASETS_LOOKUP_UUID = "1a1f9fad-8589-413e-9602-5bbd66bfe675"

EXPECTED_DEFAULT_DATASETS_RESPONSE = [
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691,
        "name": "simple_test_dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    },
    {
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    },
]

EXPECTED_DEFAULT_DATASETS_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_DATASETS_RESPONSE
)

EXPECTED_DEFAULT_BASE_URI_LOOKUP_RESPONSE = [
    {
        "base_uri": "s3://test-bucket",
        "created_at": 1604860720.736,
        "creator_username": "jotelha",
        "frozen_at": 1604864525.691,
        "name": "simple_test_dataset",
        "uri": "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675",
    }
]
EXPECTED_DEFAULT_BASE_URI_LOOKUP_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_BASE_URI_LOOKUP_RESPONSE
)

EXPECTED_DEFAULT_DESCENDING_NAME_SORTING_RESPONSE = [
    {
        "base_uri": "s3://testsorting1",
        "created_at": 1604860720.736,
        "creator_username": "testuser",
        "frozen_at": 1604864525.691,
        "name": "b",
        "uri": "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe679",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe679",
        "number_of_items": 0,
        "size_in_bytes": 0,
    },
    {
        "base_uri": "s3://testsorting1",
        "created_at": 1604860720.736,
        "creator_username": "testuser",
        "frozen_at": 1604864525.691,
        "name": "a",
        "uri": "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe678",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe678",
        "number_of_items": 0,
        "size_in_bytes": 0,
    },
]

EXPECTED_DEFAULT_DESCENDING_NAME_SORTING_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_DESCENDING_NAME_SORTING_RESPONSE)

EXPECTED_DEFAULT_ASCENDING_NAME_SORTING_RESPONSE = [
    {
        "base_uri": "s3://testsorting1",
        "created_at": 1604860720.736,
        "creator_username": "testuser",
        "frozen_at": 1604864525.691,
        "name": "a",
        "uri": "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe678",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe678",
        "number_of_items": 0,
        "size_in_bytes": 0,
    },
    {
        "base_uri": "s3://testsorting1",
        "created_at": 1604860720.736,
        "creator_username": "testuser",
        "frozen_at": 1604864525.691,
        "name": "b",
        "uri": "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe679",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe679",
        "number_of_items": 0,
        "size_in_bytes": 0,
    },
]

EXPECTED_DEFAULT_ASCENDING_NAME_SORTING_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_ASCENDING_NAME_SORTING_RESPONSE)

# manifest

EXPECTED_DEFAULT_MANIFEST_URI = EXPECTED_DEFAULT_ALL_RESPONSE[1]["uri"]

EXPECTED_DEFAULT_MANIFEST_RESPONSE = {
    "dtoolcore_version": "3.18.3",
    "hash_function": "md5sum_hexdigest",
    "items": {
        "eb58eb70ebcddf630feeea28834f5256c207edfd": {
            "hash": "2f7d9c3e0cfd47e8fcab0c12447b2bf0",
            "relpath": "simple_text_file.txt",
            "size_in_bytes": 17,
            "utc_timestamp": 1720529941.0,
        }
    },
}

EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_MANIFEST_RESPONSE
)

EXPECTED_DEFAULT_UPDATED_MANIFEST_RESPONSE = {
    "dtoolcore_version": "3.18.3",
    "hash_function": "md5sum_hexdigest",
    "items": {
        "eb58eb70ebcddf630feeea28834f5256c207edfd": {
            "hash": "2f7d9c3e0cfd47e8fcab0c12447b2bf0",
            "relpath": "simple_text_file.txt",
            "size_in_bytes": 17,
            "utc_timestamp": 1729081495.0,
        }
    },
}
EXPECTED_DEFAULT_UPDATED_MANIFEST_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_UPDATED_MANIFEST_RESPONSE
)

# user

EXPECTED_DEFAULT_USER_RESPONSE = [{"is_admin": True, "username": "testuser"}]
EXPECTED_DEFAULT_USER_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_USER_RESPONSE
)

# search

DEFAULT_SEARCH_TEXT = "simple_test_dataset"
EXPECTED_DEFAULT_SEARCH_RESPONSE = EXPECTED_DEFAULT_LOOKUP_RESPONSE
EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER = (
    EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER
)

PAGINATION_PARAMETERS = {
    "free_text": "test",
    "page_number": 1,
    "page_size": 10,
    "pagination": {},
}

# register dataset

EXPECTED_DEFAULT_README_RESPONSE = yaml.dump(
    {
        "creation_date": "2020-11-08",
        "description": "testing description",
        "expiration_date": "2022-11-08",
        "funders": [
            {
                "code": "testing_code",
                "organization": "testing_organization",
                "program": "testing_program",
            }
        ],
        "owners": [
            {
                "email": "testing@test.edu",
                "name": "Testing User",
                "orcid": "testing_orcid",
                "username": "testing_user",
            }
        ],
        "project": "testing project",
    },
    indent=4,
    default_flow_style=False,
    sort_keys=False,
)

EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_README_RESPONSE
)

EXPECTED_DEFAULT_UPDATED_README_RESPONSE = yaml.dump(
    {
        "creation_date": "2020-11-08",
        "description": "updated_readme",
        "expiration_date": "2022-11-08",
        "funders": [
            {
                "code": "testing_code",
                "organization": "testing_organization",
                "program": "testing_program",
            }
        ],
        "owners": [
            {
                "email": "testing@test.edu",
                "name": "Testing User",
                "orcid": "testing_orcid",
                "username": "testing_user",
            }
        ],
        "project": "testing project",
    },
    indent=4,
    default_flow_style=False,
    sort_keys=False,
)
EXPECTED_DEFAULT_UPDATED_README_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_UPDATED_README_RESPONSE)

# dataset entry retrieval


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_datasets_by_uuid():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_datasets_by_uuid

    logger = logging.getLogger(__name__)

    response = get_datasets_by_uuid(DEFAULT_LOOKUP_UUID)
    assert response is not None

    response_2 = get_datasets_by_uuid(
        DEFAULT_LOOKUP_UUID, sort_fields=["base_uri"], sort_order=[DESCENDING]
    )

    compares_2 = _compare(
        response_2,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_DESCENDING_BASE_URI,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_DESCENDING_BASE_URI_IMMUTABLE_MARKER,
    )

    response_3 = get_datasets_by_uuid(
        DEFAULT_LOOKUP_UUID, sort_fields=["base_uri"], sort_order=[ASCENDING]
    )

    compares_3 = _compare(
        response_3,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_ASCENDING_BASE_URI,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_ASCENDING_BASE_URI_IMMUTABLE_MARKER,
    )

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    logger.debug("Response 2:")
    _log_nested_dict(logger.debug, response_2)

    logger.debug("Response 3:")
    _log_nested_dict(logger.debug, response_3)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE,
        EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares
    assert compares_2
    assert compares_3


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_dataset():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_dataset

    logger = logging.getLogger(__name__)

    response = get_dataset(DEFAULT_DATASET)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_DATASET_RESPONSE,
        EXPECTED_DEFAULT_DATASET_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_datasets():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import (
        get_datasets,
        register_dataset,
        register_base_uri,
        delete_dataset,
        delete_base_uri,
    )

    logger = logging.getLogger(__name__)

    response = get_datasets(DEFAULT_DATASETS_LOOKUP_UUID)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_DATASETS_RESPONSE,
        EXPECTED_DEFAULT_DATASETS_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares

    response2 = get_datasets(creator_usernames=["jotelha"])

    logger.debug("Response 2:")
    _log_nested_dict(logger.debug, response2)

    assert len(response2) == 10

    response3 = get_datasets(base_uris=["s3://test-bucket"])

    logger.debug("Response 3:")
    _log_nested_dict(logger.debug, response3)

    compares3 = _compare(
        response3,
        EXPECTED_DEFAULT_BASE_URI_LOOKUP_RESPONSE,
        EXPECTED_DEFAULT_BASE_URI_LOOKUP_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares3

    response4 = get_datasets(tags=["first-half", "second-third"])

    logger.debug("Response 4:")
    _log_nested_dict(logger.debug, response4)

    assert len(response4) == 10

    base_uris = [
        {
            "base_uri": "s3://testsorting1",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        }
    ]

    # Register a new base_uri
    for base_uri in base_uris:
        response = register_base_uri(**base_uri)
        assert response == True

    # Register dataset
    response = register_dataset(
        name="a",
        uuid="1a1f9fad-8589-413e-9602-5bbd66bfe678",
        base_uri="s3://testsorting1",
        type="dataset",
        uri="s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe678",
        manifest=EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        readme=EXPECTED_DEFAULT_README_RESPONSE,
        creator_username="testuser",
        frozen_at="1604864525.691",
        created_at="1604860720.736269",
        annotations={},
        tags=[""],
        number_of_items=0,
        size_in_bytes=0,
    )
    assert response == True

    response_11 = register_dataset(
        name="b",
        uuid="1a1f9fad-8589-413e-9602-5bbd66bfe679",
        base_uri="s3://testsorting1",
        type="dataset",
        uri="s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe679",
        manifest=EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        readme=EXPECTED_DEFAULT_README_RESPONSE,
        creator_username="testuser",
        frozen_at="1604864525.691",
        created_at="1604860720.736269",
        annotations={},
        tags=[""],
        number_of_items=0,
        size_in_bytes=0,
    )
    assert response_11 == True

    # Checking for sorting order descending name
    response_5 = get_datasets(
        base_uris=["s3://testsorting1"], sort_fields=["name"], sort_order=[DESCENDING]
    )

    logger.debug("Response 5:")
    _log_nested_dict(logger.debug, response_5)

    compares_response_5 = _compare(
        response_5,
        EXPECTED_DEFAULT_DESCENDING_NAME_SORTING_RESPONSE,
        EXPECTED_DEFAULT_DESCENDING_NAME_SORTING_RESPONSE_IMMUTABLE_MARKER
    )

    assert compares_response_5

    # Checking for sorting order ascending name
    response_6 = get_datasets(
        base_uris=["s3://testsorting1"], sort_fields=["name"], sort_order=[ASCENDING]
    )

    logger.debug("Response 6:")
    _log_nested_dict(logger.debug, response_6)

    compares_response_6 = _compare(
        response_6,
        EXPECTED_DEFAULT_ASCENDING_NAME_SORTING_RESPONSE,
        EXPECTED_DEFAULT_ASCENDING_NAME_SORTING_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares_response_6

    # Delete dataset
    response_2 = delete_dataset(
        "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe678"
    )
    assert response_2 == True

    response_3 = delete_dataset(
        "s3://testsorting1/1a1f9fad-8589-413e-9602-5bbd66bfe679"
    )
    assert response_3 == True

    # Delete base_uri
    for base_uri in base_uris:
        response = delete_base_uri(base_uri["base_uri"])
        assert response == True


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
        sorted(response, key=lambda r: r["uri"]),
        EXPECTED_DEFAULT_SEARCH_RESPONSE,
        EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_pagination():

    from dtool_lookup_api.synchronous import get_datasets

    # Using ** to unpack dictionary values as function arguments
    _ = get_datasets(**PAGINATION_PARAMETERS)

    # Validate that pagination dict was populated
    pagination = PAGINATION_PARAMETERS["pagination"]
    assert pagination

    # Here, we only check the keys that are present in the pagination dictionary
    if "total" in pagination:
        assert pagination["total"] >= 0

    if "page" in pagination and "total_pages" in pagination:
        # Ensure current page is less than or equal to total pages
        assert pagination["page"] <= pagination["total_pages"]

        # If on the first page, ensure that `first_page` is equivalent to the current page
        if pagination["page"] == 1 and "first_page" in pagination:
            assert pagination["first_page"] == 1

        # If on the last page, ensure there isn't a next_page and that `last_page` is equivalent to the current page
        if pagination["page"] == pagination["total_pages"]:
            assert "next_page" not in pagination
            if "last_page" in pagination:
                assert pagination["last_page"] == pagination["page"]

    # Check if `next_page` makes sense, given the total pages and the current page
    if "next_page" in pagination and "total_pages" in pagination:
        assert pagination["next_page"] <= pagination["total_pages"]
        assert pagination["next_page"] > pagination.get("page", 0)

    # Print out keys that were not present for debugging or information
    expected_keys = [
        "total",
        "total_pages",
        "first_page",
        "last_page",
        "page",
        "next_page",
    ]
    missing_keys = [key for key in expected_keys if key not in pagination]
    for key in missing_keys:
        print(f"Optional key {key} is not present in pagination")


# TODO: use _compare function with comparison markers as with other tests to
# validate each nested response, i.e.
#     logger.debug("Response:")
#     _log_nested_dict(logger.debug, response)
#
#     compares = _compare(
#         response,
#         EXPECTED_DEFAULT_MY_SUMMARY_RESPONSE,
#         EXPECTED_DEFAULT_MY_SUMMARY_IMMUTABLE_MARKER,
#     )
@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_register_dataset():
    """Test the registration of base URIs."""
    from dtool_lookup_api.synchronous import (
        register_base_uri,
        register_dataset,
        delete_base_uri,
        delete_dataset,
        get_dataset,
        get_datasets,
        get_manifest,
        get_readme,
        get_tags,
        get_annotations,
    )

    logger = logging.getLogger(__name__)

    base_uris = [
        {
            "base_uri": "s3://test-1",
            "users_with_search_permissions": ["testuser"],
            "users_with_register_permissions": ["testuser"],
        }
    ]

    expected_result = [
        {
            "base_uri": "s3://test-1",
            "created_at": 1604860720.736,
            "creator_username": "testuser",
            "frozen_at": 1604864525.691,
            "name": "testuser",
            "uri": "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
            "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe677",
            "number_of_items": 0,
            "size_in_bytes": 0,
        }
    ]

    expected_result_immutable_marker = _make_marker(expected_result)

    expected_updated_result = [
        {
            "base_uri": "s3://test-1",
            "created_at": 2604860720.736,
            "creator_username": "another-testuser",
            "frozen_at": 2604864525.691,
            "name": "updated_test_dataset",
            "uri": "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
            "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe677",
            "number_of_items": 2,
            "size_in_bytes": 3,
        }
    ]

    expected_updated_result_make_marker = _make_marker(expected_updated_result)
    expected_updated_result_get_dataset_immutable_marker = _make_marker(
        expected_updated_result[0]
    )

    # Delete dataset (in case it exists already)
    delete_dataset("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")
    delete_base_uri("s3://test-1")

    # Ensure dataset do not yet exist
    # get datasets returns empty list even if base URI does not exist
    response_get_datasets = get_datasets(base_uris=["s3://test-1"])
    assert len(response_get_datasets) == 0

    response_get_dataset = get_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    assert (
        "code" in response_get_dataset and response_get_dataset["code"] == 403
    )  # forbidden

    # Register a new base_uri
    for base_uri in base_uris:
        response = register_base_uri(**base_uri)
        assert response == True

    # Register dataset
    response_register_dataset = register_dataset(
        name="testuser",
        uuid="1a1f9fad-8589-413e-9602-5bbd66bfe677",
        base_uri="s3://test-1",
        type="dataset",
        uri="s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
        manifest=EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        readme=EXPECTED_DEFAULT_README_RESPONSE,
        creator_username="testuser",
        frozen_at="1604864525.691",
        created_at="1604860720.736",
        annotations={"test-annotation": "test-value"},
        tags=["test-tag1"],
        number_of_items=0,
        size_in_bytes=0,
    )
    assert response_register_dataset == True

    #  Ensure dataset exist
    response_get_datasets = get_datasets(base_uris=["s3://test-1"])
    logger.debug("Response get datasets:")
    _log_nested_dict(logger.debug, response_get_datasets)

    compares_response_get_datasets = _compare(
        response_get_datasets,
        expected_result,
        expected_result_immutable_marker
    )

    assert compares_response_get_datasets

    response_get_dataset = get_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    logger.debug("Response get dataset:")
    _log_nested_dict(logger.debug, response_get_dataset)

    compares_response_get_dataset = _compare(
        response_get_dataset,
        expected_result[0],
        expected_updated_result_get_dataset_immutable_marker
    )

    assert compares_response_get_dataset

    response_get_manifest = get_manifest(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )

    logger.debug("Response get manifest:")
    _log_nested_dict(logger.debug, response_get_manifest)

    compares_response_get_manifest = _compare(
        response_get_manifest,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER
    )

    assert compares_response_get_manifest

    response_get_readme = get_readme("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")

    logger.debug("Response get Readme:")
    _log_nested_dict(logger.debug, response_get_readme)

    compares_response_get_read_me = _compare(
        response_get_readme,
        EXPECTED_DEFAULT_README_RESPONSE,
        EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER
    )

    assert compares_response_get_read_me

    response_get_tags = get_tags("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")
    assert response_get_tags == ["test-tag1"]

    response_get_annotations = get_annotations(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    assert response_get_annotations == {"test-annotation": "test-value"}

    #  Ensure idempotent behavior
    response_register_dataset = register_dataset(
        name="updated_test_dataset",
        uuid="1a1f9fad-8589-413e-9602-5bbd66bfe677",
        base_uri="s3://test-1",
        type="dataset",
        uri="s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
        manifest=EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        readme=EXPECTED_DEFAULT_README_RESPONSE,
        creator_username="another-testuser",
        frozen_at="2604864525.691",
        created_at="2604860720.736",
        annotations={
            "test-annotation": "test-value",
            "another-test-annotation": "another-test-value",
        },
        tags=["Updated_tag_1", "Updated_tag_2"],
        number_of_items=2,
        size_in_bytes=3,
    )
    assert response_register_dataset == True

    # Ensure dataset has been updated
    response_get_datasets = get_datasets(base_uris=["s3://test-1"])
    compares_get_datasets = _compare(
        response_get_datasets,
        expected_updated_result,
        expected_updated_result_make_marker,
    )
    assert compares_get_datasets
    # ATTENTION: get_datasets returns
    # [{'base_uri': 's3://test-1',
    #   'created_at': 1604860720.736,
    #   'creator_username': 'testuser',
    #   'frozen_at': 1604864525.691,
    #   'name': 'updated_test_dataset',
    #   'number_of_items': 2,
    #   'size_in_bytes': 3,
    #   'uri': 's3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677',
    #   'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe677'}]
    # with timestamps of .3 precision ...

    response_get_dataset = get_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    logger.debug("Response get dataset:")
    _log_nested_dict(logger.debug, response_get_dataset)

    compares_get_dataset = _compare(
        response_get_dataset,
        expected_updated_result[0],
        expected_updated_result_get_dataset_immutable_marker,
    )
    assert compares_get_dataset

    # ... while get_dataset return
    # {'base_uri': 's3://test-1',
    #  'created_at': 1604860720.736269,
    #  'creator_username': 'testuser',
    #  'frozen_at': 1604864525.691,
    #  'name': 'updated_test_dataset',
    #  'number_of_items': 2,
    #  'size_in_bytes': 3,
    #  'uri': 's3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677',
    #  'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe677'}
    # with timestamps of .6 precision.
    # The tests hence only work with .3 precision in the first place

    # also test modified metadata
    response_get_manifest = get_manifest(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )

    logger.debug("Response get manifest:")
    _log_nested_dict(logger.debug, response_get_manifest)

    compares_get_manifest = _compare(
        response_get_manifest,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares_get_manifest

    response_get_readme = get_readme("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")

    logger.debug("Response get readme:")
    _log_nested_dict(logger.debug, response_get_readme)

    compares_get_readme = _compare(
        response_get_readme,
        EXPECTED_DEFAULT_README_RESPONSE,
        EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER,
    )
    assert compares_get_readme

    # Test against modified manifest and readme

    updated_manifest = get_manifest(
        "s3://test-bucket/1a1f9fad-8589-413e-9602-5bbd66bfe675"
    )

    updated_readme = EXPECTED_DEFAULT_UPDATED_README_RESPONSE

    response_modified_mainfest_readme = register_dataset(
        name="updated_test_dataset",
        uuid="1a1f9fad-8589-413e-9602-5bbd66bfe677",
        base_uri="s3://test-1",
        type="dataset",
        uri="s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677",
        manifest=updated_manifest,  # modified manifest
        readme=updated_readme,  # modified readme content
        creator_username="another-testuser",
        frozen_at="2604864525.691",
        created_at="2604860720.736",
        annotations={"test-annotation": "test-value", "another-test-annotation": "another-test-value"},
        tags=["Updated_tag_1", "Updated_tag_2"],
        number_of_items=2,
        size_in_bytes=3,
    )
    assert response_modified_mainfest_readme == True

    response_get_manifest_updated = get_manifest(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )

    logger.debug("Response get updated manifest:")
    _log_nested_dict(logger.debug, response_get_manifest_updated)

    compares_get_manifest_updated = _compare(
        response_get_manifest_updated,
        EXPECTED_DEFAULT_UPDATED_MANIFEST_RESPONSE,
        EXPECTED_DEFAULT_UPDATED_MANIFEST_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares_get_manifest_updated

    response_get_readme_updated = get_readme("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")

    logger.debug("Response get updated readme:")
    _log_nested_dict(logger.debug, response_get_readme_updated)

    compares_get_readme_updated = _compare(
        response_get_readme_updated,
        EXPECTED_DEFAULT_UPDATED_README_RESPONSE,
        EXPECTED_DEFAULT_UPDATED_README_RESPONSE_IMMUTABLE_MARKER,
    )

    assert compares_get_readme_updated

    response_get_tags = get_tags("s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677")

    logger.debug("Response get tags:")
    _log_nested_dict(logger.debug, response_get_tags)

    assert set(response_get_tags) == set(["Updated_tag_1", "Updated_tag_2"])

    response_get_annotations = get_annotations(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )

    assert response_get_annotations == {
        "test-annotation": "test-value",
        "another-test-annotation": "another-test-value",
    }

    # Delete dataset
    response_delete_dataset = delete_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    assert response_delete_dataset == True

    # Ensure dataset does not exist anymore in base URI
    # response_get_datasets = get_datasets(base_uris=["s3://test-1"])
    # assert len(response_get_datasets) == 0
    # TODO: this does not work yet, deletion not propagated to search database on server side

    # Dataset does not exist anymore, but user is still allowed to search base URI
    response_get_dataset = get_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    assert (
        "code" in response_get_dataset and response_get_dataset["code"] == 404
    )  # not found

    # Delete base_uri
    for base_uri in base_uris:
        response = delete_base_uri(base_uri["base_uri"])
        assert response == True

    # Ensure dataset does not exist anymore
    response_get_datasets = get_datasets(base_uris=["s3://test-1"])
    assert len(response_get_datasets) == 0

    # Dataset does not exist anymore, and base URI neither
    response_get_dataset = get_dataset(
        "s3://test-1/1a1f9fad-8589-413e-9602-5bbd66bfe677"
    )
    assert (
        "code" in response_get_dataset and response_get_dataset["code"] == 403
    )  # forbidden

    # TODO: Check for the existence of registered base URIs on the server
