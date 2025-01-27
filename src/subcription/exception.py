
class SubcriptionNotFound(Exception):
    def __init__(self) -> None:
        self.message = "Subcription Not Found"
