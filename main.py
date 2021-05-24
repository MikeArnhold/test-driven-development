"""App routes"""
from typing import Any, Dict

from flask import Flask

from decorators import endpoint, template
from request import BaseFormRequest

app = Flask("TDD")


@endpoint(app.route("/"), template("index.html"))
def index() -> Dict[str, str]:
    """Index view"""
    return dict(greeting="Hello, World!")


@endpoint(app.route("/service/<int:service_id>"), template("service.html"))
def service(
    service_id: int, service_request: BaseFormRequest, services: Dict[str, Any]
) -> Dict[str, Any]:
    """Service view"""
    new = service_id not in services.keys()
    if service_request.method == "POST":
        services[service_id] = ""
    return dict(new=new)


if __name__ == "__main__":
    app.run(debug=True)
