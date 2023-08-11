from typing import Union

from libcst import parse_module
import libcst.matchers as m
from bmx.transform import BmxTransformer

import pytest


@pytest.fixture
def bmxtransformer():
    return BmxTransformer()


def call_BmxElement_with(func: Union[m.SimpleString, m.Name], args: list, kwargs: dict):
    return m.Call(
        func=m.Name("BmxElement"),
        args=[
            m.Arg(func),
            m.Arg(m.List([m.Element(arg) for arg in args])),
            m.Arg(m.Dict([m.DictElement(key=k, value=v) for k, v in kwargs.items()])),
        ],
    )


@pytest.mark.parametrize(
    ("source", "ref", "contents", "attributes"),
    (
        pytest.param(
            '<span> "Hello World!" </span>',
            m.SimpleString("'span'"),
            [m.SimpleString('"Hello World!"')],
            {},
            id="simple html tag",
        ),
        pytest.param(
            '<my_component> "Hello Everyone!" </my_component>',
            m.Name("my_component"),
            [m.SimpleString('"Hello Everyone!"')],
            {},
            id="simple component"
        ),
        pytest.param(
            '<h1 autocapitalize="on"> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'autocapitalize'"): m.SimpleString('"on"')},
            id="simple attribute"
        ),
        pytest.param(
            '<h1 autocapitalize="on" role="heading"> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'autocapitalize'"): m.SimpleString('"on"'), m.SimpleString("'role'"): m.SimpleString('"heading"')},
            id="multiple attributes"
        ),
        pytest.param(
            '<h1 tabindex=5> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'tabindex'"): m.Integer("5")},
            id="Integer attribute value"
        ),
        pytest.param(
            '<h1 width=1.25> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'width'"): m.Float("1.25")},
            id="Float attribute value"
        ),
        pytest.param(
            '<h1 data_stuff=[1, "Hello", 45.6]> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'data_stuff'"): m.List([m.Element(m.Integer("1")), m.Element(m.SimpleString('"Hello"')), m.Element(m.Float("45.6"))])},
            id="List attribute value"
        ),
        pytest.param(
            '<h1 class="title big"> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'class'"): m.SimpleString('"title big"')},
            id="class attribute"
        ),
        pytest.param(
            '<h1 id="title"> "Hello World!" </h1>',
            m.SimpleString("'h1'"),
            [m.SimpleString('"Hello World!"')],
            {m.SimpleString("'id'"): m.SimpleString('"title"')},
            id="id attribute"
        ),
        pytest.param(
            '<p> <span> "Some text" </span> </p>',
            m.SimpleString("'p'"),
            [call_BmxElement_with(
                m.SimpleString("'span'"),
                [m.SimpleString('"Some text"')],
                {}
            )],
            {},
            id="simple nested html tags"
        )
    ),
)
def test_simple_tag(bmxtransformer, source, ref, contents, attributes):
    source = parse_module(source)
    transformed_source = source.visit(bmxtransformer)
    print(transformed_source)
    bmx_call = call_BmxElement_with(ref, contents, attributes)
    print(bmx_call)

    assert m.findall(transformed_source, bmx_call)
