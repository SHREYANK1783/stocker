from flask import Blueprint

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

from . import routes
