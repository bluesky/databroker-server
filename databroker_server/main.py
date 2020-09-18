import logging

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.logger import logger

from .routers import runs, users, previews

# gunicorn_logger = logging.getLogger('gunicorn.error')
# logger.handlers = gunicorn_logger.handlers
# if __name__ != "main":
#    logger.setLevel(gunicorn_logger.level)
# else:
#    logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="DataBroker HTTP Server",
    description="The HTTP API server for the DataBroker project",
    version="0.0.1",
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)
app.include_router(
    runs.router,
    prefix="/runs",
    tags=["runs"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    previews.router,
    prefix="/previews",
    tags=["previews"],
    responses={404: {"description": "Not found"}},
)
# Example blocking a route based upon a dependency.
# app.include_router(
#    catalogs.router,
#    prefix="/sekrit-catalogs",
#    tags=["catalogs", "sekrit"],
#    dependencies=[Depends(get_token_header)],
#    responses={404: {"description": "Not found"}},
# )
