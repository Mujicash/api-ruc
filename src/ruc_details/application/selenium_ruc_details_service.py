from typing import List, Tuple

from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from ..domain.ruc_detail import RucDetail
from ..domain.ruc_detail_exceptions import InvalidRucException
from ..domain.ruc_details_service import RucDetailService


class SeleniumRucDetailService(RucDetailService):
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")
        self.chrome_service = Service(ChromeDriverManager().install())
        self.url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
        self.driver = webdriver.Chrome(service=self.chrome_service, options=self.chrome_options)
        self.driver_wait = WebDriverWait(self.driver, 10)

    def _get_ruc(self) -> Tuple[str, str]:
        element = self.driver_wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4"))
        )
        numero_ruc, razon_social = element.text.split(' - ', 1)

        return numero_ruc, razon_social

    def _get_tipo_contribuyente(self) -> str:
        element = self.driver_wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/p"))
        )
        tipo_contribuyente = element.text.split(' - ', 1)[0]

        return tipo_contribuyente

    def _get_nombre_comercial(self) -> str:
        element = self.driver_wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[3]/div/div[2]/p"))
        )
        nombre_comercial = element.text.split(' - ', 1)[0]

        return nombre_comercial

    def _get_domicilio_fiscal(self) -> str:
        element = self.driver_wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[2]/div[7]/div/div[2]/p"))
        )
        domicilio_fiscal = element.text.split(' - ', 1)[0]

        return domicilio_fiscal

    def _get_actividades_economicas(self) -> List[str]:
        element = self.driver_wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[3]/div[2]/div[10]/div/div[2]/table'))
        )

        rows = element.find_elements(By.XPATH, './/tbody/tr')

        actividades_economicas = []
        for row in rows:
            cells = row.find_elements(By.XPATH, './/td')
            for cell in cells:
                actividades_economicas.append(cell.text)

        return actividades_economicas

    def consultar_ruc(self, ruc: str) -> RucDetail:
        try:
            self.driver.get(self.url)

            txt_ruc = self.driver_wait.until(
                EC.presence_of_element_located((By.ID, "txtRuc"))
            )
            txt_ruc.send_keys(ruc)

            btn_aceptar = self.driver_wait.until(
                EC.presence_of_element_located((By.ID, "btnAceptar"))
            )
            btn_aceptar.click()

            self.driver_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "panel-primary"))
            )

            numero_ruc, razon_social = self._get_ruc()
            tipo_contribuyente = self._get_tipo_contribuyente()
            nombre_comercial = self._get_nombre_comercial()
            domicilio_fiscal = self._get_domicilio_fiscal()
            actividades_economicas = self._get_actividades_economicas()

            ruc_details = RucDetail(
                numero_ruc,
                razon_social,
                tipo_contribuyente,
                nombre_comercial,
                domicilio_fiscal,
                actividades_economicas
            )

            return ruc_details
        except UnexpectedAlertPresentException:
            raise InvalidRucException(ruc)
        finally:
            self.driver.quit()
