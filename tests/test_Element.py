#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from bmx.core import BMXSyntaxError, Element, Fragment, Tag
from bmx.htmltags import span


@pytest.fixture
def h1():
    return Tag("h1")


@pytest.fixture
def my_element():
    return Element(
        "h1",
        "The Title",
        id_="title",
        class_=["heading", "uppercase"],
        disabled=True,
        contenteditable=False,
    )


def test_opening_and_closing_tags_make_element(h1):
    f = +h1 - h1
    assert isinstance(f[0], Element)


def test_pos_element_fails(my_element):
    with pytest.raises(BMXSyntaxError):
        +my_element


def test_neg_element_fails(my_element):
    with pytest.raises(BMXSyntaxError):
        -my_element


def test_add_tag_creates_fragment(my_element, h1):
    heading = +h1
    f = my_element + heading
    assert isinstance(f, Fragment) and list(f) == [my_element, heading]


def test_radd_tag_creates_fragment(my_element):
    text = "The Title"
    f = text + my_element
    assert isinstance(f, Fragment)


def test_sub_tag_creates_fragment(my_element, h1):
    f = my_element - h1
    assert isinstance(f, Fragment) and len(f) == 2


def test_sub_non_tag_fails(my_element):
    with pytest.raises(BMXSyntaxError):
        my_element - "some text"


def test_str_element(my_element):
    assert (
        str(my_element)
        == '<h1 id="title" class="heading uppercase" disabled>The Title</h1>'
    )


def test_markupsafe():
    username = "<script>callSomeDangerousJavascript();</script>"
    assert (
        str(+span + f"Username is: {username}" - span)
        == "<span>Username is: &lt;script&gt;callSomeDangerousJavascript();&lt;/script&gt;</span>"
    )
