import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# We can initialize a global resource or rely on current_app.dynamodb
# For standalone scripts, we use this:
def get_dynamodb_client():
    return boto3.client(
        'dynamodb',
        region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test')
    )

def create_table(dynamodb, table_name, key_schema, attribute_definitions, global_secondary_indexes=None):
    try:
        dynamodb.describe_table(TableName=table_name)
        print(f"Table '{table_name}' already exists.")
    except dynamodb.exceptions.ResourceNotFoundException:
        print(f"Creating table '{table_name}'...")
        params = {
            'TableName': table_name,
            'KeySchema': key_schema,
            'AttributeDefinitions': attribute_definitions,
            'BillingMode': 'PAY_PER_REQUEST'
        }
        if global_secondary_indexes:
            params['GlobalSecondaryIndexes'] = global_secondary_indexes
            
        dynamodb.create_table(**params)
        print(f"Table '{table_name}' creation initiated.")

def setup_tables():
    dynamodb = get_dynamodb_client()
    
    # 1. Users Table
    create_table(
        dynamodb,
        table_name='Users',
        key_schema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
        attribute_definitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        global_secondary_indexes=[
            {
                'IndexName': 'email-index',
                'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ]
    )

    # 2. Stocks Table
    create_table(
        dynamodb,
        table_name='Stocks',
        key_schema=[{'AttributeName': 'symbol', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'symbol', 'AttributeType': 'S'}]
    )

    # 3. Portfolios Table
    create_table(
        dynamodb,
        table_name='Portfolios',
        key_schema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'symbol', 'KeyType': 'RANGE'}
        ],
        attribute_definitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'symbol', 'AttributeType': 'S'}
        ]
    )

    # 4. Transactions Table
    create_table(
        dynamodb,
        table_name='Transactions',
        key_schema=[{'AttributeName': 'transaction_id', 'KeyType': 'HASH'}],
        attribute_definitions=[
            {'AttributeName': 'transaction_id', 'AttributeType': 'S'},
            {'AttributeName': 'user_id', 'AttributeType': 'S'}
        ],
        global_secondary_indexes=[
            {
                'IndexName': 'user_id-index',
                'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ]
    )

if __name__ == '__main__':
    setup_tables()
    print("Database setup complete.")
