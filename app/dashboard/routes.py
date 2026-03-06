from flask import Blueprint, render_template, request, g, jsonify
from app.auth.routes import login_required
from app.utils.dynamodb import get_all_stocks
from . import bp

@bp.route('/')
@login_required
def index():
    stocks = get_all_stocks()
    # Mock data if no stocks exist in DB
    if not stocks:
        stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': '2800.00'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': '300.00'},
            {'symbol': 'AMZN', 'name': 'Amazon.com', 'price': '3400.00'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': '700.00'}
        ]
    return render_template('dashboard/index.html', stocks=stocks)

@bp.route('/api/search')
@login_required
def search():
    query = request.args.get('q', '').upper()
    stocks = get_all_stocks()
    if not stocks:
        stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': '2800.00'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': '300.00'},
            {'symbol': 'AMZN', 'name': 'Amazon.com', 'price': '3400.00'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': '700.00'}
        ]
    if query:
        stocks = [s for s in stocks if query in s['symbol'] or query in s['name'].upper()]
    return jsonify(stocks)
