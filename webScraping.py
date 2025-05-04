import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from supabaseService import Supabase


def main():
    supabase = Supabase()
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--headless") #Para que corra minimizado
    driver = Chrome(service=service, options=option)

    driver.get('https://www.promiedos.com.ar/team/temperley/hbac')

    try:
        wait = WebDriverWait(driver, 10)
        botones_ver_mas = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_toggle_button__MNpwf')))
        for boton in botones_ver_mas:
            boton.click()
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".table-row.row_row__vWDV9.row_hover__9rdWJ")))

    except:
        print("No se encontró el botón 'Ver más' o no fue necesario.")

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    equipos = soup.find_all('tr', class_='table-row row_row__vWDV9 row_hover__9rdWJ')

    data = {
        'prox_partidos':[],
        'resultados':[]
    }

    for item in equipos:
        equipo = item.find_all('td')
        textos = [col.get_text(strip=True) for col in equipo]
        if textos[3].rfind(':') != -1:
            data['prox_partidos'].append({'dia':textos[0], 'L/V':textos[1], 'vs':textos[2], 'hora':textos[3]})
        else:
            data['resultados'].append({'dia':textos[0], 'L/V':textos[1], 'vs':textos[2], 'res':textos[3]})

    driver.quit()

    supabase.upload_data('partidos', data)


if __name__ == "__main__":
    main()   
