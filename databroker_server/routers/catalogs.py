from fastapi import APIRouter, HTTPException
from ..model import databroker

router = APIRouter()


@router.get("/")
async def read_catalogs():
    """List the catalogs the server has access to."""
    catalogs = []
    for item in databroker.catalogs():
        catalogs.append({"name": item})
    return catalogs


@router.get("/{catalog_id}")
async def read_catalog(catalog_id: str):
    """List the runs within the supplied catalog."""
    runs = []
    run_list = databroker.runs(catalog_id)
    if run_list == None:
        raise HTTPException(status_code=404, detail="Not found")
    for run in run_list:
        runs.append({"uid": run})
    return runs

@router.get("/{catalog_id}/{uid}")
async def read_run(catalog_id: str, uid: str):
    """List the streams witin a uid."""
    streams = []
    stream_list = databroker.streams(catalog_id, uid)
    if stream_list == None:
        raise HTTPException(status_code=404, detail="Not found")
    for stream in stream_list:
        streams.append({"name": stream})
    return streams

@router.put(
    "/{id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_catalog(id: str):
    if id != "test":
        raise HTTPException(status_code=403, detail="You can only update test")
    return {"id": id, "name": "test"}