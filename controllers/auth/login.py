from flask import request
import flask_login
from flask_restful import Resource, reqparse
from typing import cast

from controllers.auth import api
from libs.helper import get_remote_ip
from libs.login import login_required
from models.account import Account
from services.account_service import AccountService
from services.errors.account import AccountRegisterError, AccountLoginError


class RegisterApi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, location="json")
        parser.add_argument("email", required=True, location="json")
        parser.add_argument("password", required=True, location="json")
        parser.add_argument("re_password", required=True, location="json")
        args = parser.parse_args()

        if args['password'] != args['re_password']:
            return {"code": "password_not_match", "message": "密码不匹配"}, 400

        try:
            account = AccountService.register(
                email=args['email'],
                name=args['name'],
                password=args['password'],
            )
        except AccountRegisterError as e:
            return {"code": "register_error", "message": str(e)}, 401

        return {"result": "success"}


class LoginApi(Resource):

    def post(self):
        """Authenticate user and login."""
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, location="json")
        parser.add_argument("password", required=True, location="json")
        args = parser.parse_args()

        try:
            account = AccountService.authenticate(args["email"], args["password"])
        except AccountLoginError as e:
            return {"code": "unauthorized", "message": str(e)}, 401

        token = AccountService.login(account, ip_address=get_remote_ip(request))
        return {"result": "success", "data": token}


class LogoutApi(Resource):

    @login_required
    def get(self):
        account = cast(Account, flask_login.current_user)
        token = request.headers.get("Authorization", "").split(" ")[1]
        AccountService.logout(account=account, token=token)
        flask_login.logout_user()
        return {"result": "success"}


# bind api route
api.add_resource(RegisterApi, '/register')
api.add_resource(LoginApi, '/login')
api.add_resource(LogoutApi, '/logout')

