import base64
from datetime import datetime, timedelta, timezone
import logging
import secrets
from typing import Optional
from werkzeug.exceptions import Unauthorized

from configs import config
from extensions.ext_redis import redis_client
from libs.password import hash_password, compare_password
from libs.passport import PassportService
from models.account import Account, AccountStatus, db
from services.errors.account import (
    AccountLoginError,
    AccountRegisterError,
)


class AccountService:

    @staticmethod
    def _get_login_cache_key(*, account_id: int, token: str) -> str:
        return f'account_login:{account_id}:{token}'

    @staticmethod
    def load_user(user_id: int) -> Optional[Account]:
        account = Account.query.filter_by(id=user_id).first()
        if not account:
            return None

        if account.status in {AccountStatus.BANNED.value, AccountStatus.CLOSED.value}:
            raise Unauthorized("Account is banned or closed.")

        # update last active time
        now_dt = datetime.now(timezone.utc).replace(tzinfo=None)
        if now_dt - account.last_active_at > timedelta(minutes=10):
            account.last_active_at = now_dt
            db.session.commit()

        return account

    @classmethod
    def load_logged_in_account(cls, *, account_id: int, token: str) -> Optional[Account]:
        if not redis_client.get(cls._get_login_cache_key(account_id=account_id, token=token)):
            return None
        return cls.load_user(account_id)

    @staticmethod
    def authenticate(email: str, password: str) -> Account:
        account = Account.query.filter_by(email=email).first()
        if not account:
            raise AccountLoginError("Invalid email")

        if account.status in {AccountStatus.BANNED.value, AccountStatus.CLOSED.value}:
            raise AccountLoginError("Account is banned or closed.")

        if account.password is None or not compare_password(password, account.password, account.password_salt):
            raise AccountLoginError("Invalid email or password.")
        return account

    @staticmethod
    def update_last_login(account: Account, *, ip_address: str) -> None:
        """Update last login time and ip"""
        account.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
        account.last_login_ip = ip_address
        db.session.add(account)
        db.session.commit()

    @staticmethod
    def get_account_jwt_token(account, *, exp: timedelta = timedelta(days=30)):
        payload = {
            "user_id": account.id,
            "exp": datetime.now(timezone.utc).replace(tzinfo=None) + exp,
            "iss": config.EDITION,
            "sub": "Console API Passport",
        }

        token = PassportService().encode(payload)
        return token

    @classmethod
    def login(cls, account: Account, *, ip_address: Optional[str] = None):
        if ip_address:
            AccountService.update_last_login(account, ip_address=ip_address)
        exp = timedelta(days=30)
        token = AccountService.get_account_jwt_token(account, exp=exp)
        redis_client.set(
            name=cls._get_login_cache_key(account_id=account.id, token=token),
            value="1",
            ex=int(exp.total_seconds())
        )
        return token

    @classmethod
    def logout(cls, *, account: Account, token: str):
        redis_client.delete(cls._get_login_cache_key(account_id=account.id, token=token))

    @staticmethod
    def create_account(email: str, name: str, password: str) -> Account:
        account = Account()
        account.email = email
        account.name = name

        # generate password salt
        salt = secrets.token_bytes(16)
        base64_salt = base64.b64encode(salt).decode()

        # encrypt password with salt
        password_hashed = hash_password(password, salt)
        base64_password_hashed = base64.b64encode(password_hashed).decode()

        account.password = base64_password_hashed
        account.password_salt = base64_salt

        db.session.add(account)
        db.session.commit()
        return account

    @classmethod
    def register(
            cls,
            email: str,
            name: str,
            password: str,
    ) -> Account:
        db.session.begin_nested()
        try:
            account = cls.create_account(email=email, name=name, password=password)
        except Exception as e:
            db.session.rollback()
            logging.error(f'Register failed: {e}')
            raise AccountRegisterError(f'Registration failed: {e}')

        return account
