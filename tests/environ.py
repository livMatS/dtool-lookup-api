# coding: utf-8
#
# environ.py
#
# Copyright (C) 2020 IMTEK Simulation
# Author: Johannes Hoermann, johannes.hoermann@imtek.uni-freiburg.de
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
"""Temporary OS environ context manager."""

import logging
import os

from utils import _log_nested_dict


class TemporaryOSEnviron:
    """Preserve original os.environ context manager."""

    def __init__(self, env=None):
        """env is a flat dict to be inserted into os.environ."""
        self._insertions = env

    def __enter__(self):
        """Store backup of current os.environ."""
        logger = logging.getLogger(__name__)
        logger.debug("Backed-up os.environ:")
        _log_nested_dict(logger.debug, dict(os.environ))
        self._original_environ = os.environ.copy()

        if self._insertions:
            for k, v in self._insertions.items():
                logger.debug("Inject env var '{}' = '{}'".format(k, v))
                os.environ[k] = str(v)

        logger.debug("Initial modified os.environ:")
        _log_nested_dict(logger.debug, dict(os.environ))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore backed up os.environ."""
        logger = logging.getLogger(__name__)
        os.environ = self._original_environ
        logger.debug("Recovered os.environ:")
        _log_nested_dict(logger.debug, os.environ)
