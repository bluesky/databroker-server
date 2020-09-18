from fastapi import APIRouter

router = APIRouter()

# This is a simple placeholder for getting user names etc, not functional.


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "foo"}, {"username": "bar"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "it_is_me"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
