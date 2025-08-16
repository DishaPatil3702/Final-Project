# app/routes/lead.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime
from app.services.supabase_client import supabase
from app.routes.auth import get_current_user
from app.models.lead import Lead, LeadCreate  # ✅ Import models instead of redefining

router = APIRouter(
    prefix="/leads",  # ✅ Proper prefix for all lead routes
    tags=["Leads"]
)

# ----------------------------
# Get Leads
# ----------------------------
@router.get("/", response_model=List[Lead])
def get_leads(
    status: Optional[str] = Query(None, description="Filter by lead status"),
    search: Optional[str] = Query(None, description="Search by first name"),
    limit: int = Query(100, description="Max number of results"),
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
    lead_data["owner_email"] = current_user["email"]

    # ✅ Convert date/datetime objects to ISO string
    if isinstance(lead_data.get("created"), (date, datetime)):
        lead_data["created"] = lead_data["created"].isoformat()

    try:
        result = supabase.table("leads").insert(lead_data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lead: {str(e)}")
# ----------------------------
# Update Lead
# ----------------------------

from datetime import datetime, date

@router.put("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead: LeadCreate, current_user: dict = Depends(get_current_user)):
    lead_data = lead.dict(exclude_unset=True)

    # Convert 'created' date to string if it is a date object
    if "created" in lead_data and isinstance(lead_data["created"], date):
        lead_data["created"] = lead_data["created"].isoformat()

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

        # Convert Supabase date object to string before returning
        lead_response = result.data[0]
        if "created" in lead_response and isinstance(lead_response["created"], date):
            lead_response["created"] = lead_response["created"].isoformat()

        return lead_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update lead: {str(e)}")
# ----------------------------
# Delete Lead
# ----------------------------
@router.delete("/{lead_id}")
def delete_lead(lead_id: int, current_user: dict = Depends(get_current_user)):
    existing = supabase.table("leads").select("*").eq("id", lead_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    user_role = current_user.get("role", "Sales")
    if user_role != "Admin" and existing.data[0]["owner_email"] != current_user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this lead")
    
    try:
        supabase.table("leads").delete().eq("id", lead_id).execute()
        return {"message": "Lead deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lead: {str(e)}")
