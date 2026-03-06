from flask import Blueprint, render_template, g
from app.auth.routes import login_required
from app.utils.dynamodb import get_portfolio, get_all_stocks
from . import bp

@bp.route('/')
@login_required
def index():
    user_id = g.user['user_id']
    portfolio_items = get_portfolio(user_id)
    
    # We need current prices to calculate value
    stocks = get_all_stocks()
    # Mock data if DB is empty
    if not stocks:
        stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': '2800.00'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': '300.00'},
            {'symbol': 'AMZN', 'name': 'Amazon.com', 'price': '3400.00'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': '700.00'}
        ]
    
    prices = {s['symbol']: float(s['price']) for s in stocks}
    
    enriched_portfolio = []
    total_value = 0
    for item in portfolio_items:
        symbol = item['symbol']
        quantity = int(item['quantity'])
        current_price = prices.get(symbol, 0.0)
        value = quantity * current_price
        total_value += value
        
        enriched_portfolio.append({
            'symbol': symbol,
            'quantity': quantity,
            'current_price': current_price,
            'value': value
        })
        
    return render_template('portfolio/index.html', portfolio=enriched_portfolio, total_value=total_value)
