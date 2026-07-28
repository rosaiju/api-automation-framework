from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginSuccessResponse:
    accessToken: str
    refreshToken: str


@dataclass
class AuthUser:
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str
