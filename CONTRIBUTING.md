Contributing to dtool-lookup-api
===========================

Code style
----------
Always follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) with the exception of line
breaks.

Structure
---------

At the core of `dtool-lookup-api` is the `dtool_lookup_api.core.LookupClient.TokenBasedLookupClient` 
object. This object defines several asynchronous methods that translate the `dserver`'s REST
API (e.g. https://demo.dtool.dev/lookup/doc/swagger) into a Python interface 
that's usable as an asynchronous context. Derived from `TokenBasedLookupClient` are the
`CredentialsBasedLookupClient` and `ConfigurationBasedLookupClient`, which offer the
ame interface but extend the mechanisms of authentication against the server.

The modules `dtool_lookup_api.synchronous` and `dtool_lookup_api.asynchronous`
wrap these core objects to provide simple functional interfaces to the lookup API
in both synchronous and asynchronous settings.

Development branches
--------------------
New features should be developed always in its own branch. When creating your own branch,
please prefix that branch by the date of creation.
For example, if you begin working on implementing pagination on 6th April 2023, the branch could be called `2023-04-06-pagination`.

Commits
-------
Prepend you commits with a shortcut indicating the type of changes they contain:
* `BUG`: Bug fix
* `CI`: Changes to the CI configuration
* `DEP`: Update in 3rd-party dependencies
* `DOC`: Changes to documentation strings
* `ENH`: Enhancement (e.g. a new feature)
* `MAINT`: Maintenance (e.g. fixing a typo)
* `TST`: Changes to the unit test environment
* `WIP`: Work in progress
