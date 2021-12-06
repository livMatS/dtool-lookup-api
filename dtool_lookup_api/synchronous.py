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

"""dtool_lookup_api.sync module."""

# TODO: make independent from external dependency

from asgiref.sync import async_to_sync

from . import asynchronous

# TODO: instead of ecplicitly wrapping every asynchronous method, automize


@async_to_sync
async def all():
    """Wraps around asynchronous.config."""
    return await asynchronous.all()


@async_to_sync
async def aggregate(aggregation):
    """Wraps around asynchronous.aggregate."""
    return await asynchronous.aggregate(aggregation)


@async_to_sync
async def config():
    """Wraps around asynchronous.config."""
    return await asynchronous.config()


@async_to_sync
async def lookup(uuid):
    """Wraps around asynchronous.lookup."""
    return await asynchronous.lookup(uuid)


@async_to_sync
async def manifest(uri):
    """Wraps around asynchronous.manifest."""
    return await asynchronous.manifest(uri)


@async_to_sync
async def query(query):
    """Wraps around asynchronous.query."""
    return await asynchronous.query(query)


@async_to_sync
async def readme(uri):
    """Wraps around asynchronous.uri."""
    return await asynchronous.readme(uri)


@async_to_sync
async def search(keyword=None):
    """Wraps around asynchronous.search."""
    return await asynchronous.search(keyword)


@async_to_sync
async def user_info(user):
    """Wraps around asynchronous.list_users."""
    return await asynchronous.user_info(user)


@async_to_sync
async def list_users():
    """Wraps around asynchronous.search."""
    return await asynchronous.list_users()


@async_to_sync
async def register_user(username, is_admin=False):
    """Wraps around asynchronous.search."""
    return await asynchronous.register_user(username, is_admin)


@async_to_sync
async def permission_info(base_uri):
    """Wraps around asynchronous.search."""
    return await asynchronous.permission_info(base_uri)


@async_to_sync
async def update_permissions(base_uri, users_with_search_permissions, users_with_register_permissions=[]):
    """Wraps around asynchronous.search."""
    return await asynchronous.register_user(base_uri, users_with_search_permissions, users_with_register_permissions)
