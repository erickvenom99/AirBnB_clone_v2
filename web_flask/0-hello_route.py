#!/usr/bin/python3
"""
Module define a flask app
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """prints "Hello HBNB!" on the browser
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
