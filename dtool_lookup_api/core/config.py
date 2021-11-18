"""dtool_lookup_api.core.config module."""

import logging

from getpass import getpass

import dtoolcore.utils

CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH

DTOOL_LOOKUP_SERVER_URL_KEY = "DTOOL_LOOKUP_SERVER_URL"
DTOOL_LOOKUP_SERVER_TOKEN_KEY = "DTOOL_LOOKUP_SERVER_TOKEN"
DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL_KEY = "DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL"
DTOOL_LOOKUP_SERVER_USERNAME_KEY = "DTOOL_LOOKUP_SERVER_USERNAME"
DTOOL_LOOKUP_SERVER_PASSWORD_KEY = "DTOOL_LOOKUP_SERVER_PASSWORD"
DTOOL_LOOKUP_SERVER_VERIFY_SSL_KEY = "DTOOL_LOOKUP_SERVER_VERIFY_SSL"

AFFIRMATIVE_EXPRESSIONS = ['true', '1', 'y', 'yes', 'on']
NEGATIVE_EXPRESSIONS = ['false', '0', 'n', 'no', 'off']

logger = logging.getLogger(__name__)

class DtoolLookupAPIConfig():
    """Connect to dtool lookup server session."""

    def __init__(self, interactive=True, cache=True):
        """If interactive set True, allow prompting for username and password.
           If cache set True, store entered username and password entered during
           runtime."""
        if logger.level >= logging.DEBUG:  # only query properties if output desired
            for attr in ('lookup_url', 'auth_url', 'username', 'verify_ssl'):
                logger.debug("dtool config %s: %s", attr, getattr(self, attr, None))

        self.interactive = interactive
        self.cache = cache

        self._username_cache = None
        self._password_cache = None

        if self.token is None and (
                self.username is None or self.password is None or self.auth_url is None):
            logger.warning(
                'Please provide either %s or a pair of credentials %s and %s together with %s.',
                DTOOL_LOOKUP_SERVER_TOKEN_KEY, DTOOL_LOOKUP_SERVER_USERNAME_KEY,
                DTOOL_LOOKUP_SERVER_PASSWORD_KEY, DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL_KEY)

    @property
    def lookup_url(self):
        lookup_url = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_URL_KEY)
        if lookup_url is None:
            logger.warning('Please provide %s', DTOOL_LOOKUP_SERVER_URL_KEY)
        return lookup_url

    @lookup_url.setter
    def lookup_url(self, value):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_URL_KEY, value)

    # optional
    @property
    def token(self):
        return dtoolcore.utils.get_config_value_from_file(
            DTOOL_LOOKUP_SERVER_TOKEN_KEY, default="")

    @token.setter
    def token(self, token):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_TOKEN_KEY, token)

    @property
    def auth_url(self):
        return dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL_KEY, default="")

    @auth_url.setter
    def auth_url(self, value):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_TOKEN_GENERATOR_URL_KEY, value)

    @property
    def username(self):
        if self._username_cache is None:
            username = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_USERNAME_KEY)
            if username is None and self.interactive:
                username = input("Authentication URL {:s} username:".format(self.auth_url))
            if self.cache:
                self._username_cache = username
        else:
            username = self._username_cache
        return username

    @username.setter
    def username(self, value):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_USERNAME_KEY, value)

    @property
    def password(self):
        if self._password_cache is None:
            password = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_PASSWORD_KEY)
            if password is None and self.interactive:
                password = getpass("Authentication URL {:s} password:".format(self.auth_url))
            if self.cache:
                self._password_cache = password
        else:
            password = self._password_cache
        return password

    @password.setter
    def password(self, value):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_PASSWORD_KEY, value)

    @property
    def verify_ssl(self):
        verify_ssl = dtoolcore.utils.get_config_value(DTOOL_LOOKUP_SERVER_VERIFY_SSL_KEY)
        if isinstance(verify_ssl, str) and verify_ssl.lower() in NEGATIVE_EXPRESSIONS:
            verify_ssl = False
        elif not isinstance(verify_ssl, bool):
            verify_ssl = True
        return verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, value):
        dtoolcore.utils.write_config_value_to_file(DTOOL_LOOKUP_SERVER_VERIFY_SSL_KEY,
                                                   AFFIRMATIVE_EXPRESSIONS[0] if value else NEGATIVE_EXPRESSIONS[0])


Config = DtoolLookupAPIConfig()
