from datetime import datetime, timedelta
import json
import logging
from backend.extensions.extensions import redis_client, celery
from backend.auth.models import User

logger = logging.getLogger(__name__)

@celery.task
def compute_user_stats():
    """Compute user statistics and cache them in Redis"""
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(deleted_at=None).count()
        recent_users = User.query.filter(
            User.created_at >= datetime.now() - timedelta(days=7)
        ).count()
        
        stats = {
            "total_users": total_users,
            "active_users": active_users,
            "recent_users": recent_users,
            "computed_at": datetime.now().isoformat()
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
