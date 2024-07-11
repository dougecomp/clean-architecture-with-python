from abc import ABC, abstractmethod

from src.interface_adapters.contracts.http_controller import HttpController

class HttpServer(ABC):

  @abstractmethod
  def register(
    self,
    route: str,
    method: str,
    controller: HttpController
  ):
    pass