def test_register_user(client):
    # Test case: Register a new user
    response = client.post('/api/register', json=dict(username='testuser', password='testpassword'))
    assert response.status_code == 200
    assert 'User registered successfully!' in str(response.json.get("message"))


def test_register_existing_user(client):
    # Register a user
    client.post('/api/register', json=dict(username='testuser', password='testpassword'))

    # Test case: Attempt to register an existing user
    response = client.post('/api/register', json=dict(username='testuser', password='newpassword'))
    assert response.status_code == 400
    assert 'User already exists!' in str(response.json.get("message"))


def test_login_user(client):
    # Register a user
    client.post('/api/register', json=dict(username='testuser', password='testpassword'))

    # Test case: Login an existing user
    response = client.post('/api/login', headers={'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3N3b3Jk'},
        content_type='application/json')
    assert response.status_code == 200
    assert 'token' in str(response.json.get("token"))


def test_login_non_existing_user(client):
    # Test case: Attempt to login a non-existing user
    response = client.post('/api/login', headers={'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3N3b3Jk'},
        content_type='application/json')
    assert response.status_code == 401
    assert 'Invalid credentials' in str(response.data)


def test_change_password(client):
    # Register a user
    client.post('/api/register', json=dict(username='testuser', password='testpassword'))

    # Login the registered user and get the token
    response_login = client.post('/api/login', headers={'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3N3b3Jk'},
        content_type='application/json')
    token = response_login.json.get('token')

    # Test case: Change the password of an existing user
    response_change_password = client.put('/api/change-password',
        json=dict(old_password='testpassword', new_password='newpassword'),
        headers={'Authorization': f'Bearer {token}'})
    assert response_change_password.status_code == 200
    assert 'Password changed successfully!' in str(response_change_password.json.get("message"))


def test_change_password_invalid_old_password(client):
    # Register a user
    client.post('/api/register', json=dict(username='testuser', password='testpassword'))

    # Login the registered user and get the token
    response_login = client.post('/api/login', headers={'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3N3b3Jk'},
        content_type='application/json')
    token = response_login.json.get('token')

    # Test case: Change the password with an invalid old password
    response_change_password = client.put('/api/change-password',
        json=dict(old_password='wrongpassword', new_password='newpassword'),
        headers={'Authorization': f'Bearer {token}'})
    assert response_change_password.status_code == 401
    assert 'Invalid old password' in str(response_change_password.json.get("message"))
