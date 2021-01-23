#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# from __future__ import annotations         # Uncomment when dropping support for Python 3.6
from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from enum import Enum
from reprlib import recursive_repr
from typing import Any, Callable, List, Optional, Union

from markupsafe import escape

try:
    # >=3.8
    from functools import singledispatchmethod  # type: ignore
except ImportError:
    # <=3.7
    from singledispatchmethod import singledispatchmethod  # type: ignore


class SelfClosingTagStyle(Enum):
    HTML = ">"
    XML = "/>"

    def __str__(self: "SelfClosingTagStyle") -> str:
        return self.value


class AbstractTag(ABC):
    @abstractmethod
    def __add__(self: "AbstractTag", other: Any) -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'add' {other!r} to {self!r}. {self!r} tag is neither opening, self-closing or closing."
        )

    @abstractmethod
    def __radd__(self: "AbstractTag", other: Any) -> "Fragment":
        pass

    @abstractmethod
    def __pos__(self: "AbstractTag") -> "AbstractTag":
        pass

    @abstractmethod
    def __neg__(self: "AbstractTag") -> "AbstractTag":
        pass

    @abstractmethod
    def __sub__(self: "AbstractTag", other: Any) -> "Fragment":
        pass

    @abstractmethod
    def __rsub__(self: "AbstractTag", other: Any) -> "Fragment":
        pass

    @abstractmethod
    def __call__(
        self: "AbstractTag", shorthand: Optional[str], **attributes: Any
    ) -> "AbstractTag":
        pass


class Tag(AbstractTag):
    def __init__(self: "Tag", _name: str, **_kwargs: Any) -> None:
        self.name = _name
        self.attributes = _kwargs if _kwargs else {}

    def create_start_tag(self: "Tag") -> "StartTag":
        return StartTag(self.name, **self.attributes)

    def __pos__(self: "Tag") -> "StartTag":
        return self.create_start_tag()

    def __neg__(self: "Tag") -> "EndTag":
        return EndTag(self.name)

    def __call__(self: "Tag", shorthand: Optional[str] = None, **kwargs: Any) -> "Tag":

        new_attributes = self.attributes.copy()

        # parse class/id shorthand
        if shorthand is not None:
            classes = shorthand.split(".")
            if classes[0].startswith("#"):
                new_attributes["id_"] = classes[0][1:]
                del classes[0]
            if classes:
                if new_attributes.get("class_", None) is None:
                    new_attributes["class_"] = []
                new_attributes["class_"].extend(classes)

        # add attributes
        new_attributes.update(kwargs)

        #        if isinstance(self, ComponentTag):
        #            return type(self)(self.name, self.render, **new_attributes)
        #        else:
        return type(self)(self.name, **new_attributes)

    def __add__(self: "Tag", other: Any) -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'add' {other!r} to {self!r}. {self!r} tag has not had it's TagType set"
        )

    def __radd__(self: "Tag", other: Any) -> "Fragment":
        return Fragment(other) + self

    def __sub__(self: "Tag", other: "Tag") -> "Fragment":
        if isinstance(other, Tag) and type(other) not in [
            StartTag,
            EndTag,
            SelfClosingTag,
        ]:
            return Fragment(self) - other
        else:
            raise BMXSyntaxError(
                f"Cannot 'subtract' {other!r} of type {type(other)!r} from {self!r}. "
                "Only Tags can be 'subtracted'"
            )

    def __rsub__(self: "Tag", other: Any) -> "Fragment":
        return Fragment(other) - self

    def __getattr__(self: "Tag", attr: str) -> "Tag":
        dashed_attr = attr.replace("_", "-")
        new_attributes = self.attributes.copy()
        if new_attributes.get("class_", None) is None:
            new_attributes["class_"] = []
        new_attributes["class_"].append(dashed_attr)

        #        if isinstance(self, ComponentTag):
        #            return type(self)(self.name, self.render, **new_attributes)
        #        else:
        return type(self)(self.name, **new_attributes)

    def __repr__(self: "Tag") -> str:
        attrs_repr = repr(self.attributes) if self.attributes else ""
        return "".join(
            (
                "<Tag:",
                self.name,
                "|",
                hex(id(self)),
                " ",
                attrs_repr,
                ">",
            )
        )

    def __str__(self: "Tag") -> str:
        raise BMXSyntaxError(
            f"Cannot stringify {self!r} as the Tag type has not been set"
        )


