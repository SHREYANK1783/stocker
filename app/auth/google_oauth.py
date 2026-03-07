import os
from flask import Blueprint, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from app.utils.dynamodb import get_user_by_email, create_user

# Create flask-dance Google blueprint
google_bp = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID', 'dummy_id'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', 'dummy_secret'),
    scope=["profile", "email"],
    redirect_to="google_auth_local.authorized"
)

# Create our own blueprint to handle the callback logic
bp = Blueprint('google_auth_local', __name__)

@bp.route('/login/google/authorized')
def authorized():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('Failed to fetch user info from Google.')
        return redirect(url_for('auth.login'))
        
    info = resp.json()
    email = info['email']
    
    user = get_user_by_email(email)
    if not user:
        # Create a user with a placeholder password (they will always log in via Google)
        create_user(email, "google_oauth_user")
        user = get_user_by_email(email)
        
    session.clear()
    session['user_id'] = user['user_id']
    return redirect(url_for('dashboard.index'))
