from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Lead(BaseModel):
    id: Optional[int] = Field(default=None)
    first_name: str
    last_name: str
    company: Optional[str]
    email: str
    phone: Optional[str]
    source: Optional[str]
    status: str
    notes: Optional[str]
    created: Optional[date]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "company": "Acme Corp",
                "email": "john@example.com",
                "phone": "+91-9876543210",
                "source": "website",
                "status": "new",
                "notes": "Interested in demo",
                "created": "2025-07-30"
            }
        }
    }
