CHANGELOG
=========

0.7.0 (14Aug23)
---------------

- New versions method for retrieving server and server side plugin version information.

0.6.1 (12Jul23)
---------------

- New dependency graph request schema in use.

0.6.0 (26Apr23)
---------------

- Server-side pagination

0.5.1 (23Oct22)
---------------

- Fixed erroneous interpretation of server response in `register_base_uri` and `update_permissions`.
- Fixed parsing of text to JSON in `aggregate`.
- Made all synchronous methods available at top-level via imports in `__init__.py`

0.5.0 (6Dec21)
--------------

- Automatically create `synchronous` and `asynchronous` modules.
- Detect server errors (in particular if a token expires) and raise exceptions.

0.4.1 (3Dec21)
--------------

- Removed obsolete prompting for username and password when valid access token available

0.4.0 (27Nov21)
---------------

- Added `user_info` method for accessing server route `/user/info`.

0.2.0 (30Aug21)
---------------

- ``dtool_lookup_api.lookup``
- ``dtool_lookup_api.search``
- ``dtool_lookup_api.query``
- ``dtool_lookup_api.config``
- ... as well as their asynchronous pendants within ``dtool_lookup_api.asynchronous`` ...
- and the underlying core mechanisms within ``dtool_lookup_api.core.LookupClient```.
