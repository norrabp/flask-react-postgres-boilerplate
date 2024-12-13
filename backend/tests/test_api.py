import pytest

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_get_users_unauthorized(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_get_users_authorized(client, auth_headers, test_user):
    response = client.get('/api/users', headers=auth_headers)
    assert response.status_code == 200
    users = response.json
    assert isinstance(users, list)
    assert len(users) > 0
    assert users[0]['username'] == test_user.username
    assert users[0]['email'] == test_user.email

def test_auth_header_missing(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_auth_header_invalid(client):
    headers = {'Authorization': 'Bearer invalid-token'}
    response = client.get('/api/users', headers=headers)
    assert response.status_code == 422
