from fastapi import HTTPException

from src.user.model import OperationType


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class OperationOutOfLimit(Exception):
    def __init__(self, operation: OperationType) -> None:
        self.operation = operation
        self.message = "Out of Limit"
