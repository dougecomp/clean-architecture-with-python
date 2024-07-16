from src.frameworks_and_drivers.http_server.fastapi_http_server import FastApiHttpServer
from src.main.http_server.fastapi.http_server_factory import makeHttpServer

httpServer: FastApiHttpServer = makeHttpServer()
app = httpServer.app
