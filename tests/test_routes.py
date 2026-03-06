def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log In' in response.data

def test_dashboard_redirect_if_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']
