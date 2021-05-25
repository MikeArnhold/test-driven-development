"""App routes"""
from typing import Any, Callable, Dict

from flask import Flask, redirect, url_for

from decorators import endpoint, parameters, template
from request import BaseFormRequest, CompleteRequest

app = Flask("TDD")

SERVICES: Dict[int, str] = {}


def _service_success_redirect(service_id):
    return redirect(url_for("endpoint_service", service_id=service_id))


endpoint_index = endpoint(app.route("/"), template("index.html"))
endpoint_service = endpoint(
    app.route("/service/<int:service_id>", methods=["GET", "POST"]),
    template("service.html"),
    parameters(
        service_request=CompleteRequest(),
        services=SERVICES,
        success_redirect=_service_success_redirect,
    ),
)


@endpoint_index
def index() -> Dict[str, str]:
    """Index view"""
    return dict(greeting="Hello, World!")


@endpoint_service
def service(
    service_id: int,
    service_request: BaseFormRequest,
    services: Dict[int, str],
    success_redirect: Callable[[int], Any],
) -> Dict[str, Any]:
    """Service view"""
    new = service_id not in services.keys()
    service_name = "" if new else services[service_id]
    if service_request.method == "POST":
        services[service_id] = service_request.form["name"]
        return success_redirect(service_id)
    return dict(new=new, service_id=service_id, service_name=service_name)


if __name__ == "__main__":
    app.run(debug=True)
