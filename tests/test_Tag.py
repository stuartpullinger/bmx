#!/usr/bin/env python

import pytest

from bmx.core import (
    BMXSyntaxError,
    EndTag,
    SelfClosingTag,
    SelfClosingTagStyle,
    StartTag,
    Tag,
)
from bmx.htmltags import h1, h2, meta


@pytest.fixture
def my_tag():
    return Tag("my-tag")


@pytest.fixture
def my_tag_with_attributes(my_tag):
    return Tag("my-tag", attr1="val1", attr2="val2")


@pytest.fixture
def my_tag_with_id_and_classes(my_tag):
    return Tag("my-tag", id_="title", class_=["heading", "uppercase"])


@pytest.fixture
def my_self_closing_tag():
    return SelfClosingTag("my-self-closing-tag", SelfClosingTagStyle.HTML)


def test_self_closing_tag_html_style():
    meta = SelfClosingTag("meta", SelfClosingTagStyle.HTML)
    assert str(meta) == "<meta>"


def test_self_closing_tag_xml_style():
    meta = SelfClosingTag("meta", SelfClosingTagStyle.XML)
    assert str(meta) == "<meta/>"


def test_self_closing_tag_with_attributes():
    meta = SelfClosingTag("meta", SelfClosingTagStyle.HTML, charset="UTF-8")
    assert str(meta) == '<meta charset="UTF-8">'


def test_self_closing_tag_with_boolean_attributes():
    meta = SelfClosingTag(
        "input", SelfClosingTagStyle.HTML, autofocus=True, disabled=False
    )
    assert str(meta) == "<input autofocus>"


def test_make_tag(my_tag):
    assert my_tag.name == "my-tag"


def test_pos_tag(my_tag):
    opening = +my_tag
    assert type(opening) == StartTag


def test_neg_tag(my_tag):
    closing = -my_tag
    assert type(closing) == EndTag


def test_keyword_args_as_attributes(my_tag):
    keyword_args_tag = my_tag(attr1="val1", attr2="val2")
    assert keyword_args_tag.attributes == {"attr1": "val1", "attr2": "val2"}


def test_shorthand(my_tag):
    my_tag_with_id_and_classes = my_tag("#title.heading.uppercase")
    assert my_tag_with_id_and_classes.attributes == {
        "id_": "title",
        "class_": ["heading", "uppercase"],
    }


def test_append_to_raw_tag_should_fail(my_tag):
    with pytest.raises(BMXSyntaxError):
        my_tag + my_tag


def test_append(my_tag):
    my_fragment = +my_tag + my_tag
    assert str(my_fragment) == "<my-tag><my-tag>"


def test_add_tag_on_the_right(my_tag):
    my_fragment = "Some content" + my_tag
    assert str(my_fragment) == "Some content<my-tag>"


def test_subtract_anything_not_a_tag_should_fail(my_tag):
    with pytest.raises(BMXSyntaxError):
        my_tag - "Some content"


def test_subtract_tag_from_tag(my_tag):
    my_fragment = "hello" - my_tag
    assert str(my_fragment) == "hello</my-tag>"


def test_subtract_already_set_tag_should_fail(my_tag, my_self_closing_tag):
    opener = +my_tag
    with pytest.raises(BMXSyntaxError):
        "Some content" - opener
    closer = -my_tag
    with pytest.raises(BMXSyntaxError):
        "Some content" - closer
    with pytest.raises(BMXSyntaxError):
        "Some content" - my_self_closing_tag


def test_subtract_already_set_tag_from_EndTag_should_fail(my_tag):
    t1 = -h1
    t2 = +h2
    with pytest.raises(BMXSyntaxError):
        t1 - t2


def test_subtract_already_set_tag_from_SelfClosingTag_should_fail(my_tag):
    t1 = meta(charset="utf-8")
    t2 = +h2
    with pytest.raises(BMXSyntaxError):
        t1 - t2


def test_str_tag(my_tag):
    with pytest.raises(BMXSyntaxError):
        str(my_tag)
    assert str(+my_tag) == "<my-tag>"
    assert str(-my_tag) == "</my-tag>"


def test_str_tag_with_attributes(my_tag_with_attributes):
    assert str(+my_tag_with_attributes) == '<my-tag attr1="val1" attr2="val2">'


def test_str_tag_with_id_and_classes(my_tag_with_id_and_classes):
    assert (
        str(+my_tag_with_id_and_classes)
        == '<my-tag id="title" class="heading uppercase">'
    )


def test_setting_class_twice(my_tag):
    tag_with_1_class = my_tag(class_="class1")
    tag_with_2_classes = tag_with_1_class(class_="class2")
    assert tag_with_2_classes.attributes["class_"] == ["class1", "class2"]


def test_keywords_arg_with_underscores_replaced_with_dashes(my_tag):
    tag_with_data_attribute = my_tag(data_bmx="some data")
    assert tag_with_data_attribute.attributes["data-bmx"] == "some data"
