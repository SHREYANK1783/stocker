from flask import Blueprint

bp = Blueprint('history', __name__, url_prefix='/history')

from . import routes
