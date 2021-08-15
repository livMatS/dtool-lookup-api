"""dtool_lookup_client.async module."""
from .core.LookupClient import ConfigurationBasedLookupClient


# TODO: instead of wrapping every method of LookupClient explicitly, automize

async def all():
    """Wraps around LookupClient method 'all'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.all()

async def aggregate(aggregation):
    """Wraps around LookupClient method 'aggregate'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.aggregate(aggregation)

async def config():
    """Wraps around LookupClient method 'config'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.config()


async def lookup(uuid):
    """Wraps around LookupClient method 'lookup'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.lookup(uuid)


async def manifest(uri):
    """Wraps around LookupClient method 'query'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.manifest(uri)


async def query(query):
    """Wraps around LookupClient method 'query'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.query(query)


async def readme(uri):
    """Wraps around LookupClient method 'readme'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.readme(uri)


async def search(keyword=None):
    """Wraps around LookupClient method 'search'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.search(keyword)


async def list_users():
    """Wraps around LookupClient method 'list_users'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.list_users()


async def register_user(username, is_admin=False):
    """Wraps around LookupClient method 'list_users'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.register_user(username, is_admin)


async def permission_info(base_uri):
    """Wraps around LookupClient method 'list_users'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.permission_info(base_uri)


async def update_permissions(base_uri, users_with_search_permissions, users_with_register_permissions=[]):
    """Wraps around LookupClient method 'list_users'."""
    async with ConfigurationBasedLookupClient() as lookup_client:
        return await lookup_client.update_permissions(base_uri, users_with_search_permissions, users_with_register_permissions)
