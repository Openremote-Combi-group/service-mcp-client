from fastapi import APIRouter

from app import model_provider
from app.schemas import AIModel

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
async def list_available_models() -> list[AIModel]:
    return model_provider.list_available_models()


@router.get("/{name}")
async def get_model_by_name(name: str) -> AIModel:
    return model_provider.get_model_by_name(name)