import os
from dotenv import load_dotenv
from supabase import create_client, Client #SETUPCONNECTION

load_dotenv()  # loads .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL missing in .env")
if not SUPABASE_KEY:
    raise Exception("SUPABASE_KEY missing in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) #db connect 

def get_supabase_client() -> Client:
    return supabase

#loads Supabase credentials from environment variables, creates a single reusable database client