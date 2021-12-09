import asyncio
import dtool_lookup_api.asynchronous as dl

if asyncio.get_event_loop().is_running():
    # then we are in jupyter notebook
    # this allows nested event loops, i.e. calls to asyncio.run inside the notebook as well
    # This way, the same code works in notebook and python
    import nest_asyncio

    nest_asyncio.apply()


def wrap_asyncio(fun):
    def wrapped(*args, **kwargs):
        return asyncio.run(fun(*args, **kwargs))

    return wrapped


query = wrap_asyncio(dl.query)
readme = wrap_asyncio(dl.readme)

# TODO: automate this: https://stackoverflow.com/questions/39184338/how-can-i-decorate-all-functions-imported-from-a-file
