from fastapi import Request, status
from fastapi.responses import JSONResponse


class DomainException(Exception):
    """Base domain exception."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class CharacterNotFoundException(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Character '{identifier}' was not found in the database.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class MoveNotFoundException(DomainException):
    def __init__(self, move_id: int):
        super().__init__(
            message=f"Move with ID {move_id} was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class NotationParseException(DomainException):
    def __init__(self, token: str, reason: str):
        super().__init__(
            message=f"Failed to parse notation token '{token}': {reason}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_type": exc.__class__.__name__,
            "message": exc.message,
            "path": request.url.path
        }
    )
