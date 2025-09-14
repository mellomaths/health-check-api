from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from checks.postgres import check_postgres_health, get_postgres_session
from checks.redis import check_redis_health
from infrastructure.logger import create_logger
from models.health_check_response import HealthCheckResponse, ServiceStatusType

LOGGER = create_logger(__name__)
router = APIRouter(prefix="/check", tags=["health-check"], redirect_slashes=False)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    responses={503: {"model": HealthCheckResponse}},
)
async def health_check(
    session: Session = Depends(get_postgres_session),
):
    log = LOGGER.getChild("health_check")
    log.info("Checking health of the application")
    
    # Check PostgreSQL health
    log.info("Checking postgres health")
    is_postgres_up, postgres_error = check_postgres_health(session)
    log.info(f"Postgres health check response: {is_postgres_up}, {postgres_error}")
    
    # Check Redis health
    log.info("Checking redis health")
    is_redis_up, redis_error = check_redis_health()
    log.info(f"Redis health check response: {is_redis_up}, {redis_error}")
    
    # Determine overall health status
    overall_health = is_postgres_up and is_redis_up
    status_code = status.HTTP_200_OK
    if not overall_health:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    response = HealthCheckResponse(
        success=overall_health, 
        up=ServiceStatusType(postgres=is_postgres_up, redis=is_redis_up)
    )
    log.info(f"Health check response: {response}")
    return JSONResponse(content=response.model_dump(), status_code=status_code)


@router.get(
    "/postgres/",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    responses={503: {"model": HealthCheckResponse}},
)
async def postgres_health_check(
    session: Session = Depends(get_postgres_session),
):
    log = LOGGER.getChild("postgres_health_check")
    log.info("Checking postgres health")
    is_postgres_up, error = check_postgres_health(session)
    log.info(f"Postgres health check response: {is_postgres_up}, {error}")
    status_code = status.HTTP_200_OK
    if not is_postgres_up or error:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    health = is_postgres_up
    response = HealthCheckResponse(
        success=health, up=ServiceStatusType(postgres=is_postgres_up, redis=True)
    )
    log.info(f"Postgres health check response: {response}")
    return JSONResponse(content=response.model_dump(), status_code=status_code)


@router.get(
    "/redis/",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
    responses={503: {"model": HealthCheckResponse}},
)
async def redis_health_check():
    log = LOGGER.getChild("redis_health_check")
    log.info("Checking redis health")
    is_redis_up, error = check_redis_health()
    log.info(f"Redis health check response: {is_redis_up}, {error}")
    status_code = status.HTTP_200_OK
    if not is_redis_up or error:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    health = is_redis_up
    response = HealthCheckResponse(
        success=health, up=ServiceStatusType(postgres=True, redis=is_redis_up)
    )
    log.info(f"Redis health check response: {response}")
    return JSONResponse(content=response.model_dump(), status_code=status_code)
