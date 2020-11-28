from bmx.core import DOCTYPE
from bmx.htmltags import (
    html, 
    head, 
    title,
    body,
    p
)
from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def greeter(name: str):
    return str(
        # fmt: off
        DOCTYPE.html
        +html
          +head
            +title +"Flask Greeter" -title
          -head
          +body
            +p +f"Hello {name}" -p
          -body
        -html
        # fmt: on
    )
