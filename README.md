import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def clima():
    driver = ChromeDriverManager()
    s = Service(driver.install())
    opc = Options()
    opc.add_argument("--window-size=1020,1200")
    navegador = webdriver.Chrome(service=s, options=opc)

    navegador.get("https://weather.com/es-MX/tiempo/hoy/l/MXDF0132:1:MX")
    time.sleep(10)

    # Encontrar y hacer clic en el apartado de "Mensual" del submenú
    monthly_link = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Mensual']"))
    )
    monthly_link.click()

    # Esperar a que el selector de año esté disponible
    year_selector = WebDriverWait(navegador, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label='Selector de año del calendario']"))
    )

    year_selector.find_element(By.CSS_SELECTOR, "option[value='2024']").click()

    option_2023 = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='2023']"))
    )
    option_2023.click()

    # Esperar a que el selector de mes esté disponible
    month_selector = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label='Selector de mes del calendario']"))
    )

    # Seleccionar el mes de marzo (value="2")
    month_selector.find_element(By.CSS_SELECTOR, "option[value='2']").click()

    navegador.quit()


if __name__ == "__main__":
    clima()
