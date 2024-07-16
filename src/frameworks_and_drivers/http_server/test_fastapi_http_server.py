from typing import Generator, TypedDict
from pytest import fixture
from unittest.mock import Mock

from fastapi.testclient import TestClient

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_response import HttpResponse
from src.interface_adapters.contracts.http_server import HttpServer
from .fastapi_http_server import FastApiHttpServer

class SetUpType (TypedDict):
  controller: Mock
  api_server: HttpServer
  client: TestClient

@fixture
def set_up() -> Generator[SetUpType, None, None]:
  controller_mock = Mock(HttpController)
  controller_mock.handle.return_value = HttpResponse(status_code=200, body='Hello World!')
  api_server = FastApiHttpServer()
  client = TestClient(api_server.app)
  yield {'controller': controller_mock, 'api_server': api_server, 'client': client}
  client.close()

def test_return_not_found_when_route_not_found(set_up):
  client = set_up['client']

  response = client.get("/any_route")

  assert response.status_code == 404

def test_return_controller_response_when_request_is_handled(set_up):
  controller_mock = set_up['controller']
  api_server = set_up['api_server']
  client = set_up['client']
  api_server.register(method="GET", route="/any_route", controller=controller_mock)

  response = client.get(url="/any_route")

  assert response.status_code == 200
  assert response.json() == 'Hello World!'

def test_can_forward_query_params_to_controller(set_up):
  controller_mock = set_up['controller']
  api_server = set_up['api_server']
  client = set_up['client']
  api_server.register(method="GET", route="/any_route", controller=controller_mock)

  client.get(url="/any_route?name=any_name")

  controller_mock.handle.assert_called_once_with({"name": "any_name"})

def test_can_forward_path_params_to_controller(set_up):
  controller_mock = set_up['controller']
  api_server = set_up['api_server']
  client = set_up['client']
  api_server.register(method="GET", route="/any_route/{name}", controller=controller_mock)

  client.get(url="/any_route/any_name")

  controller_mock.handle.assert_called_once_with({"name": "any_name"})

def test_can_forward_body_params_to_controller(set_up):
  controller_mock = set_up['controller']
  api_server = set_up['api_server']
  client = set_up['client']
  api_server.register(method="POST", route="/any_route", controller=controller_mock)

  client.post(url="/any_route", json={"name": "any_name"})

  controller_mock.handle.assert_called_once_with({"name": "any_name"})