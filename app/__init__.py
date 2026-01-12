import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from openremote_client.schemas import ExternalServiceSchema

from services.mcp_client import init_mcp_client_service
from services.openremote_service import init_openremote_service
from .config import config
from .cors import init_cors
from app.routers import init_routers


# FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init OpenRemote service
    print("Homepage url:", config.app_homepage_url)
    await init_openremote_service(
        host=str(config.openremote_url),
        client_id=config.openremote_client_id,
        client_secret=config.openremote_client_secret,
        verify_SSL=config.openremote_verify_ssl,
        service_schema=ExternalServiceSchema(
            serviceId=config.openremote_service_id,
            label="MCP-Client",
            homepageUrl=config.app_homepage_url,
            status="AVAILABLE",
        )
    )

    # Init MCP client
    mcp_config_json: dict

    if config.mcp_config is not None:
        mcp_config_json = config.mcp_config
    elif Path(config.mcp_config_file).is_file():
        with open(config.mcp_config_file, "r") as file:
            file_text = file.read()
            mcp_config_json = json.loads(file_text)
    else:
        raise RuntimeError("No MCP configuration provided.")

    await init_mcp_client_service(mcp_config_json)

    yield

app = FastAPI(
    title="OpenRemote MCP client Service",
    description="MCP client integrated with OpenRemote",
    lifespan=lifespan
)



init_cors(app)
init_routers(app)


app.mount("/", StaticFiles(directory=config.app_static_folder, html=True), name="static")
