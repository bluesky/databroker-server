from datetime import datetime

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


def rich_runs(name: str):
    """ Get a rich list of runs for a catalog."""
    try:
        current = catalog[name]
    except KeyError:
        return None
    if not _has_runs(current):
        return None

    run_list = []
    for uid in current:
        run_data = {}
        run_data["uid"] = uid
        run = current[uid]
        run_data["scan_id"] = run.metadata["start"]["scan_id"]
        run_data["timestamp"] = run.metadata["start"]["time"]
        run_data["date_time"] = datetime.fromtimestamp(run.metadata["start"]["time"])
        run_data["plan_name"] = run.metadata["start"]["plan_name"]
        run_list.append(run_data)

    return run_list


def run_summary(catalog_id: str, uid: str):
    """Generate a summary of the selected run."""
    try:
        current = catalog[catalog_id]
    except KeyError:
        return None
    if not _has_runs(current):
        return None

    run = current[uid]
    summary = {}
    summary["uid"] = uid
    summary["start"] = run.metadata["start"]
    summary["stop"] = run.metadata["stop"]
    summary["streams"] = list(run)
    return summary


def stream_summary(catalog_id: str, uid: str, stream: str):
    try:
        current = catalog[catalog_id]
    except KeyError:
        return None
    if not _has_runs(current):
        return None
    run = current[uid]
    try:
        s = run[stream]
    except KeyError:
        return None

    summary = {}
    summary["uid"] = uid
    summary["name"] = stream
    summary["metadata"] = s.metadata
    summary["data_keys"] = list(s.metadata["descriptors"][0]["data_keys"])
    return summary
