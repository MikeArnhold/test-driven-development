"""App routes"""
from typing import Dict

from flask import Flask

app = Flask("TDD")


@app.route("/")
def index() -> Dict[str, str]:
    """Index view"""
    return dict(greeting="Hello, World!")


if __name__ == "__main__":
    app.run(debug=True)
