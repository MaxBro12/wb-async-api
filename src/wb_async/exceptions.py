class WBException(Exception):
    pass


class IncorrectRequest(WBException):
    def __init__(self, status: int, adt_data: str):
        super().__init__(f"Incorrect request (status: {status}): {adt_data}")


class TooManyRequests(WBException):
    def __init__(self, adt_data: str):
        super().__init__(f"Too many requests: {adt_data}")


class WBAuthException(WBException):
    pass


class NotAuthorized(WBAuthException):
    def __init__(self, adt_data: str):
        super().__init__(f"Token scopes do not allow access: {adt_data}")


class AccessDenied(WBAuthException):
    def __init__(self, adt_data: str):
        super().__init__(f"Access denied: {adt_data}")


class PaymentRequired(WBAuthException):
    def __init__(self, adt_data: str):
        super().__init__(f"Payment required: {adt_data}")
