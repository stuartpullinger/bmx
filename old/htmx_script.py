from bmx.core import DOCTYPE
from bmx.htmltags import (
    html, 
    head, 
    title,
    body,
    p,
    script,
    button,
)
from flask import Flask
from markupsafe import Markup

app = Flask(__name__)

@app.route('/<name>')
def greeter(name: str):
    return str(
        # fmt: off
        DOCTYPE.html
        +html
          +head
            +title +"HTMX Script Test" -title
            +script(src="https://unpkg.com/htmx.org@1.5.0") -script
          -head
          +body
                +button(**{'hx-get': '/get_script', 'hx-target': 'head', 'hx-swap': 'beforeend'})
                    +"Get Script"
                -button
          -body
        -html
        # fmt: on
    )


@app.route('/get_script')
def get_script():
    return str(
        +script
            +Markup('console.log("got script");')
        -script
    )

