#
# Copyright 2020 Lars Pastewka, Johannes Laurin Hoermann
#
# ### MIT license
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""dtool_lookup_api.core.LookupClient module."""


import yaml
import json
import logging

import aiohttp

from .config import Config


class LookupServerError(Exception):
    pass


async def authenticate(auth_url, username, password, verify_ssl=True):
    """Authenticate against token generator and return received token."""
    # async with aiohttp.ClientSession() as session:
    async with aiohttp.ClientSession() as session, session.post(
            auth_url,
            json={
                'username': username,
                'password': password
            }, ssl=verify_ssl) as r:
        if r.status == 200:
            json = await r.json()
            if 'token' not in json:
                raise RuntimeError('Authentication failed')
            else:
                return json['token']
        else:
            raise RuntimeError(f'Error {r.status} retrieving data from '
                               f'authentication server.')


class TokenBasedLookupClient:
    """Core Python interface for communication with dtool lookup server."""
    def __init__(self, lookup_url, token=None, verify_ssl=True):
        logger = logging.getLogger(__name__)

        self.session = aiohttp.ClientSession()
        self.lookup_url = lookup_url
        self.verify_ssl = verify_ssl
        self.token = token

        logger.debug("%s initialized with lookup_url=%s, ssl=%s",
                     type(self).__name__, self.lookup_url, self.verify_ssl)

    async def __aenter__(self):
        logger = logging.getLogger(__name__)
        await self.connect()
        logger.debug("Connection to %s established.", self.lookup_url)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger = logging.getLogger(__name__)
        await self.session.close()
        logger.debug("Connection to %s closed.", self.lookup_url)

    async def connect(self):
        """Establish connection."""
        logger = logging.getLogger(__name__)

        if self.token is None or self.token == "":
            raise ValueError(
                "Provide JWT token.")

        logger.debug("Connect to %s, ssl=%s", self.lookup_url, self.verify_ssl)

    @property
    def header(self):
        return {'Authorization': f'Bearer {self.token}'}

    def _check_json(self, json):
        if isinstance(json, dict) and 'msg' in json:
            raise LookupServerError(json['msg'])

    async def _get(self, route):
        """Return information from a specific route."""
        async with self.session.get(
                f'{self.lookup_url}{route}',
                headers=self.header, ssl=self.verify_ssl) as r:
            json = await r.json()
            self._check_json(json)
            return json

    async def _post(self, route, json, method='json'):
        async with self.session.post(
                f'{self.lookup_url}{route}',
                headers=self.header,
                json=json,
                ssl=self.verify_ssl) as r:
            try:  # workaround for other non-json, non-method properties, better solutions welcome
                json = await getattr(r, method)()
            except TypeError:
                json = getattr(r, method)
            self._check_json(json)
            return json

    async def summary(self):
        """Overall summary of datasets accessible to a user."""
        return await self._get('/dataset/summary')

    async def all(self):
        """List all registered datasets."""
        return await self._get('/dataset/list')

    async def aggregate(self, aggregation):
        """Direct mongo aggregation, requires server-side direct mongo plugin."""
        if isinstance(aggregation, str):
            aggregation = json.loads(aggregation)
        return await self._post('/mongo/aggregate', dict(aggregation=aggregation))

    async def search(self, keyword):
        """Free text search"""
        return await self._post('/dataset/search', dict(free_text=keyword))

    # The direct-mongo plugin offers the same functionality as /dataset/search
    # plus an extra keyword "query" to contain plain mongo on the /mongo/query
    # route.

    # query and by_query are interchangeable
    async def query(self, query):
        """Direct mongo query, requires server-side direct mongo plugin."""
        return await self.by_query(query)

    async def by_query(self, query):
        """Direct mongo query, , requires server-side direct mongo plugin"""
        if isinstance(query, str):
            query = json.loads(query)
        return await self._post('/mongo/query', dict(query=query))

    # lookup and by_uuid are interchangeable
    async def lookup(self, uuid):
        """Search for a specific uuid."""
        return await self.by_uuid(uuid)

    async def by_uuid(self, uuid):
        """Search for a specific uuid."""
        return await self._get(f'/dataset/lookup/{uuid}')

    async def graph(self, uuid, dependency_keys=None):
        """Request dependency graph for specific uuid"""
        if dependency_keys is None:
            return await self._get(f'/graph/lookup/{uuid}')
        else:  # TODO: validity check on dependency key list
            return await self._post(f'/graph/lookup/{uuid}', dependency_keys)

    async def readme(self, uri):
        """Request the README.yml of a dataset by URI."""
        return await self._post('/dataset/readme', dict(uri=uri))

    async def manifest(self, uri):
        """Request the manifest of a dataset by URI."""
        return await self._post('/dataset/manifest', dict(uri=uri))

    async def config(self):
        """Request the server configuration."""
        return await self._get('/config/info')

    async def user_info(self, user):
        """Request user info."""
        return await self._get(f'/user/info/{user}')

    async def list_users(self):
        """Request a list of users. (Needs admin privileges.)"""
        return await self._get('/admin/user/list')

    async def register_base_uri(self, base_uri):
        """Register a base URI. (Needs admin privileges.)"""
        return await self._post('/admin/base_uri/register', dict(base_uri=base_uri),
                                method='status') == 201

    async def list_base_uris(self):
        """List all registered base URIs. (Needs admin privileges.)"""
        return await self._get('/admin/base_uri/list')

    async def register_user(self, username, is_admin=False):
        """Register a user. (Needs admin privileges.)"""
        return await self._post('/admin/user/register', [dict(username=username, is_admin=is_admin)],
                                method='status') == 201

    async def permission_info(self, base_uri):
        """Request permissions on base URI. (Needs admin privileges.)"""
        return await self._post('/admin/permission/info', dict(base_uri=base_uri))

    async def update_permissions(self, base_uri, users_with_search_permissions, users_with_register_permissions=[]):
        """Request permissions on base URI. (Needs admin privileges.)"""
        return await self._post('/admin/permission/update_on_base_uri', dict(
            base_uri=base_uri,
            users_with_search_permissions=users_with_search_permissions,
            users_with_register_permissions=users_with_register_permissions),
            method='status') == 201


class CredentialsBasedLookupClient(TokenBasedLookupClient):
    """Request new token for every session based on user credentials."""
    def __init__(self, lookup_url, auth_url, username, password,
                 verify_ssl=True):
        logger = logging.getLogger(__name__)
        self.auth_url = auth_url
        self.username = username
        self.password = password

        super().__init__(lookup_url=lookup_url, verify_ssl=verify_ssl)
        logger.debug("%s initialized with lookup_url=%s, auth_url=%s, username=%s, ssl=%s",
                     type(self).__name__, self.lookup_url, self.auth_url, self.username, self.verify_ssl)

    async def connect(self):
        """Establish connection."""
        logger = logging.getLogger(__name__)
        logger.debug("Connect to lookup_url=%s, auth_url=%s, username=%s, ssl=%s",
                     self.lookup_url, self.auth_url, self.username, self.verify_ssl)

        self.token = await authenticate(
            auth_url=self.auth_url,
            username=self.username,
            password=self.password,
            verify_ssl=self.verify_ssl)

        await super().connect()


class ConfigurationBasedLookupClient(CredentialsBasedLookupClient):
    """Use configured token if available and valid or reuest new token with credentials if provided."""

    # This class is intended on looking up any possibly configured token
    # and reuse that before requesting a new one (if any credentials are provided
    def __init__(self,
                 lookup_url=None,
                 auth_url=None,
                 username=None,
                 password=None,
                 verify_ssl=None,
                 cache_token=True):
        logger = logging.getLogger(__name__)
        # In order to avoid unwanted side effects, it is necessry to assign defaults as below

        if lookup_url is None:
            lookup_url = Config.lookup_url
        if auth_url is None:
            auth_url = Config.auth_url
        if verify_ssl is None:
            verify_ssl = Config.verify_ssl

        logger.debug("Initializing %s with lookup_url=%s, auth_url=%s, username=%s, ssl=%s, cache_token=%s",
                     type(self).__name__, lookup_url, auth_url, username, verify_ssl, cache_token)

        self.cache_token = cache_token

        super().__init__(
            lookup_url=lookup_url,
            auth_url=auth_url,
            username=username,
            password=password,
            verify_ssl=verify_ssl)

        self.token = Config.token
        logger.debug("%s initialized with lookup_url=%s, auth_url=%s, username=%s, ssl=%s, cache_token=%s",
                     type(self).__name__, self.lookup_url, self.auth_url,
                     self.username, self.verify_ssl, self.cache_token)

    async def connect(self):
        """Establish connection."""
        logger = logging.getLogger(__name__)
        if self.token is None or self.token == "":
            self.token = Config.token

        if await self.has_valid_token():
            logger.debug("Reusing provided token.")
            await TokenBasedLookupClient.connect(self)
        else:
            # only look for username and password if really necessry
            if self.username is None:
                self.username = Config.username
            if self.password is None:
                self.password = Config.password
            logger.debug("Requesting new token.")
            await CredentialsBasedLookupClient.connect(self)

        if self.cache_token:
            logger.debug("Caching token.")
            Config.token = self.token

    # TODO: Replace with something more elegant.
    async def has_valid_token(self):
        """Determine whether token still valid."""
        logger = logging.getLogger(__name__)
        if self.token is None or self.token == "":
            logger.debug("Token empty.")
            return False
        else:
            logger.debug("Testing token validity via /config/info route.")
            async with self.session.get(
                    f'{self.lookup_url}/config/info',
                    headers=self.header,
                    ssl=self.verify_ssl) as r:
                status_code = r.status
                text = await r.text()
            logger.debug("Server answered with %s: %s.", status_code, yaml.safe_load(text))
            return status_code == 200


class LookupClient(CredentialsBasedLookupClient):
    """Deprecated, for compatibility reasons only."""
