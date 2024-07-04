README
======

.. |dtool| image:: https://github.com/livMatS/dtool-lookup-api/blob/main/icons/22x22/dtool_logo.png?raw=True
    :height: 20px
    :target: https://github.com/livMatS/dtool-lookup-api

.. |pypi| image:: https://img.shields.io/pypi/v/dtool-lookup-api
    :alt: PyPI
    :target: https://pypi.org/project/dtool-lookup-api/

.. |tag| image:: https://img.shields.io/github/v/tag/livMatS/dtool-lookup-api
    :alt: GitHub tag (latest by date)
    :target: https://github.com/livMatS/dtool-lookup-api/tags

.. |tests| image:: https://img.shields.io/github/actions/workflow/status/livMatS/dtool-lookup-api/test.yml?branch=main&label=tests
    :alt: GitHub Workflow Status
    :target: https://github.com/livMatS/dtool-lookup-api/actions/workflows/test.yml

.. |docs| image:: https://readthedocs.org/projects/dtool-lookup-api/badge/?version=latest
   :target: https://readthedocs.org/projects/dtool-lookup-api?badge=latest
   :alt: Documentation Status

|dtool| |pypi| |tag| |tests| |docs|

Python API for interacting with dserver.

This package offers a class-based asynchronous lookup API within ``dtool_lookup_api.core.LookupClient``,
a simple class-less wrapper around it at ``dtool_lookup_api.asynchronous``,
and a synchronous interface on top at ``dtool_lookup_api.synchronous``.

Direct imports of utility functions from `dtool_lookup_api` in the examples below forward to the synchronous API variant.


Installation
------------

To install the dtool_lookup_api package.

.. code-block:: bash

    pip install dtool_lookup_api

This package depends on a `dserver
<https://github.com/jic-dtool/dserver>`_ instance to talk to.

Configuration
-------------

The API needs to know the URL of the lookup server

.. code-block:: bash

    export DSERVER_URL=https://localhost:5000

You may also need specify an access token generated on the server

.. code-block:: bash

    export DSERVER_TOKEN=$(flask user token testuser)


Instead of specifying the access token directly, it is also possible to provide

.. code-block:: bash

    export DSERVER_TOKEN_GENERATOR_URL=https://localhost:5001
    export DSERVER_USERNAME=my-username
    export DSERVER_PASSWORD=my-password

for the API to request a token. This, however, is intended only for testing
purposes and strongly discouraged in a production environment, as your password
would reside within environment variables or the dtool config file as clear text.

Our recommended setup is a combination of

.. code-block:: bash

    export DSERVER_URL=https://localhost:5000
    export DSERVER_TOKEN_GENERATOR_URL=https://localhost:5001

in the config. If used interactively, the API will then ask for your
credentials at the first interaction and cache the provided values for this
session, i.e.

