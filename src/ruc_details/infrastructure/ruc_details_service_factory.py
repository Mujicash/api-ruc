from ..domain.ruc_details_service import RucDetailService
from ..application.selenium_ruc_details_service import SeleniumRucDetailService


class RucDetailServiceFactory:
    @staticmethod
    def create(service_type: str) -> RucDetailService:
        if service_type == 'selenium':
            return SeleniumRucDetailService()
        else:
            raise ValueError(f'Service type {service_type} is not supported')
