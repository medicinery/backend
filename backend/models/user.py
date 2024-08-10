from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str
    dp: str
    name: str
    email: EmailStr
    dateCreated: datetime
    dateUpdated: datetime
    isVerified: bool
