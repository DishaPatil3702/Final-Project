from fastapi import APIRouter, Query
from typing import Optional, List
from app.models.lead import Lead
from app.services.supabase_client import supabase

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.get("/", response_model=List[Lead])
def get_leads(
    status: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    limit: Optional[int] = Query(default=100)
):
    query = supabase.table("leads").select("*")

    if status:
        query = query.eq("status", status)

    result = query.execute()
    data = result.data

    if search:
        search_lower = search.lower()
        data = [
            lead for lead in data
            if search_lower in lead.get("first_name", "").lower()
            or search_lower in lead.get("last_name", "").lower()
            or search_lower in lead.get("email", "").lower()
        ]

    return data[:limit]

@router.post("/", response_model=Lead)
def create_lead(lead: Lead):
    lead_data = lead.dict(exclude_unset=True)

    # 🛠️ Convert `date` to string if present
    if "created" in lead_data and lead_data["created"]:
        lead_data["created"] = lead_data["created"].isoformat()

    result = supabase.table("leads").insert(lead_data).execute()
    return result.data[0] if result.data else {}
