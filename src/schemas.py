from datetime import date
from pydantic import BaseModel, Field


class ContactIn(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str
    phone_number: str = Field(max_length=15)
    date_of_birth: date


class ContactOut(ContactIn):
    id: int


    class Config:
        orm_mode = True