from flask import Flask
import flask_migrate


def init_app(app: Flask):
    from extensions.ext_database import db

    flask_migrate.Migrate(app=app, db=db)
