from flask import request
import flask_login
from werkzeug.exceptions import Unauthorized

from libs.passport import PassportService
from services.account_service import AccountService


login_manager = flask_login.LoginManager()



def init_app(app):
    login_manager.init_app(app)



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
