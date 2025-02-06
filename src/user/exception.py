from datetime import datetime

from fastapi import HTTPException

from src.user.model import OperationType


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='User not found')


class UserNotWhitelisted(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='User is not whitelisted')


class OperationOutOfLimit(HTTPException):
    def __init__(self, operation: OperationType) -> None:
        detail = f"Operation '{operation.value}' is out of limit."
        super().__init__(status_code=400, detail=detail)


class NoActiveSubscription(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='User has no active subscription')


class SubscripitonNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Subscription Not Found')


class OperationOutOfLimitWithPending(HTTPException):
    def __init__(
        self,
        operation: OperationType,
        current_limit: int,
        next_sub: datetime,
    ):
        self.operation = operation
        self.current_limit = current_limit
        self.next_sub = next_sub

        detail = f"Operation '{operation.value}' is out of limit."
        super().__init__(status_code=400, detail=detail)
