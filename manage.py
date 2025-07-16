from flask import Flask

from configs import config


def create_flask_app_with_configs() -> Flask:
    """
    create a raw flask app
    with configs loaded from .env file
    """
    app = Flask(__name__)
    app.config.from_mapping(config.model_dump())
    return app


def register_blueprints(app):
    from controllers.auth import bp as auth_bp

    app.register_blueprint(auth_bp)


def create_app() -> Flask:
    app = create_flask_app_with_configs()
    register_blueprints(app)
    return app


app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
