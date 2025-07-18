import os
import time

from flask import Flask, request
from werkzeug.exceptions import Unauthorized

from configs import config

from extensions.ext_database import db
from extensions.ext_login import login_manager
from extensions import ext_database, ext_migrate, ext_redis, ext_login
from libs.passport import PassportService
from services.account_service import AccountService


os.environ['TZ'] = 'UTC'
# windows platform not support tzset
if hasattr(time, 'tzset'):
    time.tzset()


def create_flask_app_with_configs() -> Flask:
    """
    create a raw flask app
    with configs loaded from .env file
    """
    app = Flask(__name__)
    app.config.from_mapping(config.model_dump())
    return app


def register_extensions(app: Flask):
    ext_database.init_app(app)
    ext_migrate.init_app(app, db)
    ext_redis.init_app(app)
    ext_login.init_app(app)


def register_blueprints(app: Flask):
    from controllers.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


def create_app() -> Flask:
    app = create_flask_app_with_configs()

    app.secret_key = app.config['SECRET_KEY']

    register_extensions(app)
    register_blueprints(app)
    return app


@login_manager.request_loader
def load_user_from_request(*args):
    """Load user based on the request."""
    if request.blueprint not in {'auth'}:
        return None
    # Check if the user_id contains a dot, indicating the old format
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        auth_token = request.args.get("_token")
        if not auth_token:
            raise Unauthorized("Invalid Authorization token.")
    else:
        if " " not in auth_header:
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")
        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != "bearer":
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")

    decoded = PassportService().decode(auth_token)
    user_id = decoded.get("user_id")

    account = AccountService.load_logged_in_account(account_id=user_id, token=auth_token)
    return account


app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
