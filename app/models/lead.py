# app/models/lead.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# ----------------------------
# Base Lead Schema
# ----------------------------
class LeadBase(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    company: Optional[str] = Field(None, example="Acme Corp")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+91-9876543210")
    source: Optional[str] = Field(None, example="Website")
    status: str = Field(..., example="new")
    notes: Optional[str] = Field(None, example="Interested in demo")
    created: Optional[date] = Field(None, example="2025-08-16")

# ----------------------------
# Create Lead Schema
# ----------------------------
class LeadCreate(LeadBase):
    """Schema for creating a new lead — excludes ID and owner_email."""
    pass

# ----------------------------
# Full Lead Schema (DB Record)
# ----------------------------
class Lead(LeadBase):
    id: Optional[int] = Field(default=None, example=1)
    owner_email: Optional[EmailStr] = Field(None, example="user@example.com")

    class Config:
        from_attributes = True  # allows ORM → Pydantic
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "company": "Acme Corp",
                "email": "john@example.com",
                "phone": "+91-9876543210",
                "source": "Website",
                "status": "new",
                "notes": "Interested in demo",
                "created": "2025-08-16",
                "owner_email": "user@example.com"
            }
        }
