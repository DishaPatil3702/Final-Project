# app/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# ----------------------------
# Schema for creating a new user
# ----------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# ----------------------------
# Schema for user login
# ----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------------------
# Schema for returning user data
# ----------------------------
class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
