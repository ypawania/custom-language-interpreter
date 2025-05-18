from flask import Flask, request, jsonify, render_template
import lexer
import parser
from interpreter import Interpreter
import io
import sys

app = Flask(__name__)

# Define standard keywords
standard_keywords = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "and": "AND",
    "or": "OR",
    "print": "PRINT",
    "true": "TRUE",
    "false": "FALSE",
}


def merge_keywords(custom_keywords):
    merged = standard_keywords.copy()
    for k, v in custom_keywords.items():
        if k not in merged:
            merged[k] = v
    return merged


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    source_code = data.get("source_code", "")
    custom_keywords = data.get("custom_keywords", {})

    keywords = merge_keywords(custom_keywords)

    try:
        tokens = lexer.scan(source_code, keywords)
        p = parser.Parser(tokens)
        ast = p.parse()

        # Capture print output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        interpreter = Interpreter()
        interpreter.interpret(ast)

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return jsonify({"output": output.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
