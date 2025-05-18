import parser
import lexer


source_code = """
if (x == 1 or y == 2 and z == 3) {
    print("in if branch");
    x = x + 1;
} else {
    while (x == 2) {
        print("in while loop");
    }
}
"""


def pretty_print(node, indent=0):
    prefix = "  " * indent  # Indentation string

    if node is None:
        print(prefix + "None")
        return

    node_type = type(node).__name__

    if node_type == "If":
        print(prefix + "If:")
        print(prefix + "  Condition:")
        pretty_print(node.condition, indent + 2)
        print(prefix + "  Then:")
        pretty_print(node.then_branch, indent + 2)
        print(prefix + "  Else:")
        pretty_print(node.else_branch, indent + 2)

    elif node_type == "While":
        print(prefix + "While:")
        print(prefix + "  Condition:")
        pretty_print(node.condition, indent + 2)
        print(prefix + "  Body:")
        pretty_print(node.body, indent + 2)

    elif node_type == "Block":
        print(prefix + "Block:")
        for stmt in node.statements:
            pretty_print(stmt, indent + 1)

    elif node_type == "Binary":
        print(prefix + f"Binary({node.operator}):")
        print(prefix + "  Left:")
        pretty_print(node.left, indent + 2)
        print(prefix + "  Right:")
        pretty_print(node.right, indent + 2)

    elif node_type == "Unary":
        print(prefix + f"Unary({node.operator}):")
        pretty_print(node.right, indent + 1)

    elif node_type == "Literal":
        print(prefix + f"Literal({node.value})")

    elif node_type == "Variable":
        print(prefix + f"Variable({node.name})")

    elif node_type == "Assign":
        print(prefix + f"Assign({node.name} = )")
        pretty_print(node.value, indent + 1)

    elif node_type == "ExpressionStatement":
        print(prefix + "ExpressionStatement:")
        pretty_print(node.expression, indent + 1)

    else:
        # Fallback: just print the object type and fields if any
        print(
            prefix + f"{node_type}: {vars(node) if hasattr(node, '__dict__') else node}"
        )


tokens = lexer.scan(source_code)  # From your lexer
parser = parser.Parser(tokens)  # From your parser
ast = parser.parse()  # Returns a list of statements


for statement in ast:
    pretty_print(statement)
