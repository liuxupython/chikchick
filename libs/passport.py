import jwt
from werkzeug.exceptions import Unauthorized

from configs import config


class PassportService:
    def __init__(self):
        self.sk = config.SECRET_KEY

    def encode(self, payload):
        return jwt.encode(payload, self.sk, algorithm="HS256")

    def decode(self, token):
        try:
            return jwt.decode(token, self.sk, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorized("Invalid token signature.")
        except jwt.exceptions.DecodeError:
            raise Unauthorized("Invalid token.")
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorized("Token has expired.")
