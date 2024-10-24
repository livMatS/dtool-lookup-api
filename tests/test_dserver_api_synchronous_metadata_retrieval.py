"""Test synchronous lookup api metadata retrieval."""

import logging
import pytest
import yaml

from utils import _log_nested_dict, _compare, NoDatesSafeLoader, _make_marker

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

# tags

DEFAULT_TAGS_URI = 'smb://test-share/10516e27-9655-44ec-b1af-c03d69478fb6'
EXPECTED_DEFAULT_TAGS_RESPONSE = ['first-half']
EXPECTED_DEFAULT_TAGS_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_TAGS_RESPONSE)

# annotations

DEFAULT_ANNOTATIONS_URI = 'smb://test-share/f701af39-b14c-46dc-8959-f1085e46b01b'
EXPECTED_DEFAULT_ANNOTATIONS_RESPONSE = {
    "chunk": "third-quarter",
    "number": "161"
}
EXPECTED_DEFAULT_ANNOTATIONS_RESPONSE_IMMUTABLE_MARKER = _make_marker(EXPECTED_DEFAULT_ANNOTATIONS_RESPONSE)


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_manifest():
    """Test manifest retrieval."""
    from dtool_lookup_api.synchronous import get_manifest

    logger = logging.getLogger(__name__)

    response = get_manifest(DEFAULT_MANIFEST_URI)
    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE,
        EXPECTED_DEFAULT_MANIFEST_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_readme():
    """Test readme retrieval."""
    from dtool_lookup_api.synchronous import get_readme

    logger = logging.getLogger(__name__)

    response = get_readme(DEFAULT_README_URI)
    assert response is not None

    logger.debug("Response:")
    logger.debug(response)

    logger.debug("Parsed:")
    parsed_readme = yaml.load(response, Loader=NoDatesSafeLoader)
    _log_nested_dict(logger.debug, parsed_readme)

    compares = _compare(
        parsed_readme,
        EXPECTED_DEFAULT_README_RESPONSE,
        EXPECTED_DEFAULT_README_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_tags():
    """Test tags retrieval."""
    from dtool_lookup_api.synchronous import get_tags

    logger = logging.getLogger(__name__)

    response = get_tags(DEFAULT_TAGS_URI)
    assert response is not None

    logger.debug("Response:")
    logger.debug(response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_TAGS_RESPONSE,
        EXPECTED_DEFAULT_TAGS_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_annotations():
    """Test tags retrieval."""
    from dtool_lookup_api.synchronous import get_annotations

    logger = logging.getLogger(__name__)

    response = get_annotations(DEFAULT_ANNOTATIONS_URI)
    assert response is not None

    logger.debug("Response:")
    logger.debug(response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_ANNOTATIONS_RESPONSE,
        EXPECTED_DEFAULT_ANNOTATIONS_RESPONSE_IMMUTABLE_MARKER
    )
    assert compares