class StartTag(Tag):
    def __init__(
        self: "StartTag",
        _name: str,
        **_kwargs: Any,
    ) -> None:
        self.name = _name
        self.attributes = _kwargs if _kwargs else {}

    def render(self: "StartTag", *_contents: Any, **_attributes: Any) -> "Element":
        return Element(self.name, *_contents, **_attributes)

    def __pos__(self: "StartTag") -> "StartTag":
        raise BMXSyntaxError(
            f"Cannot ' + ' {self.name} Tag as the TagType is already set at {self!r}"
        )

    def __neg__(self: "StartTag") -> "EndTag":
        raise BMXSyntaxError(
            f"Cannot ' - ' {self.name} Tag as the TagType is already set at {self!r}"
        )

    def __add__(self: "StartTag", other: Any) -> "Fragment":
        return Fragment(self) + other

    def __radd__(self: "StartTag", other: Any) -> "Fragment":
        return Fragment(other) + self

    def __sub__(self: "StartTag", other: "Tag") -> "Fragment":
        if isinstance(other, Tag) and type(other) not in [
            StartTag,
            EndTag,
            SelfClosingTag,
        ]:
            return Fragment(self) - other
        else:
            raise BMXSyntaxError(
                f"Cannot 'subtract' {other!r} of type {type(other)!r} from {self!r}. "
                "Only Tags can be 'subtracted'"
            )

    def __rsub__(self: "StartTag", other: Any) -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'subtract' {self!r} tag from {other!r} as {self.name} is already an StartTag"
        )

    def __repr__(self: "StartTag") -> str:
        attrs_repr = repr(self.attributes) if self.attributes else ""
        return "".join(
            (
                "<StartTag:",
                self.name,
                "|",
                hex(id(self)),
                " ",
                attrs_repr,
                ">",
            )
        )

    def __str__(self: "StartTag") -> str:
        begin = "<"
        end = ">"

        if self.attributes:
            attributes: List[str] = []
            for key, value in self.attributes.items():
                if str(key).endswith("_"):  # ie. for_, id_, class_
                    key = key[:-1]
                if value is True:
                    attributes.extend(" " + key)
                    continue
                elif value is False:
                    continue
                elif isinstance(value, list):
                    value = " ".join(value)

                attributes.extend(" " + str(key) + '="' + str(value) + '"')
        else:
            attributes = []

        return "".join((begin, self.name, *attributes, end))


class EndTag(Tag):
    def __init__(self: "EndTag", _name: str) -> None:
        self.name = _name

    def __pos__(self: "EndTag") -> "StartTag":
        raise BMXSyntaxError(
            f"Cannot ' + ' {self.name} Tag as the TagType is already set at {self!r}"
        )

    def __neg__(self: "EndTag") -> "EndTag":
        raise BMXSyntaxError(
            f"Cannot ' - ' {self.name} Tag as the TagType is already set at {self!r}"
        )

    def __add__(self: "EndTag", other: "Tag") -> "Fragment":
        return Fragment(self) + other

    def __radd__(self: "EndTag", other: Any) -> "Fragment":
        return Fragment(other) + self

    def __sub__(self: "EndTag", other: "Tag") -> "Fragment":
        if isinstance(other, Tag) and type(other) not in [
            StartTag,
            EndTag,
            SelfClosingTag,
        ]:
            return Fragment(self) - other
        else:
            raise BMXSyntaxError(
                f"Cannot 'subtract' {other!r} of type {type(other)!r} from {self!r}. "
                "Only Tags can be 'subtracted'"
            )

    def __rsub__(self: "EndTag", other: Any) -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'subtract' {self!r} tag from {other!r} as {self.name} is already an EndTag"
        )

    def __repr__(self: "EndTag") -> str:
        return "".join(
            (
                "<EndTag:",
                self.name,
                "|",
                hex(id(self)),
                ">",
            )
        )

    def __str__(self: "EndTag") -> str:
        begin = "</"
        end = ">"

        return "".join((begin, self.name, end))


