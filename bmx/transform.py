import sys

from libcst import CSTTransformer, parse_module
from libcst._nodes.base import CSTNode
from libcst._nodes.expression import Arg, Call, DictElement, Dict, List, Element, Name, SimpleString
from libcst._parser.conversions.bmx import BmxFragment, BmxSelfClosing, BmxOpenClose
from libcst.codemod.visitors import AddImportsVisitor
from .htmltags import html5tags
from libcst.metadata.wrapper import MetadataWrapper

# target_filename = sys.argv[1]

class BmxTransformer(CSTTransformer):
    def leave_BmxSelfClosing(self, original_node: BmxSelfClosing, updated_node: BmxSelfClosing) -> Call:
        ref = original_node.ref
        # Special-case html tags eg. h1
        if isinstance(ref, Name) and ref.value in html5tags:
            ref = SimpleString(value=repr(ref.value))

        attribute_elements = [DictElement(attr.key, attr.value or Name('None')) for attr in updated_node.attributes]
        attributes = Dict(attribute_elements)

        element = Call(func=Name('BmxElement'), args=[Arg(value=ref), Arg(value=attributes, star='**')])

        return element

    def leave_BmxOpenClose(self, original_node: BmxOpenClose, updated_node: BmxOpenClose) -> Call:
        ref = original_node.ref
        # Special-case html tags eg. h1
        if isinstance(ref, Name) and ref.value in html5tags:
            ref = SimpleString(value=repr(ref.value))

        attribute_elements = [DictElement(attr.key, attr.value or Name('None')) for attr in updated_node.attributes]
        attributes = Dict(attribute_elements)

        content_elements = [Element(i) for i in updated_node.contents]
        contents = List(content_elements)

        element = Call(func=Name('BmxElement'), args=[Arg(value=ref), Arg(value=contents, star='*'), Arg(value=attributes, star='**')])

        return element

# transformer = BmxTransformer()
# with open(target_filename) as f:
#     original_tree = parse_module(f.read())
#     print(original_tree)
#     print()
#     modified_tree = original_tree.visit(transformer)
#     import_visitor = AddImportsVisitor( )
#     print(modified_tree)
#     print()
#     print(modified_tree.code)
