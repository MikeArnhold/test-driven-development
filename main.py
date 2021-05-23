"""App routes"""
from typing import Dict

from flask import Flask

from decorators import endpoint, template

app = Flask("TDD")


@endpoint(app.route("/"), template("index.html"))
def index() -> Dict[str, str]:
    """Index view"""
    return dict(greeting="Hello, World!")


if __name__ == "__main__":
    app.run(debug=True)
