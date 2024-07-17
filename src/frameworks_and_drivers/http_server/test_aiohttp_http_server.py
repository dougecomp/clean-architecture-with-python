from typing import AsyncGenerator, TypedDict
from unittest.mock import Mock
from aiohttp.test_utils import TestClient, TestServer
import pytest
import pytest_asyncio

from src.frameworks_and_drivers.http_server.aiohttp_http_server import AIOHttpHttpServer
from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_response import HttpResponse

default_controller_response = HttpResponse(status_code=200, body="Hello World!")


class SetUpType(TypedDict):
  http_server: AIOHttpHttpServer
  client: TestClient
  controller: HttpController

@pytest.fixture
async def set_up() -> AsyncGenerator[SetUpType, None]:
  controller_mock = Mock(HttpController)
  controller_mock.handle.return_value = default_controller_response
  http_server = AIOHttpHttpServer()
  client = TestClient(TestServer(http_server.app))
  yield {"http_server": http_server, "client": client, "controller": controller_mock}
  await client.close()

async def test_return_not_found_when_route_not_found(set_up: SetUpType):
  client = set_up["client"]
  await client.start_server()

  response = await client.get("/any_route")

  assert response.status == 404

async def test_return_controller_response_when_request_is_handled(set_up: SetUpType):
  controller_mock = set_up["controller"]
  http_server = set_up["http_server"]
  client = set_up["client"]
  http_server.register(route="/any_route", method="GET", controller=controller_mock)
  await client.start_server()

  response = await client.get("/any_route")

  assert response.status == default_controller_response.status_code
  assert await response.text() == default_controller_response.body