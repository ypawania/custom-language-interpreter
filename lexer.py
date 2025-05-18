class Token:
    def __init__(self, type, lexeme, line):
        self.type = type
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, line={self.line})"


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

start = 0
current = 0
line = 1


def is_letter(c):
    return c.isalpha() or c == "_"


def scan(source: str) -> list:
    tokens = []

    while current < len(source):
        start = current
        token = scan_token(source)
        if token is not None:
            tokens.append(token)

    tokens.append(Token("EOF", "", line))
    return tokens


def scan_token(source):
    global current, line

    c = source[current]
    current += 1  # advance by default unless we read more characters later

    if c == "(":
        return Token("LPAREN", c, line)
    elif c == ")":
        return Token("RPAREN", c, line)
    elif c == "{":
        return Token("LBRACE", c, line)
    elif c == "}":
        return Token("RBRACE", c, line)
    elif c == ";":
        return Token("SEMICOLON", c, line)
    elif c == "+":
        return Token("PLUS", c, line)
    elif c == "-":
        return Token("MINUS", c, line)
    elif c == "*":
        return Token("STAR", c, line)
    elif c == "/":
        return Token("SLASH", c, line)
    elif c == "%":
        return Token("MODULO", c, line)
    elif c == "<":
        return Token("LESS", c, line)
    elif c == "=":
        if current < len(source) and source[current] == "=":
            current += 1
            return Token("EQUAL_EQUAL", "==", line)
        return Token("EQUAL", "=", line)

    elif c == '"':
        value = ""
        while source[current] != '"':
            value += source[current]
            current += 1
        current += 1  # skip the closing quote
        return Token("STRING", value, line)

    elif c == "\n":
        line += 1
        return None

    elif c.isdigit():
        value = c
        while current < len(source) and source[current].isdigit():
            value += source[current]
            current += 1
        return Token("NUMBER", value, line)

    elif is_letter(c):
        value = c
        while current < len(source) and is_letter(source[current]):
            value += source[current]
            current += 1
        if value in custom_keywords:
            return Token(custom_keywords[value].upper(), value, line)  # e.g., "IF"
        return Token("IDENTIFIER", value, line)

    elif c in [" ", "\r", "\t"]:
        return None  # skip whitespace
