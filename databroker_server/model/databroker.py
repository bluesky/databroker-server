from databroker import catalog

def _has_runs(catalog):
    """Borrowed from bluesky-widgets, see if we are at a 'leaf'."""
    from databroker.v2 import Broker

    return isinstance(catalog, Broker)


def catalogs():
    """Get a list of catalogs."""
    return list(catalog)

def runs(name: str):
    """Get a list of runs for a catalog."""
    try:
        current = catalog[name]
    except KeyError:
        return None
    return list(current)

def streams(catalog_id: str, uid: str):
    """Get a list of streams from the run."""
    try:
        current = catalog[catalog_id]
    except KeyError:
        return None
    if _has_runs(current):
        return list(current[uid])

    return None
