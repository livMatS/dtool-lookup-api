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

"""dtool_lookup_api package."""

from .version import version as __version__

# use synchronous API as default
from .synchronous import (
    # config
    get_config,
    get_versions,
    # uris
    get_datasets,
    get_dataset,
    register_dataset,
    delete_dataset,
    # uuids
    get_datasets_by_uuid,
    # metadata retrieval
    get_manifest,
    get_readme,
    get_annotations,
    get_tags,
    # users
    get_users,
    get_user,
    register_user,
    delete_user,
    get_summary,
    # base-uris
    get_base_uris,
    get_base_uri,
    register_base_uri,
    delete_base_uri,
    # server-side plugin-dependent functionality
    get_datasets_by_mongo_aggregation,
    get_datasets_by_mongo_query,
    get_graph_by_uuid,
    # deprecated
    all,
    search,
    config,
    versions,
    list_base_uris,
    list_users,
    lookup,
    manifest,
    readme,
    summary,
    user_info,
    aggregate,
    query,
    graph
)
