"""dtool_lookup_api package."""

from setuptools_scm import get_version
__version__ = get_version(root='..', relative_to=__file__)

# use synchronous API as default
from .synchronous import (config, all, lookup, manifest, query, readme, search, list_users, register_user,
                          permission_info, update_permissions)
