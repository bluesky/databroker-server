from databroker import catalog

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
    