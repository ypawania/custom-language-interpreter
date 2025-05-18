import lexer


# AST Node Definitions
class Expr:
    pass


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Variable(Expr):
    def __init__(self, name):
        self.name = name


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression


class Assignment(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value


# Statements
class Stmt:
    pass


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression


class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


# Parser implementation
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    # Top-level statement parsing
    def statement(self):
        if self.match("PRINT"):
            return self.print_statement()
        if self.match("IF"):
            return self.if_statement()
        if self.match("WHILE"):
            return self.while_statement()
        if self.match("LBRACE"):
            return Block(self.block())
        return self.expression_statement()

    def print_statement(self):
        self.consume("LPAREN")
        value = self.expression()
        self.consume("RPAREN")
        self.consume("SEMICOLON")
        return Print(value)

    def if_statement(self):
        self.consume("LPAREN")
        condition = self.expression()
        self.consume("RPAREN")
        then_branch = self.statement()
        else_branch = None
        if self.match("ELSE"):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume("LPAREN")
        condition = self.expression()
        self.consume("RPAREN")
        body = self.statement()
        return While(condition, body)

    def block(self):
        statements = []
        while not self.check("RBRACE") and not self.is_at_end():
            statements.append(self.statement())
        self.consume("RBRACE")
        return statements

    def expression_statement(self):
        expr = self.expression()
        self.consume("SEMICOLON")
        return ExpressionStmt(expr)

    # Expression parsing
    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.logic_or()
        if self.match("EQUAL"):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assignment(expr.name, value)
        return expr

    def logic_or(self):
        expr = self.logic_and()
        while self.match("OR"):
            operator = self.previous()
            right = self.logic_and()
            expr = Logical(expr, operator, right)
        return expr

    def logic_and(self):
        expr = self.equality()
        while self.match("AND"):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match("EQUAL_EQUAL"):
            operator = self.previous()
            right = self.primary()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match("LESS"):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)
        return expr

    def multiplication(self):
        expr = self.unary()
        print("debugging message")
        while self.match("STAR", "SLASH", "MODULO"):
            print("inside of parser multiple while reached")
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        return self.primary()

    def primary(self):
        if self.match("NUMBER"):
            return Literal(int(self.previous().lexeme))
        if self.match("STRING"):
            return Literal(self.previous().lexeme)
        if self.match("IDENTIFIER"):
            return Variable(self.previous().lexeme)
        if self.match("LPAREN"):
            expr = self.expression()
            self.consume("RPAREN")
            return Grouping(expr)

    # Helpers
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type):
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"Expected {type} but got {self.peek().type}")

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
