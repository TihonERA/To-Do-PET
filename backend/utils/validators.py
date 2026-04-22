class DomainError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

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

class InvalidCredentialsError(DomainError):
    def __init__(self):
        super().__init__(detail="Invalid credentials", status_code=401)

def validate_pass(password: str):
    if len(password) < 16:
        raise ValidationError(detail="Password must be at least 16 characters")
    elif len(password) > 72:
        raise ValidationError("Password too long")
    
