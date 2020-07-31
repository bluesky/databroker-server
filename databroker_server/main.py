from fastapi import Depends, FastAPI, Header, HTTPException

from .routers import catalogs, users

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
    catalogs.router,
    prefix="/catalogs",
    tags=["catalogs"],
    responses={404: {"description": "Not found"}},
)
# Example blocking a route based upon a dependency.
#app.include_router(
#    catalogs.router,
#    prefix="/sekrit-catalogs",
#    tags=["catalogs", "sekrit"],
#    dependencies=[Depends(get_token_header)],
#    responses={404: {"description": "Not found"}},
#)