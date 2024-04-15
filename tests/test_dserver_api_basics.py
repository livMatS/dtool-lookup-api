"""Test dtool_lookup_api package basics."""


def test_version_is_string():
    import dtool_lookup_api
    assert isinstance(dtool_lookup_api.__version__, str)
