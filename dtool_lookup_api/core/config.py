"""dtool_lookup_api.core.config module."""

import logging

import dtoolcore.utils

CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH

DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"
DTOOL_LOOKUP_SERVER_USERNAME_KEY = "DTOOL_LOOKUP_SERVER_USERNAME"
DTOOL_LOOKUP_SERVER_PASSWORD_KEY = "DTOOL_LOOKUP_SERVER_PASSWORD"
DTOOL_LOOKUP_SERVER_VERIFY_SSL_KEY = "DTOOL_LOOKUP_SERVER_VERIFY_SSL"

AFFIRMATIVE_EXPRESSIONS = ['true', '1', 'y', 'yes', 'on']
NEGATIVE_EXPRESSIONS = ['false', '0', 'n', 'no', 'off']


class Config(object):
    """Connect to dtool lookup server session."""

    # required
    lookup_url = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_URL_KEY)
    if lookup_url is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_URL_KEY))

    auth_url = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_TOKEN_KEY)
    if auth_url is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_TOKEN_KEY))

    username = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_USERNAME_KEY)
    if username is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_USERNAME_KEY))

    password = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_PASSWORD_KEY)
    if username is None:
        raise RuntimeError('Please provide {}'.format(DTOOL_LOOKUP_SERVER_PASSWORD_KEY))

    # optional
    verify_ssl = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_VERIFY_SSL_KEY)
    if isinstance(verify_ssl, str) and verify_ssl.lower() in NEGATIVE_EXPRESSIONS:
        verify_ssl = False
    elif not isinstance(verify_ssl, bool):
        verify_ssl = True


logger = logging.getLogger(__name__)
for attr in ('lookup_url', 'auth_url', 'username', 'verify_ssl'):
    logger.debug("dtool config %s: %s" % (attr, getattr(Config, attr, None)))
