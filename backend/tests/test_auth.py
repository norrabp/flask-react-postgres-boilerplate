from backend.auth.models import User

def test_register(client):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'TestUser@2024Secure!'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'

def test_register_duplicate_email(client, test_user):
    response = client.post('/auth/register', json={
        'username': 'another',
        'email': 'unittesting@example.com',
        'password': 'TestUser@2024Secure!'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_login_success(client, test_user):
    response = client.post('/auth/login', json={
        'email': 'unittesting@example.com',
        'password': 'TestUser@2024Secure!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    response = client.post('/auth/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert 'error' in response.json

def test_get_user_profile(client, auth_headers):
    response = client.get('/auth/me', headers=auth_headers)
    assert response.status_code == 200
    assert 'username' in response.json
    assert 'email' in response.json

def test_get_user_profile_unauthorized(client):
    response = client.get('/auth/me')
    assert response.status_code == 401
