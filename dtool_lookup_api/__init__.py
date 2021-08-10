"""dtool_lookup_api package."""

from .version import version as __version__

# use synchronous API as default
from .synchronous import (config, all, lookup, manifest, query, readme, search, list_users, register_user,
						  permission_info, update_permissions)
