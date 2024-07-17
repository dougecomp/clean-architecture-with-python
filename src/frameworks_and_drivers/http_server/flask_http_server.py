from flask import Flask, request, jsonify, Response

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_server import HttpServer


class FlaskHttpServer(HttpServer):
    app: Flask

    def __init__(self):
        self.app = Flask(__name__)
        pass

    def __handle(self, controller: HttpController, path_params: dict = {}) -> Response:
        json = request.get_json() if request.is_json else {}
        query_params = request.args.to_dict()
        input = query_params | path_params | json
        controller_output = controller.handle(input)
        response = jsonify(controller_output.body)
        response.status_code = controller_output.status_code
        response.default_mimetype = "application/json"
        return response

    def register(self, route: str, method: str, controller: HttpController):
        def handler(*args, **kwargs):
            return self.__handle(controller=controller, path_params=kwargs)

        self.app.add_url_rule(
            route,
            methods=[method],
            view_func=handler,
        )
