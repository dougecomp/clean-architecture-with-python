from src.frameworks_and_drivers.http_server.fastapi_http_server import FastApiHttpServer
from src.interface_adapters.controllers.hello_world_controller import (
    HelloWorldController,
)

httpServer = FastApiHttpServer()
httpServer.register(
    route="/hello/{name}", method="GET", controller=HelloWorldController()
)
app = httpServer.app
