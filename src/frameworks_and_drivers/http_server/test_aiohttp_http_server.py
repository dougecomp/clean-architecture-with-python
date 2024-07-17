from typing import AsyncGenerator, TypedDict
from aiohttp.test_utils import TestClient, TestServer
import pytest
import pytest_asyncio

from src.frameworks_and_drivers.http_server.aiohttp_http_server import AIOHttpHttpServer

class SetUpType(TypedDict):
  http_server: AIOHttpHttpServer
  client: TestClient

@pytest_asyncio.fixture
async def set_up() -> AsyncGenerator[SetUpType, None]:
  http_server = AIOHttpHttpServer()
  client = TestClient(TestServer(http_server.app))
  yield {"http_server": http_server, "client": client}
  await client.close()

@pytest.mark.asyncio
async def test_return_not_found_when_route_not_found(set_up):
  client = set_up["client"]
  await client.start_server()

  response = await client.get("/any_route")

  assert response.status == 404  