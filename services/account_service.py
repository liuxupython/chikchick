from typing import Optional

from models.account import Account


class AccountService:

    @staticmethod
    def login(account: Account, *, ip_address: Optional[str] = None):
        pass