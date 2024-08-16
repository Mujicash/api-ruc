from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.headless = True
chrome_options.add_argument("--headless")

chrome_service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver_wait = WebDriverWait(driver, 10)
url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'

try:
    driver.get(url)

    txt_ruc = driver_wait.until(
        EC.presence_of_element_located((By.ID, "txtRuc"))
    )
    txt_ruc.send_keys("20518257723")

    btn_aceptar = driver_wait.until(
        EC.presence_of_element_located((By.ID, "btnAceptar"))
    )
    btn_aceptar.click()

    driver_wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "panel-primary"))
    )

    xpath_dict = {
        'numero_ruc': "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4",
        'tipo_contribuyente': "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/p",
        'nombre_comercial': "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[3]/div/div[2]/p",
        'domicilio_fiscal': "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[7]/div/div[2]/p"
    }

    extracted_values = {}

    # Extraer valores de cada XPath en el diccionario
    for key, xpath in xpath_dict.items():
        element = driver_wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        extracted_values[key] = element.text.strip()

    numero_ruc, razon_social = extracted_values['numero_ruc'].split(' - ', 1)
    extracted_values['numero_ruc'] = numero_ruc
    extracted_values['razon_social'] = razon_social

    tabla_actividades_economicas = driver_wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[3]/div[2]/div[10]/div/div[2]/table'))
    )

    row = tabla_actividades_economicas.find_elements(By.XPATH, './/tbody/tr')

    valores_tabla = []
    for fila in row:
        # Extraer el texto de cada celda en la fila
        cells = fila.find_elements(By.XPATH, './/td')
        for cell in cells:
            valores_tabla.append(cell.text)

    extracted_values['actividades_economicas'] = valores_tabla

    # Mostrar los valores extraídos
    print(extracted_values)
except UnexpectedAlertPresentException:
    print("Ruc invalido")
except Exception as e:
    print(f"Error durante la consulta: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
