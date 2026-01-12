from fastapi import FastAPI

from .chat import router as chat_router
from .health import router as health_router
from .models import router as models_router


def init_routers(app: FastAPI):
    app.include_router(chat_router, prefix="/api")
    app.include_router(health_router, prefix='/api')
    app.include_router(models_router, prefix='/api')