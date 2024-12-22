from supabase import create_client, Client
import time
from datetime import datetime, date

import os
from dotenv import load_dotenv

from detect_screen_text import detect_text

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

for samples in range(500):

    timestamp = str(datetime.now()) 
    print("collecting text")
    text_reading = detect_text()

    print("posting text")
    response = (
        supabase.table("Text")
        .insert({"timestamp": timestamp, "text-reading": text_reading})
        .execute()
    )

    time.sleep(10)
