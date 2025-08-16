# app/services/supabase_client.py
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    missing = []
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    raise Exception(f"Missing Supabase credentials: {', '.join(missing)}")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
