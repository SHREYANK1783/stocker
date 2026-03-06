from flask import Blueprint, render_template, g
from app.auth.routes import login_required
from app.utils.dynamodb import get_transactions
from . import bp

@bp.route('/')
@login_required
def index():
    user_id = g.user['user_id']
    transactions = get_transactions(user_id)
    return render_template('history/index.html', transactions=transactions)
