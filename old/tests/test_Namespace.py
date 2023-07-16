#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bmx.core import Namespace
from bmx.htmltags import body, h1, html


def test_namespace_with_prefix():
    xsl = Namespace(prefix="xsl:")
    stylesheet = (
        +xsl.stylesheet
        + xsl.template(match="/")
        + html
        + body
        + xsl.if_(test="price &gt; 10")
        + h1
        + "Very expensive"
        - h1
        - xsl.if_
        - body
        - html
        - xsl.template
        - xsl.stylesheet
    )
    assert str(stylesheet) == (
        '<xsl:stylesheet><xsl:template match="/">'
        '<html><body><xsl:if test="price &gt; 10">'
        "<h1>Very expensive</h1>"
        "</xsl:if></body></html>"
        "</xsl:template></xsl:stylesheet>"
    )


def test_namespace_with_prefix_and_translation():
    shoelace = Namespace(prefix="sl-")
    assert (
        str(+shoelace.icon_button(name="gear", disabled=True))
        == '<sl-icon-button name="gear" disabled>'
    )
