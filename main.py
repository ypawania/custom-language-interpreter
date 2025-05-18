import interpreter
import parser
import lexer

source_code = """

i = 0;
while (i < 30) {
    if (i % 15 == 0) { print("FizzBuzz"); }
    else { 
        if (i % 3 == 0) { print("Fizz"); }
        else { 
            if (i % 5 == 0) { print("Buzz"); }
                else { print(i); }
        }
    }
  i = i + 1;
}
"""
custom_keywords = {
    "chat": "if",
    "if": "if",
    "else": "else",
    "while": "while",
    "and": "and",
    "or": "or",
    "say": "print",
    "print": "print",
}


tokens = lexer.scan(source_code, custom_keywords)
print(tokens)
p = parser.Parser(tokens)
ast = p.parse()

interpreter = interpreter.Interpreter()
interpreter.interpret(ast)
