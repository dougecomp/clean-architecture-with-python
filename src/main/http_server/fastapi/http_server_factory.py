from src.frameworks_and_drivers.http_server.fastapi_http_server import FastApiHttpServer
from src.interface_adapters.controllers.hello_world_controller import (
    HelloWorldController,
)


def makeHttpServer() -> FastApiHttpServer:
    http_server = FastApiHttpServer()
    http_server.register(
        route="/hello/{name}", method="GET", controller=HelloWorldController()
    )
    return http_server
