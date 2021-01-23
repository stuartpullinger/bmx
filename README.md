# BMX - Basic Markup eXpressions

A DSL for representing HTML/XML in Python using an expression-like syntax. Why? You get to use the Python syntax you already know.

## Example
<table>
<tr>
<td> Taking the example from the Jinja2 website: </td> <td> This can be represented in BMX like this: </td>
</tr>
<tr>

<td>

```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
  <title>My Webpage</title>
</head>
<body>
  <ul id="navigation">
  {% for item in navigation %}
    <li>
      <a href="{{ item.href }}">{{ item.caption }}</a>
    </li>
  {% endfor %}
  </ul>

  <h1>My Webpage</h1>
  {{ a_variable }}

  {# a comment #}
</body>
</html>
```

</td>

<td>

 ```Python
mydoc = (
  DOCTYPE.html
  +html(lang='en') 
    +head
      +title +"My Webpage" -title
    -head
    +body
      +ul('#navigation') +(
        +li
          +a(href=item.href) +item.caption -a
        -li
        for item in navigation)
      -ul

      +h1 +"My Webpage" -h1
      +a_variable

      # a comment
    -body
  -html)
```

</td>
</tr>
</table>

**Note:** Just as with ordinary Python expressions, multi-line BMX expressions must be surrounded by parentheses. 

## Installation and Dependencies
`bmx` is tested on CPython versions 3.6-3.9. It has 2 dependencies: singledispatchmethod (backported from 3.8) and MarkupSafe - to escape html in strings.
```Shell
pip install bmx
```

## How does it work?
We define a `Tag` class which overrides the unary +/- and binary +/- operators to model the opening and closing tags of HTML. We provide a `__call__` method to model HTML attributes as keyword arguments and a `__getattr__` method to provide a shorthand for HTML classes (see below). A `Tag` is instantiated for every HTML tag and is available with a `from bmx.htmltags import html, head, body, span`.

## Usage
An example using Flask (available in the top-level source directory):
```Python
# flask_greeter.py
from bmx.htmltags import (
    html, 
    head, 
    title,
    body,
    p
)
from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def greeter(name: str):
    return str(
        # fmt: off
        +html
          +head
            +title +"Flask Greeter" -title
          -head
          +body
            +p +f"Hello {name}" -p
          -body
        -html
        # fmt: on
    )
```

Install Flask then  run it as:
```Shell
FLASK_APP=flask_greeter.py flask run
```

Go to `https://127.0.0.1:5000/<your_name>` in your browser (eg. `https://127.0.0.1:5000/Stuart`) and you will see the message.

## Table of Conversions

|Type   |HTML       |BMX |Comment/Mnemonic|
|-------|-----------|----|----------------|
|Opening tag | `<div>` | `+div` |*Mnemonic: Adding content*|
|Closing tag | `</div>` | `-div` |*Mnemonic: opposite of adding content*  |
|Self-closing tag | `<input/>` | `+input` | Self-closing tag are pre-defined |
|Attributes | `<input type="text">` | `+input_(type_="text")` | *Mnemonic: attributes are keyword arguments.* **Note**: Append an underscore to avoid conflicts with Python keywords |
|Attributes: shorthand for `id` and `class`| `<div id="userinput" class="credentials" >` | `+div('#userinput.credentials')` | *#id* *.classname* |
|Attributes: shorthand for `class`| `<div class="col-sm-8 col-md-7 py-4">` | `+div .col_sm_8 .col_md_7 .py_4` | *.classname* Underscores are transposed to dashes |
|Composing tags and content| `<h1>The Title</h1>`| `+h1 +"The Title" -h1` | *Mnemonic: think string concatenation ie. "Hello " + "World!"*|

### MarkupSafe
`bmx` uses MarkupSafe to escape HTML from strings. If you are sure that you don't want to escape the HTML in a string, you can wrap it in a Markup object and the string will be included as-is.

## Autoformatters

### Black
To use the Black uncompromising autoformatter, surround your BMX markup with `#fmt: off` and `#fmt: on` comments like this:
```Python
result = (
    # fmt: off
    +html
        +body
            +h1 +"My Page" -h1
        -body
    -html
    # fmt: on
)
```

### Autopep8
To use autopep8, you can use the `#fmt: off` and `#fmt: on` comments as above or turn off 2 fixes:
* E225 - Fix missing whitespace around operator.
* E131 - Fix hanging indent for unaligned continuation line.

whereever you put your autopep8 [configuration](https://github.com/hhatto/autopep8#configuration)
```INI
ignore = E225,E131
```

## Changelog
### 0.0.2
- default to using MarkupSafe for strings
- include DOCTYPE in htmltags module
- README improvements/fixes

### 0.0.1
- Initial release
