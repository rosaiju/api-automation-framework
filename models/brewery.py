from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Brewery:
    id: str
    name: str
    brewery_type: str
    country: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    longitude: Optional[Union[str, float]] = None
    latitude: Optional[Union[str, float]] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None
