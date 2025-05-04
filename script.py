import requests
from supabaseService import Supabase

def main():
    supabase = Supabase()
    url_liga = 'https://api.promiedos.com.ar/league/tables_and_fixtures/ebj'
    response = requests.get(url_liga)

    if response.status_code == 200:
        data = response.json()

        fixture = {
            'zona_a': data['tables_groups'][0]['tables'][0]['table']['rows'],
            'zona_b': data['tables_groups'][0]['tables'][1]['table']['rows']
        }

        supabase.upload_data('tabla_nacional', fixture)
        
    else:
        print(f"Error al obtener datos: {response.status_code}")

if __name__ == "__main__":
    main()
