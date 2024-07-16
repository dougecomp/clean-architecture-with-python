from fastapi.testclient import TestClient

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_response import HttpResponse
from .fastapi_http_server import FastApiHttpServer

class ControllerSpy (HttpController):
  def handle(self, http_request):
    return HttpResponse(status_code=200, body='Hello World!')
  
def test_return_not_found_when_route_not_found():
  api_server = FastApiHttpServer()
  client = TestClient(api_server.app)

  response = client.get("/any_route")

  assert response.status_code == 404

def test_return_controller_response_when_request_is_handled():
  api_server = FastApiHttpServer()
  api_server.register(method="GET", route="/any_route", controller=ControllerSpy())
  client = TestClient(api_server.app)

  response = client.get(url="/any_route")

  assert response.status_code == 200
  assert response.json() == 'Hello World!'