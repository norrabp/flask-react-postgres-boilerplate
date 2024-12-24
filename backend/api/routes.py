from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.extensions.extensions import db, redis_client
from backend.auth.models import User
import json
import logging
from backend.tasks.compute_user_stats import compute_user_stats
from backend.tasks.test_redis_celery import test_redis_celery

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def root():
    """Root endpoint for API health check"""
    return jsonify({
        'message': 'Flask API is running',
        'status': 'healthy'
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    health_status = {
        'status': 'healthy',
        'components': {}
    }
    
    # Test database connection
    try:
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        health_status['components']['database'] = 'connected'
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        health_status['components']['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Test Redis connection
    try:
        redis_client.ping()
        health_status['components']['redis'] = 'connected'
        logger.info("Redis connection successful")
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        health_status['components']['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    return jsonify(health_status)

@api_bp.route('/test-task', methods=['POST'])
def trigger_test_task():
    task = test_redis_celery.delay()
    return jsonify({
        'task_id': task.id,
        'status': 'Task scheduled'
    })

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users, has_next_page = User.get_list()
    return jsonify({'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users],
        'has_next_page': has_next_page
    })

@api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics, computing them if not cached"""
    try:
        # Try to get stats from Redis cache
        cached_stats = redis_client.get('user_statistics')
        if cached_stats:
            return jsonify(json.loads(cached_stats))
        
        # If not cached, trigger background computation
        task = compute_user_stats.delay()
        return jsonify({
            'message': 'Computing statistics',
            'task_id': task.id
        })
    except Exception as e:
        logger.error(f"Error handling stats request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats/task/<task_id>', methods=['GET'])
@jwt_required()
def get_task_status(task_id):
    """Get the status of a background task"""
    task = compute_user_stats.AsyncResult(task_id)
    if task.ready():
        return jsonify({
            'status': 'completed',
            'result': task.get() if task.successful() else str(task.result)
        })
    return jsonify({
        'status': 'processing'
    })

# Task moved to tasks.py