from flask import Flask, request, Response, jsonify

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer


class FlaskHttpServer(HttpServer):
  app: Flask

  def __init__(self):
    self.app = Flask(__name__)
    pass

  def __handle(
        self, controller: HttpController
    ):
        json = request.get_json() if request.method == "POST" else {}
        input = request.values.to_dict() | request.get_json() | json
        controller_output = controller.handle(input)
        response = jsonify(controller_output.body)
        response.status_code = controller_output.status_code
        response.default_mimetype = "application/json"
        return response

  def register(self, route: str, method: str, controller: HttpController):
    def handler():
      return self.__handle(
          controller=controller
      )
      
    self.app.add_url_rule(rule=route, endpoint=route, methods=[method], view_func=handler)
    pass