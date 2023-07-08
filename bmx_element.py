from typing import Any, Callable, NamedTuple, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')


class BmxElement:
    def __init__(self, ref: Callable[P, R] | str | None, *contents: P.args, **attributes: P.kwargs):
        self.ref = ref
        self.contents = contents
        self.attributes = attributes

    def __str__(self):
        ...

    def render(self) -> R | str | tuple[object, ...]:
        if self.ref is None:
            return self.contents
        elif isinstance(self.ref, str):
            return str(self)
        elif isinstance(self.ref, Callable):
            return self.ref(*self.contents if self.contents else (), **self.attributes)
        else:
            raise ValueError(f'ref has the wrong type: {type(self.ref)}')
