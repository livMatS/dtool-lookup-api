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
import urllib.parse

import aiohttp
import certifi
import ssl

from .config import Config

import warnings
import functools

ASCENDING = 1
DESCENDING = -1

def deprecated(replacement=None):
    """Marks a function or method a deprecated and hints to a possible replacement."""
    def decorator(func):
        """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used."""
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            msg = "Call to deprecated function {}.".format(func.__name__)
            if replacement is not None:
                msg += " Use '{}' instead.".format(replacement)

            warnings.warn(msg,
                          category=DeprecationWarning,
                          stacklevel=2)

            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        return new_func
    return decorator


def _parse_sort_fields(sort_fields, sort_order):
    """Translates sort fields to single string as expected by dserver. Internal."""

    if isinstance(sort_fields, str):
        sort_fields = [sort_fields]

    if isinstance(sort_order, int):
        sort_order = [sort_order]

    # assert that sort fields and sort order have same length
    prefixed_fields = []
    for field, order in zip(sort_fields, sort_order):
        if order == DESCENDING:
            prefixed_field = '-' + field
        else:
            prefixed_field = field
        prefixed_fields.append(prefixed_field)

    sort = ','.join(prefixed_fields)
    return sort


class LookupServerError(Exception):
    pass


class TokenBasedLookupClient:
    """Core Python interface for communication with dserver."""

    def __init__(self, lookup_url, token=None, verify_ssl=True):
        logger = logging.getLogger(__name__)

        self.ssl_context = None
        # self.ssl_context = aiohttp.ClientSSLContext()
        if verify_ssl:
            certifi_where = certifi.where()
            logger.debug("Use certifi certficates at %s", certifi_where)
            self.ssl_context = ssl.create_default_context(cafile=certifi_where)
        else:
            logger.debug("Do not verify ssl certificates.")

        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context))

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

    async def _get(self, route, headers={}):
        """Return information from a specific route."""
        async with self.session.get(
                f'{self.lookup_url}{route}',
                headers=self.header, ssl=self.verify_ssl) as r:
            json = await r.json()
            self._check_json(json)
            headers.update(**r.headers)
            return json

    async def _post(self, route, json, method='json', headers={}):
        """Wrapper for http post methpod.

        Parameters
        ----------
        route : str
        json : dict
            request data
        method : str, default 'json'
            method do interpret response data
        headers : dict
            dict filled with response headers

        Returns
        -------
        list or dict or str
            parsed json response if parsable, otherwise plain text"""
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
            headers.update(**r.headers)
            return json

    async def _put(self, route, json, method='status', headers={}):
        """Wrapper for http put method.

        Parameters
        ----------
        route : str
        json : dict
            request data
        method : str, default 'json'
            method do interpret response data
        headers : dict
            dict filled with response headers

        Returns
        -------
        list or dict or str
            parsed json response if parsable, otherwise plain text"""
        async with self.session.put(
                f'{self.lookup_url}{route}',
                headers=self.header,
                json=json,
                ssl=self.verify_ssl) as r:
            try:  # workaround for other non-json, non-method properties, better solutions welcome
                json = await getattr(r, method)()
            except TypeError:
                json = getattr(r, method)
            self._check_json(json)
            headers.update(**r.headers)
            return json

    async def _delete(self, route, method='status', headers={}):
        """Wrapper for http put method.

        Parameters
        ----------
        route : str
        method : str, default 'json'
            method do interpret response data
        headers : dict
            dict filled with response headers

        Returns
        -------
        list or dict or str
            parsed json response if parsable, otherwise plain text"""
        async with self.session.delete(
                f'{self.lookup_url}{route}',
                headers=self.header,
                ssl=self.verify_ssl) as r:
            try:  # workaround for other non-json, non-method properties, better solutions welcome
                json = await getattr(r, method)()
            except TypeError:
                json = getattr(r, method)
            self._check_json(json)
            headers.update(**r.headers)
            return json

    # configuration routes

    async def get_config(self):
        """Request the server configuration."""
        response = await self._get('/config/info')
        return response["config"]

    async def get_versions(self):
        """Request versions from the server"""
        response = await self._get('/config/versions')
        return response["versions"]

    # uris routes

    async def get_datasets(self, free_text=None, creator_usernames=None,
                           base_uris=None, uuids=None, tags=None,
                           page_number=1, page_size=10,
                           sort_fields=["uri"], sort_order=[ASCENDING],
                           pagination={}, sorting={}):
        """
        Get dataset entries on lookup server, filtered if desired.

        Parameters
        ----------
        free_text : str, optional
            select datasets containing this free text
        creator_usernames: list of str, optional
            select datasets created by any of these specific users
        base_uris: list of str, optional
            select datasets living on any of these base URIs
        uuids: list of str, optional
            select datasets matching any of these UUIDs
        tags: list of str, optional
            select datasets matching all provided tags
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        pagination : dict
            dictionary filled with data from the X-Pagination response header, e.g.
            '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sorting : dict
            dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        json : list of dict
            search results
        """
        headers = {}
        post_body = {}
        if free_text is not None:
            post_body.update({'free_text': free_text})
        if creator_usernames is not None:
            post_body.update({'creator_usernames': creator_usernames})
        if base_uris is not None:
            post_body.update({'base_uris': base_uris})
        if uuids is not None:
            post_body.update({'uuids': uuids})
        if tags is not None:
            post_body.update({'tags': tags})

        sort = _parse_sort_fields(sort_fields, sort_order)

        dataset_list = await self._post(
            f'/uris?page={page_number}&page_size={page_size}&sort={sort}',
            post_body, headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no sorting information. Server version outdated.")

        return dataset_list

    async def get_dataset(self, uri):
        """
        Retrieve dataset information by URI.

        Parameters
        ----------
        uri : str
            The unique resource identifier (URI) of the dataset to be retrieved.

        Returns
        -------
        dict
            Basic metadata info for dataset at URI.
        """
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._get(f'/uris/{encoded_uri}')
        return response

    # delete dataset

    async def delete_dataset(self, uri):
        """Delete a dataset using URI. (Needs admin privileges.)"""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._delete(f'/uris/{encoded_uri}')
        return response == 200

    # register dataset

    async def register_dataset(self, uri, base_uri, readme, manifest, uuid,
                               name, type, creator_username, frozen_at,
                               created_at, annotations, tags, number_of_items,
                               size_in_bytes):
        """Register or update a dataset using URI."""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._put(
            f'/uris/{encoded_uri}',
            dict(uuid=uuid,
                 uri=uri,
                 base_uri=base_uri,
                 name=name, type=type,
                 readme=readme,
                 manifest=manifest,
                 creator_username=creator_username,
                 frozen_at=frozen_at,
                 created_at=created_at,
                 annotations=annotations,
                 tags=tags,
                 number_of_items=number_of_items,
                 size_in_bytes=size_in_bytes)
        )
        return response in set([200, 201])

    # uuids routes

    async def get_datasets_by_uuid(self, uuid, page_number=1, page_size=10,
                                   sort_fields=["uri"], sort_order=[ASCENDING],
                                   pagination={}, sorting={}):
        """
        Search for entries by a specific UUID.

        Parameters
        ----------
        uuid : str
            The unique identifier (UUID) of the dataset to be searched.
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination: dict, optional
            Dictionary filled with data from the X-Pagination response header, e.g.
                '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        list of dict
            Query results for the specified UUID.
        """
        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        lookup_list = await self._get(
            f'/uuids/{uuid}?page={page_number}&page_size={page_size}&sort={sort}', headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no sorting information. Server version outdated.")

        return lookup_list

    # metadata retrieval routes

    async def get_readme(self, uri):
        """Request the README.yml of a dataset by URI."""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._get(f'/readmes/{encoded_uri}')
        return response["readme"]

    async def get_manifest(self, uri):
        """Request the manifest of a dataset by URI."""
        encoded_uri = urllib.parse.quote_plus(uri)
        return await self._get(f'/manifests/{encoded_uri}')

    async def get_tags(self, uri):
        """Request the tags of a dataset by URI."""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._get(f'/tags/{encoded_uri}')
        return response["tags"]

    async def get_annotations(self, uri):
        """Request the annotations of a dataset by URI."""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._get(f'/annotations/{encoded_uri}')
        return response["annotations"]

    # user management routes

    async def get_users(self, page_number=1, page_size=10,
                        sort_fields=["username"], sort_order=[ASCENDING],
                        pagination={}, sorting={}):
        """
        Request a list of users. (Needs admin privileges.)

        Parameters
        ----------
        page_number : int, optional
           The page number of the results, default is 1.
        page_size : int, optional
           The number of results per page, default is 10.
        pagination: dict, optional
           Dictionary filled with data from the X-Pagination response header, e.g.
               '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        list of dict
           User information including username, email, roles, etc.
        """

        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        users = await self._get(
            f'/users?page={page_number}&page_size={page_size}&sort={sort}', headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no sorting information. Server version outdated.")

        return users

    async def get_me(self):
        """Request the current user info."""
        response = await self._get('/me')
        return response

    async def get_user(self, username=None):
        """Request user info.

        If no username specified, query currently authenticated user."""
        if username is None:
            response = await self._get('/me')
        else:
            encoded_username = urllib.parse.quote_plus(username)
            response = await self._get(f'/users/{encoded_username}')
        return response

    async def register_user(self, username, is_admin=False):
        """Register or update a user. (Needs admin privileges.)"""
        encoded_username = urllib.parse.quote_plus(username)
        response = await self._put(
            f'/users/{encoded_username}',
            dict(username=username, is_admin=is_admin))
        return response in set([200, 201])

    async def delete_user(self, username):
        """Delete a user. (Needs admin privileges.)"""
        encoded_username = urllib.parse.quote_plus(username)
        response = await self._delete(f'/users/{encoded_username}')
        return response == 200

    async def get_summary(self, username=None):
        """Overall summary of datasets accessible to a user.

        If no username specified, query currently authenticated user."""
        if username is None:
            response = await self._get('/me/summary')
        else:
            encoded_username = urllib.parse.quote_plus(username)
            response = await self._get(f'/users/{encoded_username}/summary')
        return response

    async def get_my_summary(self):
        """Overall summary of datasets accessible to the current user."""
        response = await self._get('/me/summary')
        return response

    # base URIs & permissions management routes

    async def get_base_uris(self, page_number=1, page_size=10,
                            sort_fields=["base_uri"], sort_order=[ASCENDING],
                            pagination={}, sorting={}):
        """
        List all registered base URIs. (Needs admin privileges.)

        Parameters
        ----------
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination: dict, optional
            Dictionary filled with data from the X-Pagination response header, e.g.
               '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
                '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        list of dict
           Registered base URIs information including name, URI, and description.
        """
        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        base_uris_list = await self._get(
            f'/base-uris?page={page_number}&page_size={page_size}&sort={sort}', headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.warning("Server returned no sorting information. Server version outdated.")

        return base_uris_list

    async def get_base_uri(self, base_uri):
        """Request base URI info."""
        encoded_base_uri = urllib.parse.quote_plus(base_uri)
        response = await self._get(f'/base-uris/{encoded_base_uri}')
        return response

    async def register_base_uri(self, base_uri,
                                users_with_search_permissions=[],
                                users_with_register_permissions=[]):
        """Register or update a base URI. (Needs admin privileges.)"""
        encoded_base_uri = urllib.parse.quote_plus(base_uri)
        response = await self._put(
            f'/base-uris/{encoded_base_uri}',
            dict(users_with_search_permissions=users_with_search_permissions,
                 users_with_register_permissions=users_with_register_permissions))
        return response in set([200, 201])

    async def delete_base_uri(self, base_uri):
        """Delete a base URI. (Needs admin privileges.)"""
        encoded_base_uri = urllib.parse.quote_plus(base_uri)
        response = await self._delete(f'/base-uris/{encoded_base_uri}')
        return response == 200

    # server-side plugin-dependent routes

    async def get_datasets_by_mongo_aggregation(self, aggregation,
                        page_number=1, page_size=10,
                        sort_fields=["uri"], sort_order=[ASCENDING],
                        pagination={}, sorting={}):
        """
        Execute a direct MongoDB aggregation.

        Parameters
        ----------
        aggregation : str or dict
            The MongoDB aggregation pipeline to be executed.
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination : dict
            Dictionary filled with data from the X-Pagination response header, e.g.
            '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        list of dict
            Aggregation results.
        """

        if isinstance(aggregation, str):
            aggregation = json.loads(aggregation)

        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        aggregation_result = await self._post(
            f'/mongo/aggregate?page={page_number}&page_size={page_size}&sort={sort}',
            dict(aggregation=aggregation), headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no sorting information. Server version outdated.")

        return aggregation_result

    async def get_datasets_by_mongo_query(self, query, creator_usernames=None,
                    base_uris=None, uuids=None, tags=None,
                    page_number=1, page_size=10,
                    sort_fields=["uri"], sort_order=[ASCENDING],
                    pagination={}, sorting={}):
        """
        Direct mongo query, requires server-side direct mongo plugin.

        Parameters
        ----------
        query : str or dict
            The MongoDB query to be executed.
        creator_usernames: list of str, optional
            Select datasets created by any of these specific users
        base_uris: list of str, optional
            Select datasets living on any of these base URIs
        uuids: list of str, optional
            Select datasets matching any of these UUIDs
        tags: list of str, optional
            Select datasets matching all provided tags
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination : dict
            Dictionary filled with data from the X-Pagination response header, e.g.
            '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        json : list of dict
            query results
        """

        if isinstance(query, str):
            query = json.loads(query)

        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        post_body = {'query': query}
        if creator_usernames is not None:
            post_body.update({'creator_usernames': creator_usernames})
        if base_uris is not None:
            post_body.update({'base_uris': base_uris})
        if uuids is not None:
            post_body.update({'uuids': uuids})
        if tags is not None:
            post_body.update({'tags': tags})

        query_result = await self._post(
            f'/mongo/query?page={page_number}&page_size={page_size}&sort={sort}', post_body, headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no sorting information. Server version outdated.")

        return query_result

    async def get_graph_by_uuid(self, uuid, dependency_keys=None,
                                page_number=1, page_size=10,
                                sort_fields=["uri"], sort_order=[ASCENDING],
                                pagination={}, sorting={}):
        """
        Request dependency graph for a specific UUID.

        Parameters
        ----------
        uuid : str
            The unique identifier of the dataset for which the dependency graph is requested.
        dependency_keys : list of str, optional
            A list of dependency keys to filter the dependency graph.
            If not provided, the entire dependency graph will be returned.
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination: dict, optional
            Dictionary filled with data from the X-Pagination response header, e.g.
                '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'
        sort_fields: str or list of str, optional
            default is "uri"
        sort_order: int or list of int of ASCENDING (1) or DESCENDING (-1)
            default is ASCENDING (1)
        sorting : dict
            Dictionary filled with data from the X-Sort response header, e.g.
            '{"sort": {"uuid": 1}}' for ascending sorting by uuid

        Returns
        -------
        list of dict
            Dependency graph results.
        """

        headers = {}

        sort = _parse_sort_fields(sort_fields, sort_order)

        if dependency_keys is None:
            dependency_graph = await self._get(
                f'/graph/uuids/{uuid}?page={page_number}&page_size={page_size}&sort={sort}',
                headers=headers)
        else:  # TODO: validity check on dependency key list
            dependency_graph = await self._post(
                f'/graph/uuids/{uuid}?page={page_number}&page_size={page_size}&sort={sort}',
                {"dependency_keys": dependency_keys}, headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no pagination information. Server version outdated.")

        if 'X-Sort' in headers:
            p = json.loads(headers['X-Sort'])
            sorting.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no sorting information. Server version outdated.")

        return dependency_graph

    # deprecated

    @deprecated(replacement="get_config")
    async def config(self):
        """Request the server configuration. Deprecated."""
        return self.get_config()

    @deprecated(replacement="get_versions")
    async def versions(self):
        """Request versions from the server. Deprecated."""
        return self.get_versions()

    @deprecated(replacement="get_datasets")
    async def all(self, page_number=1, page_size=20, pagination={}):
        """List all registered datasets."""
        return await self.get_datasets(page_number=page_number,
                                       page_size=page_size,
                                       pagination=pagination)

    @deprecated(replacement="get_datasets")
    async def search(self, keyword, page_number=1, page_size=10, pagination={}):
        """
        Free text search.

        Parameters
        ----------
        keyword : str
            free text search text
        page_number : int, optional
            The page number of the results, default is 1.
        page_size : int, optional
            The number of results per page, default is 10.
        pagination : dict
            dictionary filled with data from the X-Pagination response header, e.g.
            '{"total": 124, "total_pages": 13, "first_page": 1, "last_page": 13, "page": 1, "next_page": 2}'

        Returns
        -------
        json : list of dict
            search results
        """
        headers = {}
        dataset_list = await self._post(
            f'/uris?page={page_number}&page_size={page_size}',
            {'free_text': keyword}, headers=headers)

        if 'X-Pagination' in headers:
            p = json.loads(headers['X-Pagination'])
            pagination.update(**p)
        else:
            logger = logging.getLogger(__name__)
            logger.debug("Server returned no pagination information. Server version outdated.")
        return dataset_list

    @deprecated(replacement="get_datasets_by_uuid")
    async def lookup(self, uuid, page_number=1, page_size=10, pagination={}):
        """Search for entries by a specific UUID."""
        return await self.get_datasets_by_uuid(uuid=uuid, page_number=page_number, page_size=page_size, pagination=pagination)

    @deprecated(replacement="get_datasets_by_uuid")
    async def by_uuid(self, uuid, page_number=1, page_size=10, pagination={}):
        """Search for entries by a specific UUID."""
        return await self.get_datasets_by_uuid(uuid=uuid, page_number=page_number, page_size=page_size, pagination=pagination)

    @deprecated(replacement="get_readme")
    async def readme(self, uri):
        """Request the README.yml of a dataset by URI. Deprecated."""
        encoded_uri = urllib.parse.quote_plus(uri)
        response = await self._get(f'/readmes/{encoded_uri}')
        return response["readme"]

    @deprecated(replacement="get_manifest")
    async def manifest(self, uri):
        """Request the manifest of a dataset by URI. Deprecated."""
        encoded_uri = urllib.parse.quote_plus(uri)
        return await self._get(f'/manifests/{encoded_uri}')

    @deprecated(replacement="get_users")
    async def list_users(self, page_number=1, page_size=10, pagination={}):
        """Request a list of users. (Needs admin privileges.)"""
        return await self.get_users(page_number=page_number, page_size=page_size, pagination=pagination)

    @deprecated(replacement="get_user")
    async def user_info(self, username):
        """Request user info. Deprecated."""
        return await self.get_user(username)

    @deprecated(replacement="get_summary")
    async def summary(self):
        """Overall summary of datasets accessible to a user."""
        return await self.get_summary()

    @deprecated(replacement="get_base_uris")
    async def list_base_uris(self, page_number=1, page_size=10, pagination={}):
        return await self.get_base_uris(page_number=page_number,
                                        page_size=page_size,
                                        pagination=pagination)

    @deprecated(replacement="get_datasets_by_mongo_aggregation")
    async def aggregate(self, aggregation,
                        page_number=1, page_size=10,
                        sort_fields=["uri"], sort_order=[ASCENDING],
                        pagination={}, sorting={}):
        return await self.get_datasets_by_mongo_aggregation(
            aggregation=aggregation,
            page_number=page_number, page_size=page_size, pagination=pagination,
            sort_fields=sort_fields, sort_order=sort_order, sorting=sorting)

    @deprecated(replacement="get_datasets_by_mongo_query")
    async def by_query(self, query,
                       creator_usernames=None,
                       base_uris=None, uuids=None, tags=None,
                       page_number=1, page_size=10,
                       sort_fields=["uri"], sort_order=[ASCENDING],
                       pagination={}, sorting={}):
        """Direct mongo query, requires server-side direct mongo plugin."""
        return await self.get_datasets_by_mongo_query(
            query=query, creator_usernames=creator_usernames, base_uris=base_uris, uuids=uuids, tags=tags,
            page_number=page_number, page_size=page_size, pagination=pagination,
            sort_fields=sort_fields, sort_order=sort_order, sorting=sorting)

    @deprecated(replacement="get_datasets_by_mongo_query")
    async def query(self, query, creator_usernames=None,
                    base_uris=None, uuids=None, tags=None,
                    page_number=1, page_size=10,
                    sort_fields=["uri"], sort_order=[ASCENDING],
                    pagination={}, sorting={}):
        return await self.get_datasets_by_mongo_query(
            query=query, creator_usernames=creator_usernames, base_uris=base_uris, uuids=uuids, tags=tags,
            page_number=page_number, page_size=page_size, pagination=pagination,
            sort_fields=sort_fields, sort_order=sort_order, sorting=sorting)

    @deprecated(replacement="get_graph_by_uuid")
    async def graph(self, uuid, dependency_keys=None, page_number=1, page_size=10, pagination={}):
        return await self.get_graph_by_uuid(self, uuid, dependency_keys=dependency_keys,
                          page_number=page_number, page_size=page_size, pagination=pagination)


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

    async def authenticate(self):
        """Authenticate against token generator and return received token."""
        async with self.session.post(
                self.auth_url,
                json={
                    'username': self.username,
                    'password': self.password
                }, ssl=self.verify_ssl) as r:
            if r.status == 200:
                json = await r.json()
                if 'token' not in json:
                    raise RuntimeError('Authentication failed')
                else:
                    return json['token']
            else:
                raise RuntimeError(f'Error {r.status} retrieving data from '
                                   f'authentication server.')

    async def connect(self):
        """Establish connection."""
        logger = logging.getLogger(__name__)
        logger.debug("Connect to lookup_url=%s, auth_url=%s, username=%s, ssl=%s",
                     self.lookup_url, self.auth_url, self.username, self.verify_ssl)

        self.token = await self.authenticate()

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
