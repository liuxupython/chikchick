from flask_restful import Resource, reqparse

from controllers.auth import api


class LoginApi(Resource):

    def post(self):
        """Authenticate user and login."""
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, location="json")
        parser.add_argument("password", required=True, location="json")
        parser.add_argument("remember_me", type=bool, required=False, default=False, location="json")
        args = parser.parse_args()
        print(111)
        print(type(args), isinstance(args, dict))
        return {"result": "success", "data": ''}

from flask_login import current_user
api.add_resource(LoginApi, '/login')

