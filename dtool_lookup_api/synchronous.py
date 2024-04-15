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

"""Module that has synchronous API access functions in its global scope."""

import inspect
from asgiref.sync import async_to_sync

from .core.LookupClient import ConfigurationBasedLookupClient


class _WrapClient:
    def __init__(self, name, func):
        self._name = name
        self._func = func
        self.__doc__ = self._func.__doc__

    @async_to_sync
    async def __call__(self, *args, **kwargs):
        async with ConfigurationBasedLookupClient() as lookup_client:
            return await self._func(lookup_client, *args, **kwargs)


# Import all methods from ConfigurationBasedLookupClient into the global namespace
for name, func in inspect.getmembers(ConfigurationBasedLookupClient, predicate=inspect.isfunction):
    # Import everything that does not start with an underscore
    if not name.startswith('_'):
        globals()[name] = _WrapClient(name, func)
