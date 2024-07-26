#!/usr/bin/python3
"""
Module define a flask app
"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """prints "Hello HBNB!" on the browser
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display "HBNB" on the br
    """
    return "HBNB"


@app.route('/c/<text>')
def dynamic_c(text):
    """display "C" followed by a dynamic text
    """
    format_text = text.replace('_', ' ')
    return "C {}".format(format_text)


@app.route('/python', defaults={'text': 'is_cool'})
@app.route('/python/<text>')
def dynamic_python(text):
    """display "python" followed by a dynamic text
    """
    format_text = text.replace('_', ' ')
    return "Python {}".format(format_text)


@app.route('/number/<int:n>')
def is_number(n):
    """display “n is a number” only if n is an integer
    """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
