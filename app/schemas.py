
from pydantic import BaseModel, HttpUrl
from typing import List, Dict

class DestinationBase(BaseModel):
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    email: str
    account_name: str
    website: str = None

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    app_secret_token: str
    destinations: List[Destination] = []

    class Config:
        orm_mode = True
