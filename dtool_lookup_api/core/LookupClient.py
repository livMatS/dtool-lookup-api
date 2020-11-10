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


# TODO: implement writing token to config file as within dtool_lookup_client's
# def token(dtool_lookup_server_token):
#     """Display / set / update token for dtool lookup server."""
#     if dtool_lookup_server_token is None:
#         click.secho(dtoolcore.utils.get_config_value_from_file(
#             DTOOL_LOOKUP_SERVER_TOKEN_KEY, default=""
#         ))
#     else:
#         click.secho(dtoolcore.utils.write_config_value_to_file(
#             DTOOL_LOOKUP_SERVER_TOKEN_KEY,
#             dtool_lookup_server_token
#         ))


class LookupClient:
    """Core Python interface for communication with dtool lookup server."""
    def __init__(self, lookup_url, auth_url, username, password, verify_ssl=True):
        self.session = aiohttp.ClientSession()
        self.lookup_url = lookup_url
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl

    async def __aenter__(self):
        logger = logging.getLogger(__name__)
        await self.connect()
        logger.debug("Connection to %s established." % self.lookup_url)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger = logging.getLogger(__name__)
        await self.session.close()
        logger.debug("Connection to %s closed." % self.lookup_url)

    async def connect(self):
        """Establisch connection."""
        await self._authenticate(self.username, self.password)

    async def _authenticate(self, username, password):
        logger = logging.getLogger(__name__)
        async with self.session.post(
                self.auth_url,
                json={
                    'username': username,
                    'password': password
                }, verify_ssl=self.verify_ssl) as r:
            if r.status == 200:
                json = await r.json()
                if 'token' not in json:
                    raise RuntimeError('Authentication failed')
                else:
                    self.token = json['token']
                    self.header = {'Authorization': f'Bearer {self.token}'}

                logger.debug("Authentication succeeded.")
            else:
                raise RuntimeError(f'Error {r.status} retrieving data from '
                                   f'authentication server.')

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
