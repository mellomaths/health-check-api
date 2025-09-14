import redis
from typing import Tuple, Optional

from infrastructure.logger import create_logger
from infrastructure.settings import Settings

LOGGER = create_logger(__name__)
REDIS_URL = Settings.load().redis.url


def get_redis_connection() -> redis.Redis:
    """
    Get a Redis connection instance.
    
    Returns
    -------
    redis.Redis
        A Redis connection instance.
    """
    log = LOGGER.getChild("get_redis_connection")
    log.info("Creating Redis connection")
    
    settings = Settings.load()
    redis_client = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
        db=settings.redis.database,
        decode_responses=True
    )
    
    return redis_client


def check_redis_health() -> Tuple[bool, Optional[str]]:
    """
    Check Redis health by attempting to ping the Redis server.
    
    Returns
    -------
    Tuple[bool, Optional[str]]
        A tuple containing:
        - bool: True if Redis is healthy, False otherwise
        - Optional[str]: Error message if Redis is not healthy, None otherwise
    """
    log = LOGGER.getChild("check_redis_health")
    log.info("Checking Redis health")
    
    is_redis_working = True
    error = None
    
    try:
        redis_client = get_redis_connection()
        # Ping Redis server to check connectivity
        redis_client.ping()
        log.info("Redis health check successful")
    except Exception as e:
        error = str(e)
        log.error(f"Error checking Redis health: {error}")
        is_redis_working = False
    
    return is_redis_working, error
