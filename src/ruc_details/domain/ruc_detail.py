from typing import List


class RucDetail:
    def __init__(self, numero_ruc: str, razon_social: str, tipo_contribuyente: str, nombre_comercial: str, domicilio_fiscal: str,
                 actividades_economicas: List[str]):
        self.numero_ruc = numero_ruc
        self.razon_social = razon_social
        self.tipo_contribuyente = tipo_contribuyente
        self.nombre_comercial = nombre_comercial
        self.domicilio_fiscal = domicilio_fiscal
        self.actividades_economicas = actividades_economicas

    def to_dict(self):
        return {
            'numero_ruc': self.numero_ruc,
            'razon_social': self.razon_social,
            'tipo_contribuyente': self.tipo_contribuyente,
            'nombre_comercial': self.nombre_comercial,
            'domicilio_fiscal': self.domicilio_fiscal,
            'actividades_economicas': self.actividades_economicas
        }
