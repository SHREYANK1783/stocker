import os
import boto3
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize DynamoDB client (attached to app to be accessible globally via current_app)
    # Note: For DynamoDB Local, you can set endpoint_url='http://localhost:8000'
    app.dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test')
    )
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)
    
    from .portfolio import bp as portfolio_bp
    app.register_blueprint(portfolio_bp)
    
    from .history import bp as history_bp
    app.register_blueprint(history_bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
