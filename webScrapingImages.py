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
    option.add_argument("--headless")
    driver = Chrome(service=service, options=option)

    driver.get('https://www.promiedos.com.ar/league/primera-nacional/ebj')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    imagenes = soup.find_all('img', class_='table_table_team_image___vCP0')

    data = {
        'zona_a':[],
        'zona_b':[]
    }

    for item in imagenes:
        if len(data['zona_a']) <= 17:
            data['zona_a'].append({'name':item.get_attribute_list('alt')[0], 'url':item.get_attribute_list('src')[0]})
            continue

        data['zona_b'].append({'name':item.get_attribute_list('alt')[0], 'url':item.get_attribute_list('src')[0]})
        
        if len(data['zona_b']) == 18:
            break

    print(data)

    driver.quit()

    supabase.upload_data('imagenes', data)


if __name__ == "__main__":
    main()   
