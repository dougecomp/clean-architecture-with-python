from abc import ABC, abstractmethod

from src.interface_adapters.contracts.http_response import HttpResponse


class HttpController(ABC):
    @abstractmethod
    def handle(self, http_request) -> HttpResponse:
        pass
