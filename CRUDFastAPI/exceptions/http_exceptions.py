from http import HTTPStatus
from typing import Union

from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        if not detail:  # pragma: no cover
            detail = HTTPStatus(status_code).description
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)  # pragma: no cover


class NotFoundException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)  # pragma: no cover


class ForbiddenException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)  # pragma: no cover


class UnauthorizedException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)  # pragma: no cover


class UnprocessableEntityException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers,
        )  # pragma: no cover


class DuplicateValueException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class RateLimitException(CustomException):
    def __init__(
        self,
        detail: Union[str, None] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers=headers,
        )  # pragma: no cover
