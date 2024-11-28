import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
datos_climaticos=[]
def crear_csv(fecha, temp_max, temp_min, condicion, temporada):
    # Guardar los datos en la lista
    datos_climaticos.append({
        'Fecha': fecha,
        'Temperatura Máxima': temp_max,
        'Temperatura Mínima': temp_min,
        'Condición Climática': condicion,
        'Temporada': temporada
    })

    # Convertir la lista a un DataFrame de pandas
    df = pd.DataFrame(datos_climaticos)

    # Escribir el DataFrame en un archivo CSV (sin índice)
    df.to_csv('datos_climaticos/clima_tijuana.csv', index=False, mode='w', encoding='utf-8')
def clima():
    # Configurar el driver de Chrome
    driver = ChromeDriverManager().install()
    s = Service(driver)
    opc = Options()
    opc.add_argument("--window-size=1020,1200")
    navegador = webdriver.Chrome(service=s, options=opc)

    try:
        # Navegar a la página web
        navegador.get("https://www.wunderground.com/")
        time.sleep(15)

        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Full Forecast')]"))
        ).click()

        # Esperar a que el botón "CALENDAR" esté presente y hacer clic
        calendar_button = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(), 'Calendar')]"))
        )
        calendar_button.click()

        # Esperar a que el selector de año esté disponible
        year_selector = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "yearSelection"))
        )

        # Seleccionar el año 2024
        year_2024_option = year_selector.find_element(By.XPATH, "//option[text()='2024']")
        year_2024_option.click()

        # Esperar un momento para cargar los datos del año 2024
        time.sleep(2)

        # Seleccionar el año 2023
        year_2023_option = year_selector.find_element(By.XPATH, "//option[text()='2023']")
        year_2023_option.click()

        # Esperar un momento para cargar los datos del año 2023
        time.sleep(2)

        # Esperar a que el botón "View" esté presente y hacer clic
        view_button = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='View' and @id='dateSubmit']"))
        )
        view_button.click()  # Hacer clic en el botón "View"
        time.sleep(2)

        # Seleccionar los meses del año
        month_selector = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "monthSelection"))
        )
        for i in range(1, 13):  # Meses de enero a diciembre
            # Seleccionar el mes
            month_option = month_selector.find_element(By.XPATH, f"//option[@value='{i}']")
            month_option.click()
            time.sleep(2)

            # Reubicar y hacer clic en el botón "View" después de cada selección de mes
            #CHECAR ESTA FUNCION QUE ESTA MAL

#            view_button = WebDriverWait(navegador, 15).until(
#                EC.presence_of_element_located((By.XPATH, "//input[@value='View' and @id='dateSubmit']"))
#           )
#            view_button.click()
#            time.sleep(2)

        # Obtener la página actual con BeautifulSoup después de recorrer todos los meses
        soup = BeautifulSoup(navegador.page_source, 'html.parser')

        # Buscar todos los días dentro del calendario
        calendar_days = soup.find_all('li', class_='calendar-day')

        for day in calendar_days:
            try:
                # Extraer la fecha
                fecha = day.find('div', class_='header').text.strip()

                # Extraer la temperatura máxima y mínima
                temp_data = day.find('td', class_='temperature')
                temp_max = temp_data.find('span', class_='hi').text.strip()
                temp_min = temp_data.find('span', class_='low').text.strip()

                # Extraer la temperatura promedio
                temp_prom = temp_data.find_next('td', class_='temperature').text.strip()

                # Extraer la precipitación
                precip_data = day.find('td', class_='precipitation')
                precipitacion = precip_data.find('span', class_='wu-value').text.strip() if precip_data else '0'

                # Guardar los datos en el CSV
                crear_csv(fecha, temp_max, temp_min, temp_prom, precipitacion)

            except Exception as e:
                print(f"Error al extraer datos de un día: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

    finally:
        navegador.quit()

if __name__=="__main__":
    clima()
