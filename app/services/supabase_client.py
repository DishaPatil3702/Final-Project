# app/services/supabase_client.py
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Logger setup
logger = logging.getLogger(__name__)

# Validate credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    missing = []
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    raise Exception(f"❌ Missing Supabase credentials: {', '.join(missing)}")

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Supabase client: {e}")
    raise
