from fastapi import FastAPI, APIRouter
from httpx import HTTPStatusError
from starlette.responses import JSONResponse

from services.openremote_service import get_openremote_service
from app.config import config

router = APIRouter()


@router.get("/health")
async def health():
    openremote_service = get_openremote_service()

    try:
        await openremote_service.client.status.get_health_status()
    except HTTPStatusError:
        return JSONResponse({"status": "unhealthy", "service_id": config.openremote_service_id, "error": "Failed to connect to OpenRemote"}, status_code=200)

    return JSONResponse({"status": "healthy", "service_id": config.openremote_service_id}, status_code=200)
