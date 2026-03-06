import uuid
from flask import current_app
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def get_table(table_name):
    return current_app.dynamodb.Table(table_name)

# --- USERS ---

def get_user_by_email(email):
    table = get_table('Users')
    response = table.query(
        IndexName='email-index',
        KeyConditionExpression=Key('email').eq(email)
    )
    items = response.get('Items', [])
    return items[0] if items else None

def get_user_by_id(user_id):
    table = get_table('Users')
    response = table.get_item(Key={'user_id': user_id})
    return response.get('Item')

def create_user(email, password_hash):
    table = get_table('Users')
    user_id = str(uuid.uuid4())
    user = {
        'user_id': user_id,
        'email': email,
        'password_hash': password_hash
    }
    table.put_item(Item=user)
    return user

# --- STOCKS ---

def get_all_stocks():
    table = get_table('Stocks')
    response = table.scan()
    return response.get('Items', [])

def get_stock(symbol):
    table = get_table('Stocks')
    response = table.get_item(Key={'symbol': symbol})
    return response.get('Item')

# --- PORTFOLIOS ---

def get_portfolio(user_id):
    table = get_table('Portfolios')
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response.get('Items', [])

def get_portfolio_item(user_id, symbol):
    table = get_table('Portfolios')
    response = table.get_item(Key={'user_id': user_id, 'symbol': symbol})
    return response.get('Item')

def update_portfolio(user_id, symbol, quantity_change):
    table = get_table('Portfolios')
    
    # Needs to handle atomicity using ADD or update if it exists
    item = get_portfolio_item(user_id, symbol)
    new_quantity = (item['quantity'] if item else 0) + quantity_change
    
    if new_quantity > 0:
        table.put_item(Item={
            'user_id': user_id,
            'symbol': symbol,
            'quantity': new_quantity
        })
    elif new_quantity == 0:
        if item:
            table.delete_item(Key={'user_id': user_id, 'symbol': symbol})
    else:
        raise ValueError("Not enough shares to sell.")
    
    return new_quantity

# --- TRANSACTIONS ---

def create_transaction(user_id, symbol, tx_type, quantity, price):
    table = get_table('Transactions')
    import datetime
    txn_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()
    
    item = {
        'transaction_id': txn_id,
        'user_id': user_id,
        'symbol': symbol,
        'type': tx_type,  # 'buy' or 'sell'
        'quantity': quantity,
        'price_at_execution': str(price),  # DynamoDB handles Decimal, but storing float as str is safer
        'timestamp': timestamp
    }
    table.put_item(Item=item)
    return item

def get_transactions(user_id):
    table = get_table('Transactions')
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    # Sort by timestamp descending
    items = response.get('Items', [])
    items.sort(key=lambda x: x['timestamp'], reverse=True)
    return items
