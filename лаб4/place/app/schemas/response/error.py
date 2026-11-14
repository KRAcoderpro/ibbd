from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ErrorResponseSchema(BaseModel):
    detail: str


class UserNotFoundErrorSchema(ErrorResponseSchema):
    detail: str = "User not found"


class InvalidChatNameErrorSchema(ErrorResponseSchema):
    detail: str = "Chat name too short:6 symbols or more required"


class ChatNotFoundErrorSchema(ErrorResponseSchema):
    detail: str = "Chat not found"


class ChatDoesNotBelongToUserSchema(ErrorResponseSchema):
    detail: str = "Chat does not belong to user"


class DBClientErrorSchema(ErrorResponseSchema):
    detail: str = "Something went wrong"


class UserAlreadyExistsErrorSchema(ErrorResponseSchema):
    detail: str = "Email already registered"


class UserVerificationErrorSchema(ErrorResponseSchema):
    detail: str = "Incorrect username or password"


class UserNotFoundResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "User not found"}
        )


class InvalidChatNameResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Chat name too short: 6 symbols or more required"}
        )


class ChatNotFoundResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Chat not found"}
        )


class ChatDoesNotBelongToUserResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Chat does not belong to user"}
        )


class DBClientErrorResponse(JSONResponse):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail":  f"Something went wrong: {message}"}
        )


class UserAlreadyExistsResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Email already registered"}
        )


class UserVerificationResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Incorrect username or password"}
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token expired"

        )


class SellerTokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token expired"

        )


class TokenVerificationFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token verification failed"
        )


class SellerTokenVerificationFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token verification failed"
        )


class TokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token not found"
        )


class SellerTokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token not found"
        )


class AccessTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token exception"
        )


class SellerTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token exception"
        )
