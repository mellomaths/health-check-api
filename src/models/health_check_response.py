from pydantic import BaseModel


class ServiceStatusType(BaseModel):
    postgres: bool
    redis: bool


class HealthCheckResponse(BaseModel):
    success: bool
    up: ServiceStatusType
