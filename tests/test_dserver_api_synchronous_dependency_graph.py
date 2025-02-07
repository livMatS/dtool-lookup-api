import logging
import pytest

from utils import _log_nested_dict, _compare, _make_marker

ASCENDING = 1
DESCENDING = -1

DEFAULT_GET_GRAPH_BY_UUID_UUID = "2a74dfd2-0699-47b9-b8b6-c1356f968aee"

EXPECTED_DEFAULT_GET_GRAPH_BY_UUID_RESPONSE = [
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.786,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.795,
    "name": "2020-12-15-12-53-46-616772-c-15-n-338-m-338-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half",
      "second-third"
    ],
    "type": "dataset",
    "uri": "smb://test-share/09c42267-f6fa-4274-b71b-07d52977cab2",
    "uuid": "09c42267-f6fa-4274-b71b-07d52977cab2"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394345.471,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394345.48,
    "name": "2020-12-15-12-53-46-583537-c-125-n-281-m-281-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "second-third"
    ],
    "type": "dataset",
    "uri": "smb://test-share/09d7bc19-4837-4773-869d-da8c787dd14d",
    "uuid": "09d7bc19-4837-4773-869d-da8c787dd14d"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.025,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.036,
    "name": "2020-12-15-12-53-46-527997-c-075-n-169-m-169-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half"
    ],
    "type": "dataset",
    "uri": "smb://test-share/0f816c68-11a4-4f65-8362-96368559eea7",
    "uuid": "0f816c68-11a4-4f65-8362-96368559eea7"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394345.668,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394345.677,
    "name": "2020-12-15-12-53-46-554144-c-10-n-225-m-225-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "second-third"
    ],
    "type": "dataset",
    "uri": "smb://test-share/1b08d0f6-f299-4e55-b46a-071dfa065e49",
    "uuid": "1b08d0f6-f299-4e55-b46a-071dfa065e49"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.507,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.517,
    "name": "2020-12-15-12-53-46-498999-c-05-n-112-m-112-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half"
    ],
    "type": "dataset",
    "uri": "smb://test-share/2025be08-314f-472f-8e8f-82dc75fdf9c6",
    "uuid": "2025be08-314f-472f-8e8f-82dc75fdf9c6"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394346.127,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394346.136,
    "name": "2020-12-15-12-53-46-641755-c-175-n-394-m-394-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [],
    "type": "dataset",
    "uri": "smb://test-share/2a74dfd2-0699-47b9-b8b6-c1356f968aee",
    "uuid": "2a74dfd2-0699-47b9-b8b6-c1356f968aee"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.237,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.247,
    "name": "2020-12-15-12-53-46-629260-c-15-n-338-m-338-s-hemicylinders-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half"
    ],
    "type": "dataset",
    "uri": "smb://test-share/55b01e60-d270-4908-a7c0-17a8350c6605",
    "uuid": "55b01e60-d270-4908-a7c0-17a8350c6605"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.089,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.099,
    "name": "2020-12-15-12-53-46-474407-c-025-n-56-m-56-s-monolayer-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half"
    ],
    "type": "dataset",
    "uri": "smb://test-share/7941baae-b475-4e54-b815-9478874994df",
    "uuid": "7941baae-b475-4e54-b815-9478874994df"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394344.015,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394344.025,
    "name": "2020-12-15-12-53-46-512103-c-05-n-112-m-112-s-hemicylinders-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "first-half"
    ],
    "type": "dataset",
    "uri": "smb://test-share/804eb317-b9a2-4d4e-9fba-b97ed349c517",
    "uuid": "804eb317-b9a2-4d4e-9fba-b97ed349c517"
  },
  {
    "base_uri": "smb://test-share",
    "created_at": 1681394345.55,
    "creator_username": "jotelha",
    "derived_from": [
      "51490ee3-e130-4514-bfa8-4dc2e9cd0e04"
    ],
    "dtoolcore_version": "3.18.2",
    "frozen_at": 1681394345.559,
    "name": "2020-12-15-12-53-46-486687-c-025-n-56-m-56-s-hemicylinders-substratepassivation",
    "number_of_items": 3,
    "size_in_bytes": 12,
    "tags": [
      "second-third"
    ],
    "type": "dataset",
    "uri": "smb://test-share/a6faaeae-8e05-4d65-96c2-fea208ef8cf9",
    "uuid": "a6faaeae-8e05-4d65-96c2-fea208ef8cf9"
  }
]

EXPECTED_DEFAULT_GET_GRAPH_BY_UUID_IMMUTABLE_MARKER = _make_marker(
    EXPECTED_DEFAULT_GET_GRAPH_BY_UUID_RESPONSE
)


@pytest.mark.usefixtures("dserver", "dtool_config")
def test_default_get_graph_by_uuid():
    """Will send a direct mongo query request to the server."""
    from dtool_lookup_api.synchronous import get_graph_by_uuid

    logger = logging.getLogger(__name__)

    response = get_graph_by_uuid(DEFAULT_GET_GRAPH_BY_UUID_UUID)

    assert response is not None

    logger.debug("Response:")
    _log_nested_dict(logger.debug, response)

    compares = _compare(
        response,
        EXPECTED_DEFAULT_GET_GRAPH_BY_UUID_RESPONSE,
        EXPECTED_DEFAULT_GET_GRAPH_BY_UUID_IMMUTABLE_MARKER,
    )

    assert compares