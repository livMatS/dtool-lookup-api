CHANGELOG
=========

0.3.0 (6Dec21)
--------------

- Automatically create `synchronous` and `asynchronous` modules.
- Detect server errors (in particular if a token expires) and raise exceptions.

0.2.0 (30Aug21)
---------------

- ``dtool_lookup_api.lookup``
- ``dtool_lookup_api.search``
- ``dtool_lookup_api.query``
- ``dtool_lookup_api.config``
- ... as well as their asynchronous pendants within ``dtool_lookup_api.asynchronous`` ...
- and the underlying core mechanisms within ``dtool_lookup_api.core.LookupClient```.