class SelfClosingTag(Tag):
    def __init__(
        self: "SelfClosingTag",
        _name: str,
        _self_closing_tag_style: SelfClosingTagStyle = SelfClosingTagStyle.XML,
        **_kwargs: Any,
    ) -> None:
        self.name = _name
        self.attributes = _kwargs if _kwargs else {}
        self._self_closing_tag_style = _self_closing_tag_style

    # TODO: is *_contents needed here?
    def render(
        self: "SelfClosingTag", *_contents: Any, **_attributes: Any
    ) -> "Element":
        return Element(self.name, **_attributes)

    def __pos__(self: "SelfClosingTag") -> "StartTag":
        raise BMXSyntaxError(
            f"Cannot ' + ' {self.name} Tag as the Tag type is already set at {self!r}"
        )

    def __neg__(self: "SelfClosingTag") -> "EndTag":
        raise BMXSyntaxError(
            f"Cannot ' - ' {self.name} Tag as the Tag type is already set at {self!r}"
        )

    def __add__(self: "SelfClosingTag", other: Any) -> "Fragment":
        return Fragment(self) + other

    def __radd__(self: "SelfClosingTag", other: Any) -> "Fragment":
        return Fragment(other) + self

    def __sub__(self: "SelfClosingTag", other: "Tag") -> "Fragment":
        if isinstance(other, Tag) and type(other) not in [
            StartTag,
            EndTag,
            SelfClosingTag,
        ]:
            return Fragment(self) - other
        else:
            raise BMXSyntaxError(
                f"Cannot 'subtract' {other!r} of type {type(other)!r} from {self!r}. "
                "Only Tags can be 'subtracted'"
            )

    def __rsub__(self: "SelfClosingTag", other: "Tag") -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'subtract' {self!r} tag from {other!r} as {self.name} is already an StartTag"
        )

    def __repr__(self: "SelfClosingTag") -> str:
        attrs_repr = repr(self.attributes) if self.attributes else ""
        return "".join(
            (
                "<SelfClosingTag:",
                self.name,
                "|",
                hex(id(self)),
                " ",
                attrs_repr,
                ">",
            )
        )

    def __str__(self: "SelfClosingTag") -> str:
        begin = "<"
        end = str(self._self_closing_tag_style)

        if self.attributes:
            attributes: List[str] = []
            for key, value in self.attributes.items():
                if str(key).endswith("_"):  # ie. for_, id_, class_
                    key = key[:-1]
                if value is True:
                    attributes.extend(" " + key)
                    continue
                elif value is False:
                    continue
                elif isinstance(value, list):
                    value = " ".join(value)

                attributes.extend(" " + str(key) + '="' + str(value) + '"')
        else:
            attributes = []

        return "".join((begin, self.name, *attributes, end))


