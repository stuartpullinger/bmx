#!/usr/bin/env python

import pytest

from bmx.core import (
    BMXSyntaxError,
    EndTag,
    Fragment,
    SelfClosingTag,
    SelfClosingTagStyle,
    StartTag,
    Tag,
)


@pytest.fixture
def start_html():
    return StartTag("html")


@pytest.fixture
def end_html():
    return EndTag("html")


def test_fragment_get_slice():
    hl = Tag("html")
    hd = Tag("head")
    m = SelfClosingTag("meta", SelfClosingTagStyle.HTML)
    b = Tag("body")
    p = Tag("p")

    f = +hl + hd + m - hd + b + p + "The Paragraph"
    assert str(f[3:5]) == "<p>The Paragraph"


def test_fragment_plus_untyped_tag():
    t = Tag("html")
    f = Fragment()
    assert str(f + t) == "<html>"


def test_fragment_plus_opening_tag(start_html):
    f = Fragment()
    assert str(f + start_html) == "<html>"


def test_fragment_plus_closing_tag(end_html):
    f = Fragment()
    assert str(f + end_html) == "</html>"


def test_fragment_plus_self_closing_tag():
    t = SelfClosingTag("meta", SelfClosingTagStyle.HTML)
    f = Fragment()
    assert str(f + t) == "<meta>"


def test_unbalanced_tags_fail(start_html):
    end_body = EndTag("body")
    f = Fragment() + start_html
    with pytest.raises(BMXSyntaxError):
        f + end_body


def test_self_closing_tag_inside_balanced_tags():
    head = Tag("head")
    meta = SelfClosingTag("meta", SelfClosingTagStyle.HTML)
    f = Fragment()
    assert str(f + head + meta - head) == "<head><meta></head>"


def test_fragment_plus_fragment(start_html, end_html):
    f1 = Fragment() + start_html
    f2 = Fragment() + end_html
    assert str(f1 + f2) == "<html></html>"


def test_fragment_plus_iterable(start_html, end_html):
    f = Fragment()
    i = (start_html, end_html)
    assert str(f + i) == "<html></html>"


def test_fragment_plus_non_string_non_iterable():
    f = Fragment()
    n = 123.456
    assert str(f + n) == "123.456"


def test_fragment_minus_tag():
    f = Fragment()
    html = Tag("html")
    assert str(f - html) == "</html>"
