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

tokens = lexer.scan(source_code)  # From your lexer
# print(tokens)
parser = parser.Parser(tokens)  # From your parser
ast = parser.parse()  # Returns a list of statements
print(ast)  # Just to see if parsing succeeds
