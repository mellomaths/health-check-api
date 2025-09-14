from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api import router as api_router
from infrastructure.logger import create_logger
from infrastructure.settings import get_settings
from models.up_response import UpResponse

settings = get_settings()
LOGGER = create_logger(__name__)
app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    ignore_trailing_slash=True,
    root_path=settings.app.root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

app.include_router(api_router, prefix=settings.api.path)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.app.name,
        version=settings.app.version,
        description=settings.app.description,
        routes=app.routes,
        servers=[
            {
                "url": "http://api.homepi.net/health",
                "description": "HomePi",
            },
            {
                "url": "http://localhost:3001",
                "description": "Local",
            },
        ],
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get(
    "/up",
    status_code=status.HTTP_200_OK,
    response_model=UpResponse,
    responses={503: {"model": UpResponse}},
)
async def up():
    log = LOGGER.getChild("up")
    log.info("Checking if the application is up")
    return JSONResponse(
        content=UpResponse(status="ok").model_dump(), status_code=status.HTTP_200_OK
    )
