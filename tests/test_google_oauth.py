import pytest
from unittest.mock import patch, MagicMock

def test_google_login_redirect(client):
    response = client.get('/login/google')
    # Should redirect somewhere (either to Google if not logged in, or handled by flask-dance)
    assert response.status_code == 302
    location = response.headers.get('Location', '')
    assert 'accounts.google.com' in location or 'google' in location.lower() or '/login' in location

import app.auth.google_oauth

def test_google_authorized_callback(client, app):
    mock_google = MagicMock()
    mock_google.authorized = True
    
    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {'email': 'google_user@example.com'}
    mock_google.get.return_value = mock_resp

    # Overwrite the LocalProxy with our Mock to avoid proxy evaluation errors
    original_google = app.auth.google_oauth.google
    app.auth.google_oauth.google = mock_google

    try:
        response = client.get('/login/google/authorized')
        
        assert response.status_code == 302
        assert '/dashboard' in response.headers.get('Location', '')
        
        with client.session_transaction() as sess:
            assert 'user_id' in sess
    finally:
        app.auth.google_oauth.google = original_google
