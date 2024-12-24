import os
import pytest
from backend.app import create_app, db
from backend.auth.models import User
import psycopg2
import time
import subprocess
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
import redis
from typing import Generator


def pytest_configure(config):
    """Set up test environment before any tests run"""
    os.environ['ENVIRONMENT'] = 'testing'

def wait_for_postgres(host: str, port: int, user: str, password: str, dbname: str, max_retries: int = 30) -> bool:
    """Wait for Postgres to become available with retries"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            if retry_count >= max_retries:
                return False
            time.sleep(1)
    return False

def wait_for_redis(host: str, port: int, max_retries: int = 30) -> bool:
    """Wait for Redis to become available with retries"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            r = redis.Redis(host=host, port=port)
            r.ping()
            r.close()
            return True
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            retry_count += 1
            if retry_count >= max_retries:
                return False
            time.sleep(1)
    return False

@pytest.fixture(scope="session")
def redis_client() -> Generator[redis.Redis, None, None]:
    """Create a Redis client for testing"""
    # Redis will be started by docker_compose_up fixture
    client = redis.Redis(host='localhost', port=6380)
    
    # Wait for Redis to be ready
    if not wait_for_redis(host='localhost', port=6380):
        raise Exception("Redis failed to become ready")
    
    yield client
    
    # Clear all data after tests
    client.flushall()
    client.close()

@pytest.fixture(autouse=True)
def clear_redis(redis_client):
    """Clear Redis data between tests"""
    redis_client.flushall()
    yield

# Update your existing docker_compose_up fixture to also check Redis
@pytest.fixture(scope="session", autouse=True)
def docker_compose_up() -> Generator[None, None, None]:
    """Start the test database and Redis using Docker Compose"""
    # Start containers
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"],
        check=True
    )

    # Wait for PostgreSQL to be ready
    if not wait_for_postgres(
        host="localhost",
        port=5433,
        user="postgres",
        password="postgres",
        dbname="postgres",
        max_retries=30
    ):
        subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down", "-v"])
        raise Exception("PostgreSQL failed to become ready")

    # Wait for Redis to be ready
    if not wait_for_redis(
        host="localhost",
        port=6380,
        max_retries=30
    ):
        subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down", "-v"])
        raise Exception("Redis failed to become ready")

    yield

    # Cleanup
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "down", "-v"],
        check=True
    )

@pytest.fixture(scope="function")
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    client = app.test_client()
    client.environ_base['CONTENT_TYPE'] = 'application/json'
    return client

@pytest.fixture(scope="function")
def test_user(app):
    user = User(
        username='unittestuser',
        email='unittesting@example.com'
    )
    user.set_password('TestUser@2024Secure!')
    user.create()
    return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    response = client.post('/auth/login', json={
        'email': 'unittesting@example.com',
        'password': 'TestUser@2024Secure!'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
