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

datos_climaticos = []

# Diccionario para mapear números de mes a nombres de mes
meses = {
    '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
    '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'
}


def crear_csv(fecha, temp_max, temp_min, condicion):
    # Guardar los datos en la lista
    datos_climaticos.append({
        'Fecha': fecha,
        'Temperatura Máxima': temp_max,
        'Temperatura Mínima': temp_min,
        'Condición Climática': condicion,
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
        WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Full Forecast')]"))
        ).click()

        # Navegar al calendario
        calendar_button = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(), 'Calendar')]"))
        )
        calendar_button.click()

        # Esperar a que el selector de año esté disponible
        year_selector = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "yearSelection"))
        )

        # Seleccionar el año 2023
        year_2023_option = year_selector.find_element(By.XPATH, "//option[text()='2023']")
        year_2023_option.click()
        time.sleep(2)

        # Esperar a que el botón "View" esté presente y hacer clic
        view_button = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='View' and @id='dateSubmit']"))
        )
        view_button.click()
        time.sleep(2)

        # Seleccionar y recorrer los meses
        for i in range(1, 13):  # Cambiar entre meses
            # Localizar nuevamente el selector de mes
            month_selector = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.ID, "monthSelection"))
            )
            month_option = month_selector.find_element(By.XPATH, f"//option[@value='{i}']")
            month_option.click()

            # Hacer clic en el botón "View"
            view_button = WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='View' and @id='dateSubmit']"))
            )
            view_button.click()

            # Esperar a que la página se actualice
            WebDriverWait(navegador, 15).until(EC.staleness_of(view_button))
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar-day"))
            )

            # Obtener la página actual con BeautifulSoup
            soup = BeautifulSoup(navegador.page_source, 'html.parser')
            calendar_days = soup.find_all('li', class_='calendar-day')

            for day in calendar_days:
                try:
                    # Extraer el día
                    fecha_div = day.find('div', class_='date')
                    dia = fecha_div.text.strip() if fecha_div else 'Desconocida'

                    # Crear la fecha completa (por ejemplo: "1 de enero de 2023")
                    fecha_completa = f"{dia} de {meses[str(i)]} de 2023"

                    # Extraer la temperatura máxima y mínima
                    temp_data = day.find('div', class_='temperature')
                    temp_max = temp_data.find('span', class_='hi').text.strip() if temp_data and temp_data.find('span', 'hi') else 'Desconocida'
                    temp_min = temp_data.find('span', class_='low').text.strip() if temp_data and temp_data.find('span', 'low') else 'Desconocida'

                    # Extraer la condición climática
                    condicion_div = day.find('div', class_='phrase')
                    condicion = condicion_div.text.strip() if condicion_div else 'Desconocida'

                    # Guardar los datos en el CSV
                    crear_csv(fecha_completa, temp_max, temp_min, condicion)

                except Exception as e:
                    print(f"Error al extraer datos de un día: {e}")

        # Procesar ahora el año 2024
        year_selector = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "yearSelection"))
        )
        year_2024_option = year_selector.find_element(By.XPATH, "//option[text()='2024']")
        year_2024_option.click()
        time.sleep(2)

        for i in range(1, 13):  # Cambiar entre meses
            # Seleccionar mes
            month_selector = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.ID, "monthSelection"))
            )
            month_option = month_selector.find_element(By.XPATH, f"//option[@value='{i}']")
            month_option.click()

            # Hacer clic en "View"
            view_button = WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='View' and @id='dateSubmit']"))
            )
            view_button.click()

            # Esperar a que se cargue el calendario
            WebDriverWait(navegador, 15).until(EC.staleness_of(view_button))
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar-day"))
            )

            # Extraer datos del año 2024
            soup = BeautifulSoup(navegador.page_source, 'html.parser')
            calendar_days = soup.find_all('li', class_='calendar-day')
            for day in calendar_days:
                try:
                    fecha_div = day.find('div', class_='date')
                    dia = fecha_div.text.strip() if fecha_div else 'Desconocida'
                    fecha_completa = f"{dia} de {meses[str(i)]} de 2024"
                    temp_data = day.find('div', class_='temperature')
                    temp_max = temp_data.find('span', class_='hi').text.strip() if temp_data and temp_data.find('span', 'hi') else 'Desconocida'
                    temp_min = temp_data.find('span', class_='low').text.strip() if temp_data and temp_data.find('span', 'low') else 'Desconocida'
                    condicion_div = day.find('div', class_='phrase')
                    condicion = condicion_div.text.strip() if condicion_div else 'Desconocida'
                    crear_csv(fecha_completa, temp_max, temp_min, condicion)
                except Exception as e:
                    print(f"Error al extraer datos de un día (2024): {e}")

    except Exception as e:
        print(f"Se produjo un error: {e}")

    finally:
        navegador.quit()

if __name__ == "__main__":
    clima()
