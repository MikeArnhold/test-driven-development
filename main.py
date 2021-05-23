"""App routes"""
from flask import Flask

app = Flask("TDD")


@app.route("/")
def index():
    """Index view"""
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
