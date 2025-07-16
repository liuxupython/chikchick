from flask.blueprints import Blueprint

from libs.external_api import ExternalApi


bp = Blueprint('auth', __name__, url_prefix='/auth/api')
api = ExternalApi(bp)

from . import login

