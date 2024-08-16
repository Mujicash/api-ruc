from abc import ABC, abstractmethod

from .ruc_detail import RucDetail


class RucDetailService(ABC):
    @abstractmethod
    def consultar_ruc(self, ruc: str) -> RucDetail:
        pass
