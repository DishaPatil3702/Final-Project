# app/routes/lead.py

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date
from app.services.supabase_client import supabase
from app.routes.auth import get_current_user

router = APIRouter()

# ----------------------------
# Lead Models
# ----------------------------
class LeadBase(BaseModel):
    first_name: str
    last_name: str
    company: str
    email: EmailStr
    phone: str
    source: str
    status: str
    notes: Optional[str] = None
    created: date

class LeadCreate(LeadBase):
    """Schema for creating a lead (no ID or owner_email)"""
    pass

class Lead(LeadBase):
    """Schema for returning a lead (includes ID and owner_email)"""
    id: Optional[int] = None
    owner_email: EmailStr

# ----------------------------
# Get Leads
# ----------------------------
@router.get("/", response_model=List[Lead])
def get_leads(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    query = supabase.table("leads").select("*").eq("owner_email", current_user["email"])

    if status:
        query = query.eq("status", status)

    if search:
        query = query.ilike("first_name", f"%{search}%")

    result = query.limit(limit).execute()
    return result.data

# ----------------------------
# Create Lead
# ----------------------------
@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, current_user: dict = Depends(get_current_user)):
    lead_data = lead.dict(exclude_unset=True)
    lead_data["owner_email"] = current_user["email"]  # Set owner from token

    try:
        result = supabase.table("leads").insert(lead_data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# Update Lead
# ----------------------------
@router.put("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead: LeadCreate, current_user: dict = Depends(get_current_user)):
    lead_data = lead.dict(exclude_unset=True)

    try:
        result = (
            supabase.table("leads")
            .update(lead_data)
            .eq("id", lead_id)
            .eq("owner_email", current_user["email"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# Delete Lead
# ----------------------------
@router.delete("/{lead_id}")
def delete_lead(lead_id: int, current_user: dict = Depends(get_current_user)):
    try:
        result = (
            supabase.table("leads")
            .delete()
            .eq("id", lead_id)
            .eq("owner_email", current_user["email"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"message": "Lead deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
