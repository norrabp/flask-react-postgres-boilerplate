from backend.extensions.extensions import celery
from backend.auth.models import User
import logging

logger = logging.getLogger(__name__)

@celery.task
def cleanup_inactive_users():
    """Cleanup inactive users (dry run - logs only)"""
    try:
        inactive_users = User.query.filter_by(is_active=False).all()
        logger.info(f"Found {len(inactive_users)} inactive users")
        # Log instead of delete for safety
        for user in inactive_users:
            logger.info(f"Would clean up inactive user: {user.username}")
        return f"Found {len(inactive_users)} inactive users"
    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        return str(e)