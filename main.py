import lexer
import parser
from interpreter import Interpreter

source_code = """
x = 1;
if (x == 1 or false) {
    print("x is 1");
} else {
    print("x is not 1");
}
"""

tokens = lexer.scan(source_code)
p = parser.Parser(tokens)
ast = p.parse()

interpreter = Interpreter()
interpreter.interpret(ast)