def Component(func: Callable) -> Tag:
    class RenderMixin(ABC):
        def render(self: "RenderMixin", *args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

    class StartComponentTag(RenderMixin, StartTag):
        def __init__(
            self: "StartComponentTag",
            _name: str,
            #            render: Callable,
            **_attributes: Any,
        ) -> None:
            super().__init__(_name, **_attributes)
            # setattr(self, "render", render)
            # self.render = render

    class ComponentTag(Tag):
        def __init__(
            self: "ComponentTag",
            _name: str,
            #            render: Callable,
            **_attributes: Any,
        ) -> None:
            super().__init__(_name, **_attributes)
            # setattr(self, "render", render)
            # self.render = render

        def create_start_tag(self: "ComponentTag") -> StartComponentTag:
            return StartComponentTag(self.name, **self.attributes)

    new_tag = ComponentTag(func.__name__.replace("_", "-"))
    return new_tag


class BMXSyntaxError(SyntaxError):
    pass


class Element:
    def __init__(
        self: "Element", _name: str, *_contents: Any, **_attributes: Any
    ) -> None:
        self.name = _name
        self.contents = list(_contents)
        self.attributes = _attributes

    def __pos__(self: "Element") -> None:
        raise BMXSyntaxError(f"Cannot ' + ' an Element at {self!r}")

    def __neg__(self: "Element") -> None:
        raise BMXSyntaxError(f"Cannot ' - ' an Element at {self!r}")

    def __add__(self: "Element", other: Any) -> "Fragment":
        return Fragment(self, other)

    def __radd__(self: "Element", other: Any) -> "Fragment":
        return Fragment(other, self)

    def __sub__(self: "Element", other: "Tag") -> "Fragment":
        if not isinstance(other, Tag):
            raise BMXSyntaxError(
                f"Cannot 'subtract' {other!r} of type {type(other)!r}. "
                "Only Tags can be 'subtracted'"
            )
        return Fragment(self, -other)

    def __repr__(self: "Element") -> str:
        attrs_repr = repr(self.attributes) if self.attributes else ""
        contents_repr = repr(self.contents) if self.contents else ""
        return "".join(
            (
                "<Element:",
                self.name,
                "|",
                hex(id(self)),
                " ",
                attrs_repr,
                contents_repr,
                ">",
            )
        )

    def __str__(self: "Element") -> str:
        if self.attributes:
            attributes: List[str] = []
            for key, value in self.attributes.items():
                if str(key).endswith("_"):  # ie. for_, id_, class_
                    key = key[:-1]
                if value is True:
                    attributes.extend(" " + key)
                    continue
                elif value is False:
                    continue
                elif isinstance(value, list):
                    value = " ".join(value)

                attributes.extend(" " + str(key) + '="' + str(value) + '"')
        else:
            attributes = []

        begin = ("<", self.name, *attributes, ">")
        end = ("</", self.name, ">")

        return "".join((*begin, *map(str, self.contents), *end))


class Fragment(Sequence):
    def __init__(self: "Fragment", *args: Any) -> None:
        self._contents = args
        # self.tagstack = [self]

    # def __iter__(self):
    # Not sure this is correct
    #    return iter((i for c in self.tagstack for i in c.contents))

    def __len__(self: "Fragment") -> int:
        return len(self._contents)

    def __getitem__(self: "Fragment", index: Union[int, slice]) -> Any:
        if isinstance(index, int):
            return self._contents[index]
        elif isinstance(index, slice):
            return Fragment(*self._contents[index])
        else:
            raise ValueError(
                f"Cannot get item with index {index!r}. Index must be int or slice"
            )

    @singledispatchmethod
    def __add__(self: "Fragment", other: Any) -> "Fragment":
        return Fragment(*self._contents, str(other))

    @__add__.register(Tag)
    def _add_Tag(self: "Fragment", other: Tag) -> "Fragment":
        new_tag = other.create_start_tag()
        return Fragment(*self._contents, new_tag)

    @__add__.register(StartTag)
    def _add_StartTag(self: "Fragment", other: StartTag) -> "Fragment":
        return Fragment(*self._contents, other)

    @__add__.register(EndTag)
    def _add_EndTag(self: "Fragment", other: EndTag) -> "Fragment":
        # TODO: check for start tag in reversed(self._contents)
        for idx, item in enumerate(reversed(self._contents)):
            if isinstance(item, StartTag):
                if item.name == other.name:
                    new_element = item.render(
                        *self._contents[len(self._contents) - idx :], **item.attributes
                    )
                    return Fragment(
                        *self._contents[: len(self._contents) - idx - 1], new_element
                    )
                else:
                    raise BMXSyntaxError(
                        f"Tag mismatch. Appending {other!r} but found {item!r}."
                    )
        else:
            return Fragment(*self._contents, other)

    @__add__.register(SelfClosingTag)
    def _add_SelfClosingTag(self: "Fragment", other: SelfClosingTag) -> "Fragment":
        return Fragment(*self._contents, other)

    @__add__.register(str)
    def _add_str(self: "Fragment", other: str) -> "Fragment":
        # We use markupsafe to escape all strings to make them safe
        return Fragment(*self._contents, escape(other))

    @__add__.register(Element)
    def _add_Element(self: "Fragment", other: Element) -> "Fragment":
        return Fragment(*self._contents, other)

    @__add__.register(Iterable)
    def _add_Iterable(self: "Fragment", other: Iterable) -> "Fragment":
        for item in other:
            self = self + item
        return self

    @singledispatchmethod
    def __sub__(self: "Fragment", other: Any) -> "Fragment":
        raise BMXSyntaxError(
            f"Cannot 'subtract' {other!r} of type {type(other)!r}. Only Tags can be 'subtracted'"
        )

    @__sub__.register(Tag)
    def _sub_Tag(self: "Fragment", other: Tag) -> "Fragment":
        # check for matching start tag in reversed(self._contents)
        for idx, item in enumerate(reversed(self._contents)):
            if isinstance(item, StartTag):
                if item.name == other.name:
                    new_element = item.render(
                        *self._contents[len(self._contents) - idx :], **item.attributes
                    )
                    return Fragment(
                        *self._contents[: len(self._contents) - idx - 1], new_element
                    )
                else:
                    raise BMXSyntaxError(
                        f"Tag mismatch. Appending {other!r} but found {item!r}."
                    )
        else:
            return Fragment(*self._contents, -other)

    def __radd__(self: "Fragment", other: Any) -> "Fragment":
        return Fragment(other) + self._contents

    @recursive_repr(fillvalue="self")
    def __repr__(self: "Fragment") -> str:
        self_repr = "".join(("<Fragment|", hex(id(self)), " "))
        return "".join(
            (
                self_repr,
                "contents=",
                repr(self._contents),
                # " ",
                # "tagstack=",
                # repr(self.tagstack),
                ">",
            )
        )

    def __str__(self: "Fragment") -> str:
        result = []
        for item in self._contents:
            result.append(str(item))
            # result.extend([str(i) for i in item.contents if hasattr(i, "contents")])
        return "".join(result)


class DOCTYPE(Enum):
    """Enumeration for easy access to Document Type Declarations

    See: https://www.w3.org/QA/2002/04/valid-dtd-list.html for the source of these.
    Only html and xhtml doctypes are included for now. If you need more, open a PR!"""

    html = "<!DOCTYPE html>"
    html4_strict = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
       "http://www.w3.org/TR/html4/strict.dtd">"""
    html4_transitional = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
       "http://www.w3.org/TR/html4/loose.dtd">"""
    html4_frameset = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
       "http://www.w3.org/TR/html4/frameset.dtd">"""
    xhtml1_strict = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">"""
    xhtml1_transitional = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
    xhtml1_frameset = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">"""
    xhtml11_dtd = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
       "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">"""
    xhtml_basic11 = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN"
        "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">"""

    def __str__(self: "DOCTYPE") -> str:
        return self.value


class Namespace:
    """Create tags as object attributes.

    Suitable for Web Components or ad-hoc XML markup"""

    def __init__(self: "Namespace", prefix: str = None, translate: bool = True) -> None:
        self.prefix = prefix
        self.translate = translate

    def __getattr__(self: "Namespace", attr: str) -> Tag:
        if attr.endswith("_"):
            attr = attr[:-1]  # remove trailing '_' for python keyword clashes
        if self.translate:
            attr = attr.replace("_", "-")
        if self.prefix is not None:
            name = self.prefix + attr
        else:
            name = attr
        return Tag(name)
