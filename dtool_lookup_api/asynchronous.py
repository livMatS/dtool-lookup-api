"""dtool_lookup_client.async module."""
from .core.config import Config
from .core.LookupClient import LookupClient

class ConfiguredLookupClient(LookupClient):
    """Wrapper for profiding default configuration values."""
    def __init__(self, lookup_url=Config.lookup_url,
                 auth_url=Config.auth_url,
                 username=Config.username,
                 password=Config.password,
                 verify_ssl=Config.verify_ssl):
        super().__init__(lookup_url, auth_url, username, password, verify_ssl)

# TODO: instead of wrapping every method of LookupClient explicitly, automize


async def all():
    """Wraps around LookupClient method 'all'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.all()


async def config():
    """Wraps around LookupClient method 'config'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.config()


async def lookup(uuid):
    """Wraps around LookupClient method 'lookup'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.lookup(uuid)


async def manifest(uri):
    """Wraps around LookupClient method 'query'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.manifest(uri)


async def query(query):
    """Wraps around LookupClient method 'query'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.query(query)


async def readme(uri):
    """Wraps around LookupClient method 'readme'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.readme(uri)


async def search(keyword=None):
    """Wraps around LookupClient method 'search'."""
    async with ConfiguredLookupClient() as lookup_client:
        return await lookup_client.search(keyword)
