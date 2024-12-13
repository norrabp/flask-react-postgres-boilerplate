from datetime import datetime, timedelta
from celery import Celery
import json
import logging
from .extensions import redis_client, celery
from .models import User
from .extensions import db

logger = logging.getLogger(__name__)

@celery.task
def test_redis_celery():
    """Test task to verify Redis and Celery are working"""
    current_time = datetime.utcnow().isoformat()
    logger.info(f"Test task executed at {current_time}")
    return f"Task completed successfully at {current_time}"

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

@celery.task
def compute_user_stats():
    """Compute user statistics and cache them in Redis"""
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        recent_users = User.query.filter(
            User.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        stats = {
            "total_users": total_users,
            "active_users": active_users,
            "recent_users": recent_users,
            "computed_at": datetime.utcnow().isoformat()
        }
        
        # Cache the stats in Redis
        redis_client.setex(
            'user_statistics',
            timedelta(minutes=5),
            json.dumps(stats)
        )
        
        return stats
    except Exception as e:
        logger.error(f"Error computing stats: {str(e)}")
        return {
            "total_users": "Error",
            "active_users": "Error",
            "recent_users": "Error",
            "error": str(e)
        }
