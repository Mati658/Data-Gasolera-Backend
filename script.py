from pytest import fixture
import requests
from supabaseService import Supabase

def main():
    supabase = Supabase()
    url_liga = 'https://webws.365scores.com/web/standings/?appTypeId=5&langId=14&timezoneName=America/Buenos_Aires&userCountryId=382&competitions=419&live=false&withSeasonsFilter=true'
    response = requests.get(url_liga)

    if response.status_code == 200:
        data = response.json()
        if data:
            fixture = {'zona_a': [], 'zona_b': []}

            for equipo in data['standings'][0]['rows']:
                
                if equipo['groupNum'] == 1:
                    agregar = {
                        'name': equipo['competitor']['name'],
                        'num': equipo['position'],
                        'points': equipo['points'],
                        'played': equipo['gamePlayed'],
                        'gfga': f"{equipo['for']} : {equipo['against']}",
                        'ratio': equipo['ratio'],
                        'wons': equipo['gamesWon'],
                        'even': equipo['gamesEven'],
                        'losts': equipo['gamesLost'],
                    }
                    fixture['zona_a'].append(agregar)
                else:
                    agregar = {
                        'name': equipo['competitor']['name'],
                        'num': equipo['position'],
                        'points': equipo['points'],
                        'played': equipo['gamePlayed'],
                        'gfga': f"{equipo['for']} : {equipo['against']}",
                        'ratio': equipo['ratio'],
                        'wons': equipo['gamesWon'],
                        'even': equipo['gamesEven'],
                        'losts': equipo['gamesLost'],
                    }
                    fixture['zona_b'].append(agregar)

            supabase.upload_data('tabla_nacional', fixture)
        else:
            print(f"ERROR, {url_liga} trae un JSON Vacío!")

    else:
        print(f"Error al obtener datos: {response.status_code}")

if __name__ == "__main__":
    main()
