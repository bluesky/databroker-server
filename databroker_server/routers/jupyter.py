import asyncio
import functools
import os
from urllib.parse import urljoin

from fastapi import APIRouter, HTTPException
from httpx import AsyncClient

router = APIRouter()


INTERNAL_JUPYTER_BASE_URL = os.getenv("DATABROKER_SERVER_INTERNAL_JUPYTER_BASE_URL", "http://locahost:8888")
"Base URL to Juptyer server as seen from this server, e.g. 'http://localhost:8888'"

EXTERNAL_JUPYTER_BASE_URL = os.getenv("DATABROKER_SERVER_EXTERNAL_JUPYTER_BASE_URL", "http://locahost:8888")
"Base URL to Juptyer server as seen from the client/user, e.g. 'http://localhost:8888'"

JUPYTER_ACCESS_TOKEN = os.getenv("DATABROKER_SERVER_JUPYTER_ACCESS_TOKEN", "dev")
"Access token to Jupyter server, e.g. 'dev'"

JUPYTER_PAPERMILL_TEMPLATE = os.getenv(
    "DATABROKER_SERVER_JUPYTER_PAPERMILL_TEMPLATE",
    "./dashboard_template.ipynb"
)
"Filepath to a notebook with a cell of papermill parameters"

HEADERS = {"Authorization": f"token {JUPYTER_ACCESS_TOKEN}"}


@functools.lru_cache(maxsize=1)
def read_template():
    "Read the template file just once, the first time it is needed."
    import json

    with open(JUPYTER_PAPERMILL_TEMPLATE) as file:
        return json.load(file)


@router.get("/{catalog_name}/{run_uid}")
async def run_voila_dashboard(catalog_name: str, run_uid: str):
    """Create a dashboard for this Run."""
    in_path = "dashboard_template.ipynb"
    out_path = f"dashboard_{catalog_name}_{run_uid}.ipynb"
    async with AsyncClient(base_url=INTERNAL_JUPYTER_BASE_URL) as client:
        response = await client.put(
            f"/api/contents/{in_path}",
            json={"content": read_template(), "type": "notebook"},
            headers=HEADERS,
        )
        if response.is_error:
            raise HTTPException(
                status_code=500,
                detail=f"Dashboard setup failed with error {response.status_code} {response.reason_phrase}")
        response = await client.post(
            "/papermillhub/",
            json={
                "in_path": in_path,
                "out_path": out_path,
                # TODO Eventually use the catalog_name in the template too.
                "parameters": {"uid": run_uid}},
            headers=HEADERS,
        )
        if response.is_error:
            raise HTTPException(
                status_code=500,
                detail=f"Dashboard creation failed with error {response.status_code} {response.reason_phrase}")
        job_id = response.json()["job_id"]
        # A retry loop
        for attempt in range(10):
            response = await client.get("/papermillhub/")
            if response.is_error:
                raise HTTPException(
                    status_code=500,
                    detail=("Monitoring dashboard creation failed with error "
                            f"{response.status_code} {response.reason_phrase}"))
            if job_id not in response.json()["jobs"]:
                # Papermill is done with our job.
                break
            # Papermill is still working on this job.
            # Wait 1 second and then check # on it again.
            await asyncio.sleep(1)
        else:
            # We have done 10 retries, taking greater than 10 seconds. Give up.
            raise HTTPException(
                status_code=500, detail="Dashboard generation took more than 10 seconds.")
    dashboard_url = urljoin(EXTERNAL_JUPYTER_BASE_URL, f"/voila/render/{out_path}")
    return {"dashboard_url": dashboard_url}
