from src.user.service import OperationType


class UserNotFound(Exception):
    def __init__(self, *args) -> None:
        self.message = 'User not found'


class OperationOutOfLimit(Exception):
    def __init__(self, operation: OperationType) -> None:
        self.operation = operation
        self.message = "Out of Limit"
