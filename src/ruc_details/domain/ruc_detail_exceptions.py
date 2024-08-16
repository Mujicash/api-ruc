from ...shared.domain.api_exception import ApiException


class InvalidRucException(ApiException):
    def __init__(self, ruc: str):
        super().__init__(f"El RUC {ruc} no existe.", 404)
