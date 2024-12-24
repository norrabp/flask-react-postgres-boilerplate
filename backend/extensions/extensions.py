from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from redis import Redis
from backend.config.environment import CONFIG

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

# Initialize Redis
redis_client = Redis.from_url(CONFIG.REDIS_URL)

# Initialize Celery
celery = Celery(__name__, broker=CONFIG.CELERY_BROKER_URL)
celery.conf.update(
    broker_url=CONFIG.CELERY_BROKER_URL,
    result_backend=CONFIG.REDIS_URL,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)
