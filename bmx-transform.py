import sys

from libcst_bmx.libcst import CSTTransformer, parse_module
from libcst_bmx.libcst._nodes.base import CSTNode
from libcst_bmx.libcst._nodes.expression import Arg, Call, DictElement, Dict, Name, SimpleString
from libcst_bmx.libcst._parser.conversions.bmx import BmxSelfClosing
from libcst_bmx.libcst.codemod.visitors import AddImportsVisitor
from bmx.htmltags import html5tags
from libcst_bmx.libcst.metadata.wrapper import MetadataWrapper

target_filename = sys.argv[1]

class BmxTransformer(CSTTransformer):
    def leave_BmxSelfClosing(self, original_node: BmxSelfClosing, updated_node: CSTNode) -> Call:
        ref = original_node.ref
        # Special-case html tags eg. h1
        if isinstance(ref, Name) and ref.value in dir(html5tags):
            ref = SimpleString(ref.value)

        attribute_elements = [DictElement(attr.key, attr.value or Name('None')) for attr in original_node.attributes]
        attributes = Dict(attribute_elements)

        element = Call(func=SimpleString('BmxElement'), args=[Arg(value=ref), Arg(value=attributes, star='**')])

        return element

transformer = BmxTransformer()
with open(target_filename) as f:
    original_tree = parse_module(f.read())
    print(original_tree)
    print()
    modified_tree = original_tree.visit(transformer)
    import_visitor = AddImportsVisitor( )
    print(modified_tree)
    print()
    print(modified_tree.code)
