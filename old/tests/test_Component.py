#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from bmx.core import Component
from bmx.htmltags import a, body, div, h1, html, li, ul


@pytest.fixture
def my_component():
    @Component
    def my_component(*contents, **attributes):
        return +div(**attributes) + contents - div

    return my_component


def test_component():
    @Component
    def navbar(*contents, targets=None, **attributes):
        result = +ul(class_="navbar")
        if targets is not None:
            for target in targets:
                result += (
                    +li(class_=f"{target}")
                    + a(href=f"/{target}")
                    + target.capitalize()
                    - a
                    - li
                )
        result += -ul
        return result

    nav_targets = ("home", "about", "products", "contact")
    assert str(+navbar(targets=nav_targets) - navbar) == (
        '<ul class="navbar">'
        '<li class="home"><a href="/home">Home</a></li>'
        '<li class="about"><a href="/about">About</a></li>'
        '<li class="products"><a href="/products">Products</a></li>'
        '<li class="contact"><a href="/contact">Contact</a></li>'
        "</ul>"
    )


# def test_component_underscore_translates_to_minus(my_component):
#    assert my_component.name == "my-component"


def test_fragment_add_component(my_component):
    f = +html + body
    assert (
        str(f + my_component + h1 + "hello" - h1 - my_component)
        == "<html><body><div><h1>hello</h1></div>"
    )
