# BMX - Basic Markup eXpressions

A DSL for representing HTML/XML in Python using an expression-like syntax.

## Example
Taking the example from the Jinja2 website:
```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>

    <h1>My Webpage</h1>
    {{ a_variable }}

    {# a comment #}
</body>
</html>
```

This can be represented in BMX like this:
```Python
mydoc = (doc('html')
        +html(lang='en')
          +head
            +title +"My Webpage" -title
          -head
          +body
            +ul('#navigation')
              +(+li
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
**Note:** Just as with ordinary Python expressions, multi-line BMX expressions must be surrounded by parentheses. 

## Table of Conversions

|Type   |HTML       |BMX |Comment/Mnemonic|
|-------|-----------|----|----------------|
|Opening tag | `<div>` | `+div` |*Mnemonic: Adding content*|
|Closing tag | `</div>` | `-div` |*Mnemonic: opposite of adding content*  |
|Self-closing tag | `<input/>` | `+input` | Self-closing tag are pre-defined |
|Attributes | `<input type="text">` | `input_(type_="text")` | *Mnemonic: attributes are keyword arguments.* **Note**: Append an underscore to avoid conflicts with Python keywords |
|Attributes: shorthand for `id` and `class`| `<div id="userinput" class="credentials" >` | `div('#userinput.credentials')` | *#id* *.classname* |
|Attributes: shorthand for `class`| `<div class="col-sm-8 col-md-7 py-4">` | `+div .col_sm_8 .col_md_7 .py_4` | *.classname* Underscores are transposed to dashes |
|Composing tags and content| `<h1>The Title</h1>`| `+h1 +"The Title" -h1` | *Mnemonic: think string concatenation ie. "Hello " + "World!"*|

## Autoformatters

### Black
To use the Black uncompromising autoformatter, surround your BMX markup with `#fmt: off` and `#fmt: on` comments like this:
```Python
result = (
    # fmt: off
    +html
        +body
            +title +"My Page" -title
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
