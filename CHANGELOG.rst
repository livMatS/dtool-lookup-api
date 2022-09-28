CHANGELOG
=========

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
