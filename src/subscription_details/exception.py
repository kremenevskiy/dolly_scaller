from fastapi import HTTPException


class SubscriptionNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Subscription not found')
