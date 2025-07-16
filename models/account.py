
class Account:
    pass


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
db.init_app()