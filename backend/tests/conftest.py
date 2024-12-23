import pytest
from backend.app import create_app, db
from backend.auth.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('TestUser@2024Secure!')
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestUser@2024Secure!'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}