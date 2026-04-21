class AlreadyTaken(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class NotFound(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class ValidationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

def validate_pass(password: str):
    if len(password) < 16:
        raise ValidationError(detail="Password must be at least 16 characters")
    elif len(password) > 72:
        raise ValidationError("Password too long")
    
