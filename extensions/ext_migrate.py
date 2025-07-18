import flask_migrate


def init_app(app, db):
    flask_migrate.Migrate(app=app, db=db)
