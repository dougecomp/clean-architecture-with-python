from fastapi import FastAPI, Request, Response

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer


class FastApiHttpServer(HttpServer):
    def __init__(self):
        self.app = FastAPI()

    def __handle(self, controller: HttpController, request: Request, response: Response):
        input = request.path_params
        controllerOutput = controller.handle(input)
        response.status_code = controllerOutput.status_code
        return controllerOutput.body

    def register(self, route: str, method: str, controller: HttpController):
        def handler(request: Request, response: Response):
            return self.__handle(controller=controller, request=request, response=response)

        self.app.add_api_route(
            path=route,
            endpoint=handler,
            methods=[method],
        )
