from typing import Any, Callable, NamedTuple, ParamSpec, TypeVar
from markupsafe import escape

P = ParamSpec('P')
R = TypeVar('R')


class BmxElement:
    def __init__(self, ref: Callable[P, R] | str | None, *contents: P.args, **attributes: P.kwargs):
        self.ref = ref
        self.contents = contents
        self.attributes = attributes

    def __str__(self) -> str:
        if isinstance(self.ref, Callable):
            return str(self.ref(*(self.contents or []), **(self.attributes or {})))
        else:
            seq = ['<']
            seq.append(escape(self.ref))
            if self.attributes:
                seq.append(' ')
                for key, value in self.attributes.items():
                    if value is True:
                        seq.append(escape(str(key)))
                        continue
                    elif value is False:
                        continue
                    else:
                        seq.extend((escape(str(key)), '=', '"', escape(str(value)), '"', ' '))

            if self.contents is not None:
                seq.append('>')

                seq.extend((escape(str(c)) if not isinstance(c, BmxElement) else str(c) for c in self.contents))

                seq.extend(('</', str(self.ref), '>'))
            else:
                seq.append('/>')

            return ''.join(seq)

    def render(self) -> R | str | tuple[object, ...]:
        if self.ref is None:
            return self.contents
        elif isinstance(self.ref, str):
            return str(self)
        elif isinstance(self.ref, Callable):
            return self.ref(*self.contents if self.contents else (), **self.attributes)
        else:
            raise ValueError(f'ref has the wrong type: {type(self.ref)}')
