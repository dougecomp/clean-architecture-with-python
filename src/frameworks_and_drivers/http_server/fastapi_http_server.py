from fastapi import APIRouter, FastAPI, Response, Request

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer

class FastApiHttpServer (HttpServer):
  def __init__(self):
    self.app = FastAPI()

  def handle(self, controller: HttpController, request: Request, response: Response):
    input = request.path_params
    output = controller.handle(input)
    response.status_code = output.status_code
    return output.body

  def register(self, route: str, method: str, controller: HttpController):
    def handler(request: Request, response: Response):
      return self.handle(controller, request, response)
    
    self.app.add_api_route(
      path=route,
      endpoint=handler,
      methods=[method],
    )