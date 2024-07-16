from unittest.mock import Mock

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

def test_can_forward_query_params_to_controller():
  controllerMock = Mock(spec=HttpController)
  controllerMock.handle.return_value = HttpResponse(status_code=200, body='')
  api_server = FastApiHttpServer()
  api_server.register(method="GET", route="/any_route", controller=controllerMock)
  client = TestClient(api_server.app)

  client.get(url="/any_route?name=any_name")

  controllerMock.handle.assert_called_once_with({"name": "any_name"})

def test_can_forward_path_params_to_controller():
  controllerMock = Mock(spec=HttpController)
  controllerMock.handle.return_value = HttpResponse(status_code=200, body='')
  api_server = FastApiHttpServer()
  api_server.register(method="GET", route="/any_route/{name}", controller=controllerMock)
  client = TestClient(api_server.app)

  client.get(url="/any_route/any_name")

  controllerMock.handle.assert_called_once_with({"name": "any_name"})