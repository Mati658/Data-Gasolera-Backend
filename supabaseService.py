from supabase import create_client, Client
import os

class Supabase:
    def __init__(self):
        SUPABASE_URL = os.environ['SUPABASE_URL']
        SUPABASE_KEY = os.environ['SUPABASE_KEY']
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def upload_data(self, columna, valor):
        response = (
            self.supabase.table("fixture")
            .update({columna: valor})
            .eq("id", 1)
            .execute()
        )

