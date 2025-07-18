from services.errors.base import BaseServiceError


class AccountNotFoundError(BaseServiceError):
    pass


class AccountRegisterError(BaseServiceError):
    pass


class AccountLoginError(BaseServiceError):
    pass


class CurrentPasswordIncorrectError(BaseServiceError):
    pass
