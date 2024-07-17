from aiohttp import web

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer


class AIOHttpHttpServer(HttpServer):
  app: web.Application
  def __init__(self):
    self.app = web.Application()

  async def __handle(
      self, controller: HttpController, request: web.Request
  ) -> web.Response:
    json = await request.json() if request.method == "POST" else {}
    query_params = {}
    path_params = {}
    input = query_params | path_params | json
    controller_output = controller.handle(input)
    return web.Response(body=controller_output.body, status=controller_output.status_code)

  def register(self, route: str, method: str, controller: HttpController):
    async def handler(request: web.Request):
        return await self.__handle(
            controller=controller,
            request=request
        )

    self.app.router.add_route(method, route, handler)