import os
import time

from flask import Flask

from configs import config


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
    from extensions import (
        ext_database, ext_migrate, ext_redis, ext_login
    )

    extension_list = [
        ext_database,
        ext_migrate,
        ext_redis,
        ext_login,
    ]

    for ext in extension_list:
        ext.init_app(app)


def register_blueprints(app: Flask):
    from controllers.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


def create_app() -> Flask:
    app = create_flask_app_with_configs()

    app.secret_key = app.config['SECRET_KEY']

    register_extensions(app)
    register_blueprints(app)
    return app



app = create_app()
app.debug = True


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
