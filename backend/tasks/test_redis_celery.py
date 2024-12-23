
from datetime import datetime
import logging

from backend.extensions.extensions import celery

logger = logging.getLogger(__name__)

@celery.task
def test_redis_celery():
    """Test task to verify Redis and Celery are working"""
    current_time = datetime.now().isoformat()
    logger.info(f"Test task executed at {current_time}")
    return f"Task completed successfully at {current_time}"