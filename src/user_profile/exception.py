from fastapi import HTTPException


class FormatsNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Formats not found')
