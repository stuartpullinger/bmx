# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .core import SelfClosingTag, SelfClosingTagStyle, Tag, DOCTYPE

# <!--...-->
pass
# <!DOCTYPE>
pass
# <a>
a = Tag("a")
# <abbr>
abbr = Tag("abbr")
# <acronym>
acronym = Tag("acronym")
# <address>
address = Tag("address")
# <applet>
applet = Tag("applet")
# <area>
area = SelfClosingTag("area", SelfClosingTagStyle.HTML)
# <article>
article = Tag("article")
# <aside>
aside = Tag("aside")
# <audio>
audio = Tag("audio")
# <b>
b = Tag("b")
# <base>
base = SelfClosingTag("base", SelfClosingTagStyle.HTML)
# <basefont>
basefont = Tag("basefont")
# <bdi>
bdi = Tag("bdi")
# <bdo>
bdo = Tag("bdo")
# <big>
big = Tag("big")
# <blockquote>
blockquote = Tag("blockquote")
# <body>
body = Tag("body")
# <br>
br = SelfClosingTag("br", SelfClosingTagStyle.HTML)
# <button>
button = Tag("button")
# <canvas>
canvas = Tag("canvas")
# <caption>
caption = Tag("caption")
# <center>
center = Tag("center")
# <cite>
cite = Tag("cite")
# <code>
code = Tag("code")
# <col>
col = SelfClosingTag("col", SelfClosingTagStyle.HTML)
# <colgroup>
colgroup = Tag("colgroup")
# <data>
data = Tag("data")
# <datalist>
datalist = Tag("datalist")
# <dd>
dd = Tag("dd")
# <del>
del_ = Tag("del")
# <details>
details = Tag("details")
# <dfn>
dfn = Tag("dfn")
# <dialog>
dialog = Tag("dialog")
# <dir>
dir_ = Tag("dir")
# <div>
div = Tag("div")
# <dl>
dl = Tag("dl")
# <dt>
dt = Tag("dt")
# <em>
em = Tag("em")
# <embed>
embed = SelfClosingTag("embed", SelfClosingTagStyle.HTML)
# <fieldset>
fieldset = Tag("fieldset")
# <figcaption>
figcaption = Tag("figcaption")
# <figure>
figure = Tag("figure")
# <font>
font = Tag("font")
# <footer>
footer = Tag("footer")
# <form>
form = Tag("form")
# <frame>
frame = Tag("frame")
# <frameset>
frameset = Tag("frameset")
# <h1> to <h6>
h1 = Tag("h1")
h2 = Tag("h2")
h3 = Tag("h3")
h4 = Tag("h4")
h5 = Tag("h5")
h6 = Tag("h6")
# <head>
head = Tag("head")
# <header>
header = Tag("header")
# <hr>
hr = SelfClosingTag("hr", SelfClosingTagStyle.HTML)
# <html>
html = Tag("html")
# <i>
i = Tag("i")
# <iframe>
iframe = Tag("iframe")
# <img>
img = SelfClosingTag("img", SelfClosingTagStyle.HTML)
# <input>
input_ = SelfClosingTag("input", SelfClosingTagStyle.HTML)
# <ins>
ins = Tag("ins")
# <kbd>
kbd = Tag("kbd")
# <label>
label = Tag("label")
# <legend>
legend = Tag("legend")
# <li>
li = Tag("li")
# <link>
link = SelfClosingTag("link", SelfClosingTagStyle.HTML)
# <main>
main = Tag("main")
# <map>
map_ = Tag("map")
# <mark>
mark = Tag("mark")
# <meta>
meta = SelfClosingTag("meta", SelfClosingTagStyle.HTML)
# <meter>
meter = Tag("meter")
# <nav>
nav = Tag("nav")
# <noframes>
noframes = Tag("noframes")
# <noscript>
noscript = Tag("noscript")
# <object>
object_ = Tag("object")
# <ol>
ol = Tag("ol")
# <optgroup>
optgroup = Tag("optgroup")
# <option>
option = Tag("option")
# <output>
output = Tag("output")
# <p>
p = Tag("p")
# <param>
param = SelfClosingTag("param", SelfClosingTagStyle.HTML)
# <picture>
picture = Tag("picture")
# <pre>
pre = Tag("pre")
# <progress>
progress = Tag("progress")
# <q>
q = Tag("q")
# <rp>
rp = Tag("rp")
# <rt>
rt = Tag("rt")
# <ruby>
ruby = Tag("ruby")
# <s>
s = Tag("s")
# <samp>
samp = Tag("samp")
# <script>
script = Tag("script")
# <section>
section = Tag("section")
# <select>
select = Tag("select")
# <small>
small = Tag("small")
# <source>
source = SelfClosingTag("source", SelfClosingTagStyle.HTML)
# <span>
span = Tag("span")
# <strike>
strike = Tag("strike")
# <strong>
strong = Tag("strong")
# <style>
style = Tag("style")
# <sub>
sub = Tag("sub")
# <summary>
summary = Tag("summary")
# <sup>
sup = Tag("sup")
# <svg>
svg = Tag("svg")
# <table>
table = Tag("table")
# <tbody>
tbody = Tag("tbody")
# <td>
td = Tag("td")
# <template>
template = Tag("template")
# <textarea>
textarea = Tag("textarea")
# <tfoot>
tfoot = Tag("tfoot")
# <th>
th = Tag("th")
# <thead>
thead = Tag("thead")
# <time>
time = Tag("time")
# <title>
title = Tag("title")
# <tr>
tr = Tag("tr")
# <track>
track = SelfClosingTag("track", SelfClosingTagStyle.HTML)
# <tt>
tt = Tag("tt")
# <u>
u = Tag("u")
# <ul>
ul = Tag("ul")
# <var>
var = Tag("var")
# <video>
video = Tag("video")
# <wbr>
wbr = SelfClosingTag("wbr", SelfClosingTagStyle.HTML)


# result = +body +h1 +"The Title" -body
