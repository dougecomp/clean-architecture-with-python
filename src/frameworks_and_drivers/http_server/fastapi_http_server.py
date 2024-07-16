from fastapi import FastAPI, Request, Response

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer


class FastApiHttpServer(HttpServer):
    def __init__(self):
        self.app = FastAPI()

    async def __handle(self, controller: HttpController, request: Request, response: Response):
        json = await request.json() if request.method == "POST" else {}
        input = request.path_params | request.query_params._dict | json
        controllerOutput = controller.handle(input)
        response.status_code = controllerOutput.status_code
        return controllerOutput.body

    def register(self, route: str, method: str, controller: HttpController):
        async def handler(request: Request, response: Response):
            return await self.__handle(controller=controller, request=request, response=response)

        self.app.add_api_route(
            path=route,
            endpoint=handler,
            methods=[method],
        )
