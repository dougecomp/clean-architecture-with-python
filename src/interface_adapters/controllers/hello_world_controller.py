from string import Template

from src.interface_adapters.contracts.http_controller import HttpController
from src.interface_adapters.contracts.http_response import HttpResponse


class HelloWorldController(HttpController):
    def handle(self, http_request) -> HttpResponse:
        greetings_template = Template("Hello $name!")
        name = http_request["name"]
        greetings = greetings_template.substitute(name=name)
        return HttpResponse(status_code=200, body=greetings)
