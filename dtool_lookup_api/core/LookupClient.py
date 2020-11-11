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


async def authenticate(auth_url, username, password, verify_ssl=True):
    """Authenticate against token generator and return received token."""
    # async with aiohttp.ClientSession() as session:
    async with aiohttp.ClientSession() as session, session.post(
            auth_url,
            json={
                'username': username,
                'password': password
            }, verify_ssl=verify_ssl) as r:
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

        logger.debug("%s initialized with lookup_url=%s, verify_ssl=%s",
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

        logger.debug("Connect to %s, verify_ssl=%s", self.lookup_url, self.verify_ssl)

    @property
    def header(self):
        return {'Authorization': f'Bearer {self.token}'}

    async def all(self):
        """List all registered datasets."""
        async with self.session.get(
                f'{self.lookup_url}/dataset/list',
                headers=self.header, verify_ssl=self.verify_ssl) as r:
            return await r.json()

    async def search(self, keyword):
        """Free text search"""
        async with self.session.post(
                f'{self.lookup_url}/dataset/search',
                headers=self.header,
                json={
                    'free_text': keyword
                }, verify_ssl=self.verify_ssl) as r:
            return await r.json()

    # The direct-mongo plugin offers the same functionality as /dataset/search
    # plus an extra keyword "query" to contain plain mongo on the /mongo/query
    # route.

    # query and by_query are interchangeable
    async def query(self, query):
        """Direct mongo query."""
        return await self.by_query(query)

    async def by_query(self, query):
        """Direct mongo query"""
        if isinstance(query, str):
            query = json.loads(query)
        async with self.session.post(
                f'{self.lookup_url}/mongo/query',
                headers=self.header,
                json={
                    'query': query
                }, verify_ssl=self.verify_ssl) as r:
            return await r.json()

    # lookup and by_uuid are interchangeable
    async def lookup(self, uuid):
        """Search for a specific uuid"""
        return await self.by_uuid(uuid)

    async def by_uuid(self, uuid):
        """Search for a specific uuid"""
        async with self.session.get(
                f'{self.lookup_url}/dataset/lookup/{uuid}',
                headers=self.header,
                verify_ssl=self.verify_ssl) as r:
            return await r.json()

    async def graph(self, uuid, dependency_keys=None):
        """Request dependency graph for specific uuid"""
        if dependency_keys is None:
            async with self.session.get(
                    f'{self.lookup_url}/graph/lookup/{uuid}',
                    headers=self.header,
                    verify_ssl=self.verify_ssl) as r:
                return await r.json()
        else:  # TODO: validity check on dependency key list
            async with self.session.post(
                    f'{self.lookup_url}/graph/lookup/{uuid}',
                    headers=self.header,
                    json=dependency_keys,
                    verify_ssl=self.verify_ssl) as r:
                return await r.json()

    async def readme(self, uri):
        """Request the README.yml of a dataset by URI."""
        async with self.session.post(
                f'{self.lookup_url}/dataset/readme',
                headers=self.header,
                json={
                    'uri': uri
                }, verify_ssl=self.verify_ssl) as r:
            text = await r.text()
            return yaml.safe_load(text)

    async def manifest(self, uri):
        """Request the manifest of a dataset by URI."""
        async with self.session.post(
                f'{self.lookup_url}/dataset/manifest',
                headers=self.header,
                json={
                    'uri': uri
                }, verify_ssl=self.verify_ssl) as r:
            text = await r.text()
            return yaml.safe_load(text)

    async def config(self):
        """Request the server configuration."""
        async with self.session.get(
                f'{self.lookup_url}/config/info',
                headers=self.header,
                verify_ssl=self.verify_ssl) as r:
            text = await r.text()
            return yaml.safe_load(text)


class CredentialsBasedLookupClient(TokenBasedLookupClient):
    """Request new token for every session based on user credentials."""
    def __init__(self, lookup_url, auth_url, username, password,
                 verify_ssl=True):
        logger = logging.getLogger(__name__)
        self.auth_url = auth_url
        self.username = username
        self.password = password

        super().__init__(lookup_url=lookup_url, verify_ssl=verify_ssl)
        logger.debug("%s initialized with lookup_url=%s, auth_url=%s, username=%s, verify_ssl=%s",
                     type(self).__name__, self.lookup_url, self.auth_url, self.username, self.verify_ssl)

    async def connect(self):
        """Establish connection."""
        logger = logging.getLogger(__name__)
        logger.debug("Connect to lookup_url=%s, auth_url=%s, username=%s, verify_ssl=%s",
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
        if username is None:
            username = Config.username
        if password is None:
            password = Config.password
        if verify_ssl is None:
            verify_ssl = Config.verify_ssl

        logger.debug("Initializing % swith lookup_url=%s, auth_url=%s, username=%s, verify_ssl=%s, cache_token=%s",
                     type(self).__name__, lookup_url, auth_url, username, verify_ssl, cache_token)

        self.cache_token = cache_token

        super().__init__(
            lookup_url=lookup_url,
            auth_url=auth_url,
            username=username,
            password=password,
            verify_ssl=verify_ssl)

        self.token = Config.token
        logger.debug("%s initialized with lookup_url=%s, auth_url=%s, username=%s, verify_ssl=%s, cache_token=%s",
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
                    verify_ssl=self.verify_ssl) as r:
                status_code = r.status
                text = await r.text()
            logger.debug("Server answered with %s: %s.", status_code, yaml.safe_load(text))
            return status_code == 200


class LookupClient(CredentialsBasedLookupClient):
    """Deprecated, for compatibility reasons only."""
