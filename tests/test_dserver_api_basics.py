"""Test dserver_api package basics."""


def test_version_is_string():
    import dserver_api
    assert isinstance(dserver_api.__version__, str)
