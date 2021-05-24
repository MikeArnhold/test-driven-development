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
    service_id: int, service_request: BaseFormRequest, services: Dict[int, str]
) -> Dict[str, Any]:
    """Service view"""
    new = service_id not in services.keys()
    service_name = "" if new else services[service_id]
    if service_request.method == "POST":
        services[service_id] = service_request.form["name"]
    return dict(new=new, service_id=service_id, service_name=service_name)


if __name__ == "__main__":
    app.run(debug=True)
