from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserAddress:
    address: str
    city: str
    state: str
    stateCode: str
    postalCode: str
    country: str
    coordinates: dict


@dataclass
class UserBank:
    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str


@dataclass
class UserCompany:
    department: str
    name: str
    title: str
    address: dict


@dataclass
class UserCrypto:
    coin: str
    wallet: str
    network: str


@dataclass
class User:
    id: int
    firstName: str
    lastName: str
    maidenName: str
    age: int
    gender: str
    email: str
    phone: str
    username: str
    password: str
    birthDate: str
    image: str
    bloodGroup: str
    height: float
    weight: float
    eyeColor: str
    hair: dict
    ip: str
    address: dict
    macAddress: str
    university: str
    bank: dict
    company: dict
    ein: str
    ssn: str
    userAgent: str
    crypto: dict
    role: str


@dataclass
class UserListResponse:
    users: list
    total: int
    skip: int
    limit: int


@dataclass
class CreateUserResponse:
    id: int
    firstName: str
    lastName: str


@dataclass
class UpdateUserResponse:
    id: int
    firstName: str
    lastName: str
