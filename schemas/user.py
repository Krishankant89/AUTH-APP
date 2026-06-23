from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    roles: List[str] = []
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str