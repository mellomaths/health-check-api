from fastapi import APIRouter

from controllers.health_check_controller import router as health_check_api

router = APIRouter(redirect_slashes=False)

router.include_router(health_check_api)
