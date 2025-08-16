# app/models/lead.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# ----------------------------
# Base Lead Schema
# ----------------------------
class LeadBase(BaseModel):
    first_name: str
    last_name: str
    company: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created: Optional[date] = None

# ----------------------------
# Create Lead Schema
# ----------------------------
class LeadCreate(LeadBase):
    """Schema for creating a lead — no ID or owner_email required."""
    pass

# ----------------------------
# Full Lead Schema
# ----------------------------
class Lead(LeadBase):
    id: Optional[int] = Field(default=None)
    owner_email: Optional[EmailStr] = None  # Set from current user automatically

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "company": "Acme Corp",
                "email": "john@example.com",
                "phone": "+91-9876543210",
                "source": "website",
                "status": "new",
                "notes": "Interested in demo",
                "created": "2025-07-30",
                "owner_email": "user@example.com"
            }
        }
    }
