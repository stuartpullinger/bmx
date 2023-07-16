import json

from bmx.core import DOCTYPE, Component
from bmx.htmltags import (
    article,
    html, 
    head, 
    title,
    img,
    body,
    div,
    a,
    main,
    p,
    script,
    style,
    button,
)
from flask import Flask
from markupsafe import Markup

app = Flask(__name__)

with open('users.json', 'r') as f:
    user_data = json.load(f)


@Component
def user_card(*,user):
    return (
        +article .card
            +div .card_image
                +img(src=f"https://picsum.photos/id/{user['id']}/200")
            -div
            +div .card_content
                +p +f"Name: " +user["name"] -p
                +p +f"Email: " +user["email"] -p
                +p +a(href=f"https://{user['website']}") +user["website"] -a -p
            -div
        -article
    )


@app.route('/users')
def users():
    return str(
        # fmt: off
        DOCTYPE.html
        +html
          +head
            +title +"User Component Demo" -title
            +script(src="https://unpkg.com/htmx.org@1.5.0") -script
            +style
                +Markup("""
                    .contents {
                        display: flex;
                        flex-wrap: wrap;
                        margin-left: 8px;
                        margin-right: 8px;
                    }  

                    .card {
                        flex-basis: 25%;
                        padding-left: 8px;
                        padding-right: 8px;
                    }
                """)
            -style
          -head
          +body
                +main .contents
                    +(user_card(user=user) for user in user_data)
                -main
          -body
        -html
        # fmt: on
    )

