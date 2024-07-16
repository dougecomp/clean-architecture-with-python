from unittest.mock import Mock

from src.interface_adapters.contracts.http_response import HttpResponse
from src.frameworks_and_drivers.http_server.flask_http_server import FlaskHttpServer

default_controller_response = HttpResponse(status_code=200, body="Hello World!")

def test_return_not_found_when_route_not_found():
    http_server = FlaskHttpServer()
    client = http_server.app.test_client()

    response = client.get("/any_route")

    assert response.status_code == 404

def test_return_controller_response_when_request_is_handled():
    http_server = FlaskHttpServer()
    client = http_server.app.test_client()

    controller_mock = Mock()
    controller_mock.handle.return_value = default_controller_response
    http_server.register(route="/any_route", method="GET", controller=controller_mock)

    response = client.get("/any_route", json={})

    assert response.status_code == default_controller_response.status_code
    assert response.get_json() == default_controller_response.body