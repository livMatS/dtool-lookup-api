"""Testing metdata"""

from utils import _make_marker

# TODO: right now, the expected metadata content depends on what's to be found within
# https://github.com/jotelha/dtool-lookup-server-container-composition/tree/master/tests/dtool/simple_test_dataset
# That should become independent of the testing framework, ideally by providing our own datasets.

# all

ALL_METADTA = [
    {
        "base_uri": "smb://test-share",
        "created_at": "Sun, 08 Nov 2020 18:38:40 GMT",
        "creator_username": "jotelha",
        "dtoolcore_version": "3.17.0",
        "frozen_at": "Mon, 09 Nov 2020 11:33:41 GMT",
        "name": "simple_test_dataset",
        "tags": [],
        "type": "dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675"
    }
]

ALL_METADTA_IMMUTABLE_MARKER = _make_marker(ALL_METADTA)
ALL_METADTA_IMMUTABLE_MARKER[0].update(
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
    }
]
EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_ALL_RESPONSE)
EXPECTED_DEFAULT_ALL_RESPONSE_IMMUTABLE_MARKER[0].update(
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
EXPECTED_DEFAULT_LOOKUP_RESPONSE = [
    {
        "base_uri": "smb://test-share",
        "created_at": 1604860720.736269,
        "creator_username": "jotelha",
        "frozen_at": 1604921621.719575,
        "name": "simple_test_dataset",
        "uri": "smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675",
        "uuid": "1a1f9fad-8589-413e-9602-5bbd66bfe675"
    }
]
EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_LOOKUP_RESPONSE)
EXPECTED_DEFAULT_LOOKUP_RESPONSE_IMMUTABLE_MARKER[0].update(
    {
        "created_at": False,
        "frozen_at": False,
    }
)

# manifest

# interestingly, different machines returned different time stamps here
# for the same dataset:
# Comparing '1605054830.454785' == '1605027357.284966' -> False
# might that time stamp depend on the actual file creation time on disk?
DEFAULT_MANIFEST_URI = 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675'
EXPECTED_DEFAULT_MANIFEST_RESPONSE = {
    "dtoolcore_version": "3.17.0",
    "hash_function": "md5sum_hexdigest",
    "items": {
        "eb58eb70ebcddf630feeea28834f5256c207edfd": {
            "hash": "2f7d9c3e0cfd47e8fcab0c12447b2bf0",
            "relpath": "simple_text_file.txt",
            "size_in_bytes": 17,
            "utc_timestamp": 1605027357.284966
        }
    }
}
EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_MANIFEST_RESPONSE)
EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER.update(
    {
        "dtoolcore_version": False,
    }
)
EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER["items"]["eb58eb70ebcddf630feeea28834f5256c207edfd"].update(
    {
        "utc_timestamp": False,
    }
)

# query

DEFAULT_QUERY = {
    'base_uri': 'smb://test-share',
    'name': {'$regex': 'test'},
}
EXPECTED_DEFAULT_QUERY_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_QUERY_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER

# readme

DEFAULT_README_URI = 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675'
EXPECTED_DEFAULT_README_RESPONSE = {
    "creation_date": "2020-11-08",
    "description": "testing description",
    "expiration_date": "2022-11-08",
    "funders": [
        {
            "code": "testing_code",
            "organization": "testing_organization",
            "program": "testing_program"
        }
    ],
    "owners": [
        {
            "email": "testing@test.edu",
            "name": "Testing User",
            "orcid": "testing_orcid",
            "username": "testing_user"
        }
    ],
    "project": "testing project"
}

EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_README_RESPONSE)

# search

DEFAULT_SEARCH_TEXT = "test"
EXPECTED_DEFAULT_SEARCH_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_SEARCH_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER

# config

EXPECTED_CONFIG_RESPONSE = {
    "dtool_lookup_server_dependency_graph_plugin": {
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
        "version": "0.1.3"
    },
    "dtool_lookup_server_direct_mongo_plugin": {
        "allow_direct_aggregation": False,
        "allow_direct_query": True,
        "version": "0.1.2"
    },
    "jsonify_prettyprint_regular": True,
    "jwt_algorithm": "RS256",
    "jwt_header_name": "Authorization",
    "jwt_header_type": "Bearer",
    "jwt_public_key": "",
    "jwt_token_location": "headers",
    "sqlalchemy_track_modifications": False,
    "version": "0.15.0"
}

EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_CONFIG_RESPONSE)
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["jwt_public_key"] = False
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["version"] = False
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["dtool_lookup_server_dependency_graph_plugin"]["version"] = False
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["dtool_lookup_server_direct_mongo_plugin"]["version"] = False
EXPECTED_CONFIG_RESPONSE_IMMUTABLE_MARKER["dtool_lookup_server_direct_mongo_plugin"]["allow_direct_aggregation"] = False

EXPECTED_DEFAULT_LIST_USERS_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_LIST_USERS_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER

EXPECTED_DEFAULT_REGISTER_USER_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_REGISTER_USER_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER

EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_PERMISSION_INFO_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER

EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE = ALL_METADTA
EXPECTED_DEFAULT_UPDATE_PERMISSIONS_RESPONSE_IMMUTABLE_MARKER = ALL_METADTA_IMMUTABLE_MARKER
