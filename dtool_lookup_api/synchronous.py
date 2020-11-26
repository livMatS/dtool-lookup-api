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
