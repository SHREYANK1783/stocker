from flask import Blueprint, request, redirect, url_for, flash, g
from app.auth.routes import login_required
from app.utils.dynamodb import update_portfolio, create_transaction, get_portfolio_item
from . import bp

@bp.route('/place', methods=['POST'])
@login_required
def place():
    symbol = request.form['symbol']
    price = request.form['price']
    tx_type = request.form['type']
    
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        flash("Invalid quantity.")
        return redirect(url_for('dashboard.index'))

    if quantity <= 0:
        flash("Quantity must be greater than 0.")
        return redirect(url_for('dashboard.index'))

    user_id = g.user['user_id']

    if tx_type == 'buy':
        try:
            update_portfolio(user_id, symbol, quantity)
            create_transaction(user_id, symbol, 'buy', quantity, price)
            flash(f"Successfully bought {quantity} shares of {symbol}.")
        except Exception as e:
            flash(f"Error buying stock: {str(e)}")
            
    elif tx_type == 'sell':
        # Check if they have enough
        item = get_portfolio_item(user_id, symbol)
        current_qty = int(item['quantity']) if item else 0
        if current_qty < quantity:
            flash(f"Not enough shares to sell. You have {current_qty}.")
        else:
            try:
                update_portfolio(user_id, symbol, -quantity)
                create_transaction(user_id, symbol, 'sell', quantity, price)
                flash(f"Successfully sold {quantity} shares of {symbol}.")
            except Exception as e:
                flash(f"Error selling stock: {str(e)}")
    
    return redirect(url_for('portfolio.index'))
