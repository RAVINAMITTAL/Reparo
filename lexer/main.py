# =============================================================================
# main.py — Entry point for running the Reparo lexer on a .rpl source file
# =============================================================================

import os
import sys

# Allow running directly from the lexer/ directory
sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer, LexerError


def run(file_path: str = "tests/test1.rpl"):
    """Lex a Replon source file and print the resulting token stream."""

    if not os.path.exists(file_path):
        print(f"[Error] File not found: '{file_path}'")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    print(f"--- Lexing: {file_path} ---\n")

    try:
        lexer  = Lexer(source_code)
        tokens = lexer.tokenize()
    except LexerError as e:
        print(e)
        return

    print("--- Token Stream ---")
    for tok in tokens:
        print(tok)


if __name__ == "__main__":
    # Optionally accept a file path as a command-line argument.
    path = sys.argv[1] if len(sys.argv) > 1 else "tests/test1.rpl"
    run(path)
