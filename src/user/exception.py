from fastapi import HTTPException

from src.user.model import OperationType


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='User not found')


class OperationOutOfLimit(HTTPException):
    def __init__(self, operation: OperationType) -> None:
        detail = f"Operation '{operation.value}' is out of limit."
        super().__init__(status_code=400, detail=detail)


class NoActiveSubscription(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='User has no active subscription')
