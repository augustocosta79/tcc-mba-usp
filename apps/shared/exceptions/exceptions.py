class DomainError(Exception):
    """Base para erros de domínio da aplicação."""
    pass

class NotFoundError(DomainError):
    pass

class ConflictError(DomainError):
    pass

class UnauthorizedError(DomainError):
    pass

class UnprocessableEntityError(DomainError):
    pass

class OutOfStockError(DomainError):
    pass
