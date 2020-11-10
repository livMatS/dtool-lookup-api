README
======

Python API for interacting with dtool lookup server

Installation
------------

To install the dtool_lookup_api package.

.. code-block:: bash

    pip install dtool_lookup_api

This package depends on a `dtool-lookup-server
<https://github.com/jic-dtool/dtool-lookup-server>`_ instance to talk to.

Configuration
-------------

The API needs to know the URL of the lookup server::

    export DTOOL_LOOKUP_SERVER_URL=http://localhost:5000

You also need to specify the access token::

    export DTOOL_LOOKUP_SERVER_TOKEN=$(flask user token testuser)


For testing purposes, it is possible to disable SSL certificates validation with::

    export DTOOL_LOOKUP_SERVER_VERIFY_SSL=false

As usual, these settings may be specified within the default dtool configuration file as well.

List all datasets
-----------------

To list all registered datasets::

    In [1]: from dtool_lookup_api import all
       ...: res = all()

    In [2]: res
    Out[2]:
    [{'base_uri': 'smb://test-share',
    'created_at': 1604860720.736269,
    'creator_username': 'jotelha',
    'frozen_at': 1604921621.719575,
    'name': 'simple_test_dataset',
    'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
    'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]



Looking up datasets by UUID
---------------------------

To lookup URIs from a dataset UUID within Python::

    In [1]: from dtool_lookup_api import lookup
       ...: uuid = "1a1f9fad-8589-413e-9602-5bbd66bfe675"
       ...: res = lookup(uuid)

    In [2]: res
    Out[2]:
    [{'base_uri': 'smb://test-share',
      'created_at': 1604860720.736269,
      'creator_username': 'jotelha',
      'frozen_at': 1604921621.719575,
      'name': 'simple_test_dataset',
      'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
      'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]


Full text searching
-------------------

Full text search for the word "test"::

    In [1]: from dtool_lookup_api import search
        ...: res = search("test")

    In [2]: res
    Out[2]:
    [{'base_uri': 'smb://test-share',
      'created_at': 1604860720.736,
      'creator_username': 'jotelha',
      'dtoolcore_version': '3.17.0',
      'frozen_at': 1605027357.308,
      'name': 'simple_test_dataset',
      'tags': [],
      'type': 'dataset',
      'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
      'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]


Manifest
--------

Request the manifest of a particular dataset by URI::

    In [1]: from dtool_lookup_api import manifest
       ...: uri = 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675'
       ...: res = manifest(uri)

    In [2]: res
    Out[2]:
    {'dtoolcore_version': '3.17.0',
     'hash_function': 'md5sum_hexdigest',
     'items': {'eb58eb70ebcddf630feeea28834f5256c207edfd': {'hash': '2f7d9c3e0cfd47e8fcab0c12447b2bf0',
       'relpath': 'simple_text_file.txt',
       'size_in_bytes': 17,
       'utc_timestamp': 1605027357.284966}}}


Readme
------

Request the readme cotent of a particular dataset by URI::

    In [1]: from dtool_lookup_api import readme
        ..: res = readme('smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675')

    In [2]: res
    Out[2]:
    {'creation_date': '2020-11-08',
    'description': 'testing description',
    'expiration_date': '2022-11-08',
    'funders': [{'code': 'testing_code',
     'organization': 'testing_organization',
     'program': 'testing_program'}],
    'owners': [{'email': 'testing@test.edu',
     'name': 'Testing User',
     'orcid': 'testing_orcid',
     'username': 'testing_user'}],
    'project': 'testing project'}



Direct mongo language queries
-----------------------------

To list all datasets at a certain base URI with their name matching some regular
expression pattern, send a direct mongo language query to the server with::

    In [15]: from dtool_lookup_api import query
        ...: res = query(
        ...:     {
        ...:         'base_uri': 'smb://test-share',
        ...:         'name': {'$regex': 'test'},
        ...:     }
        ...: )

    In [16]: res
    Out[16]:
    [{'base_uri': 'smb://test-share',
    'created_at': 'Sun, 08 Nov 2020 18:38:40 GMT',
    'creator_username': 'jotelha',
    'dtoolcore_version': '3.17.0',
    'frozen_at': 'Tue, 10 Nov 2020 16:55:57 GMT',
    'name': 'simple_test_dataset',
    'tags': [],
    'type': 'dataset',
    'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
    'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]


It is possible to search readme content via::

    In [21]: from dtool_lookup_api import query
        ...: res = query(
        ...:     {
        ...:         'readme.owners.name': {'$regex': '^Testing User$'},
        ...:     }
        ...: )

    In [22]: res
    Out[22]:
    [{'base_uri': 'smb://test-share',
      'created_at': 'Sun, 08 Nov 2020 18:38:40 GMT',
      'creator_username': 'jotelha',
      'dtoolcore_version': '3.17.0',
      'frozen_at': 'Tue, 10 Nov 2020 16:55:57 GMT',
      'name': 'simple_test_dataset',
      'tags': [],
      'type': 'dataset',
      'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
      'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]


This requires the server-side `dtool-lookup-server-direct-mongo-plugin
<https://github.com/IMTEK-Simulation/dtool-lookup-server-direct-mongo-plugin>`_.

TODO: Response from server-side direct mongo plugin still yields dates as strings.
Fix within https://github.com/IMTEK-Simulation/dtool-lookup-server-direct-mongo-plugin.
