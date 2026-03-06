import uuid
import datetime

# --- MOCK LOCAL DATABASE ---
MOCK_DB = {
    'Users': {},
    'Stocks': {},
    'Portfolios': {},
    'Transactions': {}
}

# --- USERS ---

def get_user_by_email(email):
    for u in MOCK_DB['Users'].values():
        if u['email'] == email:
            return u
    return None

def get_user_by_id(user_id):
    return MOCK_DB['Users'].get(user_id)

def create_user(email, password_hash):
    user_id = str(uuid.uuid4())
    user = {
        'user_id': user_id,
        'email': email,
        'password_hash': password_hash
    }
    MOCK_DB['Users'][user_id] = user
    return user

# --- STOCKS ---

def get_all_stocks():
    return list(MOCK_DB['Stocks'].values())

def get_stock(symbol):
    return MOCK_DB['Stocks'].get(symbol)

# --- PORTFOLIOS ---

def get_portfolio(user_id):
    return [p for p in MOCK_DB['Portfolios'].values() if p['user_id'] == user_id]

def get_portfolio_item(user_id, symbol):
    key = f"{user_id}_{symbol}"
    return MOCK_DB['Portfolios'].get(key)

def update_portfolio(user_id, symbol, quantity_change):
    key = f"{user_id}_{symbol}"
    item = get_portfolio_item(user_id, symbol)
    new_quantity = (item['quantity'] if item else 0) + quantity_change
    
    if new_quantity > 0:
        MOCK_DB['Portfolios'][key] = {
            'user_id': user_id,
            'symbol': symbol,
            'quantity': new_quantity
        }
    elif new_quantity == 0:
        if item:
            del MOCK_DB['Portfolios'][key]
    else:
        raise ValueError("Not enough shares to sell.")
    
    return new_quantity

# --- TRANSACTIONS ---

def create_transaction(user_id, symbol, tx_type, quantity, price):
    txn_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()
    
    item = {
        'transaction_id': txn_id,
        'user_id': user_id,
        'symbol': symbol,
        'type': tx_type,  # 'buy' or 'sell'
        'quantity': quantity,
        'price_at_execution': str(price),
        'timestamp': timestamp
    }
    MOCK_DB['Transactions'][txn_id] = item
    return item

def get_transactions(user_id):
    items = [t for t in MOCK_DB['Transactions'].values() if t['user_id'] == user_id]
    items.sort(key=lambda x: x['timestamp'], reverse=True)
    return items
