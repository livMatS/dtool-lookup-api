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

"""dtool_lookup_api.core.config module."""

import logging

from getpass import getpass

import dtoolcore.utils

CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH

DSERVER_URL_KEY = "DSERVER_URL"
DSERVER_TOKEN_KEY = "DSERVER_TOKEN"
DSERVER_TOKEN_GENERATOR_URL_KEY = "DSERVER_TOKEN_GENERATOR_URL"
DSERVER_USERNAME_KEY = "DSERVER_USERNAME"
DSERVER_PASSWORD_KEY = "DSERVER_PASSWORD"
DSERVER_VERIFY_SSL_KEY = "DSERVER_VERIFY_SSL"

AFFIRMATIVE_EXPRESSIONS = ['true', '1', 'y', 'yes', 'on']
NEGATIVE_EXPRESSIONS = ['false', '0', 'n', 'no', 'off']

logger = logging.getLogger(__name__)

class DtoolLookupAPIConfig():
    """Connect to dserver session."""

    def __init__(self, interactive=True, cache=True):
        """If interactive set True, allow prompting for username and password.
           If cache set True, store entered username and password entered during
           runtime."""
        if logger.level >= logging.DEBUG:  # only query properties if output desired
            for attr in ('lookup_url', 'auth_url', 'username', 'verify_ssl'):
                logger.debug("dtool config %s: %s", attr, getattr(self, attr, None))

        # don't behave interactive at constructor
        self.interactive = False
        self.cache = cache

        self._username_cache = None
        self._password_cache = None

        if self.token is None and (
                self.username is None or self.password is None or self.auth_url is None):
            logger.warning(
                'Please provide either %s or a pair of credentials %s and %s together with %s.',
                DSERVER_TOKEN_KEY, DSERVER_USERNAME_KEY,
                DSERVER_PASSWORD_KEY, DSERVER_TOKEN_GENERATOR_URL_KEY)

        self.interactive = interactive

    @property
    def lookup_url(self):
        lookup_url = dtoolcore.utils.get_config_value(DSERVER_URL_KEY)
        if lookup_url is None:
            logger.warning('Please provide %s', DSERVER_URL_KEY)
        return lookup_url

    @lookup_url.setter
    def lookup_url(self, value):
        dtoolcore.utils.write_config_value_to_file(DSERVER_URL_KEY, value)

    # optional
    @property
    def token(self):
        return dtoolcore.utils.get_config_value_from_file(
            DSERVER_TOKEN_KEY, default="")

    @token.setter
    def token(self, token):
        dtoolcore.utils.write_config_value_to_file(DSERVER_TOKEN_KEY, token)

    @property
    def auth_url(self):
        return dtoolcore.utils.get_config_value(DSERVER_TOKEN_GENERATOR_URL_KEY, default="")

    @auth_url.setter
    def auth_url(self, value):
        dtoolcore.utils.write_config_value_to_file(DSERVER_TOKEN_GENERATOR_URL_KEY, value)

    @property
    def username(self):
        if self._username_cache is None:
            username = dtoolcore.utils.get_config_value(DSERVER_USERNAME_KEY)
            if username is None and self.interactive:
                username = input("Authentication URL {:s} username:".format(self.auth_url))
            if self.cache:
                self._username_cache = username
        else:
            username = self._username_cache
        return username

    @username.setter
    def username(self, value):
        dtoolcore.utils.write_config_value_to_file(DSERVER_USERNAME_KEY, value)

    @property
    def password(self):
        if self._password_cache is None:
            password = dtoolcore.utils.get_config_value(DSERVER_PASSWORD_KEY)
            if password is None and self.interactive:
                password = getpass("Authentication URL {:s} password:".format(self.auth_url))
            if self.cache:
                self._password_cache = password
        else:
            password = self._password_cache
        return password

    @password.setter
    def password(self, value):
        dtoolcore.utils.write_config_value_to_file(DSERVER_PASSWORD_KEY, value)

    @property
    def verify_ssl(self):
        verify_ssl = dtoolcore.utils.get_config_value(DSERVER_VERIFY_SSL_KEY)
        if isinstance(verify_ssl, str) and verify_ssl.lower() in NEGATIVE_EXPRESSIONS:
            verify_ssl = False
        elif not isinstance(verify_ssl, bool):
            verify_ssl = True
        return verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, value):
        dtoolcore.utils.write_config_value_to_file(DSERVER_VERIFY_SSL_KEY,
                                                   AFFIRMATIVE_EXPRESSIONS[0] if value else NEGATIVE_EXPRESSIONS[0])


Config = DtoolLookupAPIConfig()
