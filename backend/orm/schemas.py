from typing import Optional, List

from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    email: str
    location: str


class UserWholeInfo(UserRegister):
    id: int
    name: str
    email: str
    location: str
    weather: int


class EntityData(BaseModel):
    id: int
    name: str
    email: str
    weather: int
    location: str
    max_month: float
    min_month: float
    avg_month: float


class AllEntities(BaseModel):
    result: List[EntityData]
