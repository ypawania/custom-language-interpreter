# interpreter.py
import lexer
import parser


class Environment:
    def __init__(self):
        self.values = {}

    def get(self, name):
        if name in self.values:
            return self.values[name]
        raise NameError(f"Undefined variable '{name}'")

    def assign(self, name, value):
        self.values[name] = value


class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, stmt):
        method_name = f"execute_{type(stmt).__name__}"
        method = getattr(self, method_name)
        return method(stmt)

    def evaluate(self, expr):
        method_name = f"evaluate_{type(expr).__name__}"
        method = getattr(self, method_name)
        return method(expr)

    def execute_ExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)

    def execute_Print(self, stmt):
        value = self.evaluate(stmt.expression)

        print(value)

    def execute_Assign(self, stmt):
        value = self.evaluate(stmt.value)
        self.env.assign(stmt.name, value)

    def execute_Block(self, stmt):
        for statement in stmt.statements:
            self.execute(statement)

    def execute_If(self, stmt):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def execute_While(self, stmt):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)

    def evaluate_Literal(self, expr):
        return expr.value

    def evaluate_Variable(self, expr):
        return self.env.get(expr.name)

    def evaluate_Assignment(self, expr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def evaluate_Unary(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator == "-":
            return -right
        elif expr.operator == "!":
            return not self.is_truthy(right)

    def evaluate_Binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op = expr.operator.lexeme

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "%":
            return left % right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return left < right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == ">=":
            return left >= right
        else:
            print("no matches")

    def evaluate_Logical(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == "OR":
            if self.is_truthy(left):
                return True
            return self.evaluate(expr.right)
        elif expr.operator.type == "AND":
            if not self.is_truthy(left):
                return False
            return self.evaluate(expr.right)

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return bool(value)


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


tokens = lexer.scan(source_code)
print(tokens)
p = parser.Parser(tokens)
ast = p.parse()

interpreter = Interpreter()
interpreter.interpret(ast)
