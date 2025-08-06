from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials are missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
