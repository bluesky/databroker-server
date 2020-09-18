from pathlib import Path
from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse


router = APIRouter()


@router.get("/{run_uid}")
async def read_run_preview(run_uid: str):
    """Return a PNG if one exists for the UID."""
    preview = Path(f"/tmp/{run_uid}.png")
    if not preview.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(preview.absolute(), media_type="image/png")