.. code-block::

    In [1]: from dtool_lookup_api import query
       ...: res = query(
       ...:     {
       ...:         'readme.owners.name': {'$regex': '^Testing User$'},
       ...:     }
       ...: )
    Authentication URL https://localhost:5001/token username:my-username
    Authentication URL https://localhost:5001/token password:

    In [2]: res
    Out[2]:
    [{'base_uri': 'smb://test-share',
      'created_at': 'Sun, 08 Nov 2020 18:38:40 GMT',
      'creator_username': 'jotelha',
      'dtoolcore_version': '3.17.0',
      'frozen_at': 'Wed, 11 Nov 2020 17:20:30 GMT',
      'name': 'simple_test_dataset',
      'tags': [],
      'type': 'dataset',
      'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
      'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]

    In [3]: from dtool_lookup_api import all
       ...: all()
    Out[4]:
    [{'base_uri': 'smb://test-share',
      'created_at': 1604860720.736269,
      'creator_username': 'jotelha',
      'frozen_at': 1604921621.719575,
      'name': 'simple_test_dataset',
      'uri': 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675',
      'uuid': '1a1f9fad-8589-413e-9602-5bbd66bfe675'}]

Credentials caching and interactive prompting are turned off with

.. code-block::

  In [1]: import dtool_lookup_api.core.config
     ...: dtool_lookup_api.core.config.Config.interactive = False
     ...: dtool_lookup_api.core.config.Config.cache = False

  In [2]: from dtool_lookup_api import all
     ...: all()
  ...
  RuntimeError: Authentication failed

For testing purposes, it is possible to disable SSL certificates validation with

.. code-block:: bash

    export DSERVER_VERIFY_SSL=false

As usual, these settings may be specified within the default dtool configuration
file as well, i.e. at ``~/.config/dtool/dtool.json``

.. code-block:: bash

    {
        "DSERVER_TOKEN_GENERATOR_URL": "https://localhost:5001/token",
        "DSERVER_URL": "https://localhost:5000"
    }


List all datasets
-----------------

To list all registered datasets

.. code-block::

    In [1]: from dtool_lookup_api import get_datasets
       ...: res = get_datasets()

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

To lookup URIs from a dataset UUID within Python

.. code-block::

    In [1]: from dtool_lookup_api import get_datasets_by_uuid
       ...: uuid = "1a1f9fad-8589-413e-9602-5bbd66bfe675"
       ...: res = get_datasets_by_uuid(uuid)

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

Full text search for the word "test"

.. code-block::

    In [1]: from dtool_lookup_api import get_datasets
        ...: res = get_datasets(free_text="test")

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

Request the manifest of a particular dataset by URI

.. code-block::

    In [1]: from dtool_lookup_api import get_manifest
       ...: uri = 'smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675'
       ...: res = get_manifest(uri)

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

Request the readme content of a particular dataset by URI

.. code-block::

    In [1]: from dtool_lookup_api import get_readme
        ..: res = get_readme('smb://test-share/1a1f9fad-8589-413e-9602-5bbd66bfe675')

    In [2]: import yaml
        ..: yaml.safe_load(res)
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
expression pattern, send a direct mongo language query to the server with

.. code-block::

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


It is possible to search readme content via

.. code-block::

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

This requires the server-side `dserver-direct-mongo-plugin
<https://github.com/livMatS/dserver-direct-mongo-plugin>`_.

TODO: Response from server-side direct mongo plugin still yields dates as strings.
Fix within https://github.com/IMTEK-Simulation/dserver-direct-mongo-plugin.


Usage on Jupyter notebook
--------------------------

The current implementation via ``asgiref.async_to_sync`` (https://github.com/django/asgiref)
hinders the use of the synchronous interface within Jupyter notebooks.
Directly use the asynchronous api instead

.. code-block:: python

    import dtool_lookup_api.asynchronous as dl
    res = await dl.query({
        'base_uri': 'smb://test-share',
        'name': {'$regex': 'test'},
    })

The drawback of the above approach is that the same code doesn't work in python and in jupyter (`await` outsite of a function is a syntax error in non-interactive python context).
The code below can be executed in both contexts:

.. code-block:: python

    import dtool_lookup_api.asynchronous as dl
    if asyncio.get_event_loop().is_running():
        # then we are in jupyter notebook
        # this allows nested event loops, i.e. calls to asyncio.run inside the notebook as well
        # This way, the same code works in notebook and python
        import nest_asyncio
        nest_asyncio.apply()

    def query(query_dict):
        return asyncio.run(dl.query(query_dict))

    query({
        'base_uri': 'smb://test-share',
        'name': {'$regex': 'test'},
    })

See https://github.com/jupyter/notebook/issues/3397#issuecomment-419386811, https://ipython.readthedocs.io/en/stable/interactive/autoawait.html


Testing
-------

Install editable with testing requirements with

.. code-block:: bash

    pip install -e .[test]

By default, tests rely on the `demo.dtool.dev` demonstrator instance.

This can be changed by configuring

.. code-block:: python

    DSERVER_ADDRESS_AND_CREDENTIALS = {
        "DSERVER_URL": "https://demo.dtool.dev/lookup",
        "DSERVER_TOKEN_GENERATOR_URL": "https://demo.dtool.dev/token",
        "DSERVER_USERNAME": "testuser",
        "DSERVER_PASSWORD": "test_password",
        "DSERVER_VERIFY_SSL": False,
    }

within ``tests/conftest.py``.