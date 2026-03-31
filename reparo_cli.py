# =============================================================================
# reparo_cli.py — Command-line interface for the Reparo compiler
#
# After installing with `pip install -e .`, this becomes the `reparo` command.
#
# Usage:
#   reparo run <file.rpl>        — full pipeline (lex → parse → ...)
#   reparo lex <file.rpl>        — show only the token stream (debug)
#   reparo parse <file.rpl>      — show only the AST (debug)
# =============================================================================

import sys
import os


def _print_section(title: str):
    bar = "─" * 60
    print(f"\n{bar}\n  {title}\n{bar}")


def _read_source(file_path: str) -> str:
    """Read a .rpl source file, with helpful error messages."""
    if not file_path.endswith('.rpl'):
        print(f"[Reparo] Warning: '{file_path}' does not have a .rpl extension.")
    if not os.path.exists(file_path):
        print(f"[Reparo] Error: file not found — '{file_path}'")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------
# Sub-commands
# ---------------------------------------------------------------------------

def cmd_lex(file_path: str):
    """Lex a .rpl file and print the token stream."""
    from lexer.lexer import Lexer, LexerError

    source = _read_source(file_path)
    print(f"[Reparo] Lexing: {file_path}")

    try:
        tokens = Lexer(source).tokenize()
    except LexerError as e:
        print(f"\n[Reparo] Lexer error:\n  {e}")
        sys.exit(1)

    _print_section("Token Stream")
    for tok in tokens:
        print(f"  {tok}")


def cmd_parse(file_path: str):
    """Lex + parse a .rpl file and print the AST."""
    from lexer.lexer import Lexer, LexerError
    from parser.parser import Parser, ParseError

    source = _read_source(file_path)
    print(f"[Reparo] Parsing: {file_path}")

    try:
        tokens = Lexer(source).tokenize()
    except LexerError as e:
        print(f"\n[Reparo] Lexer error:\n  {e}")
        sys.exit(1)

    try:
        ast = Parser(tokens).parse()
    except ParseError as e:
        print(f"\n[Reparo] Parse error:\n  {e}")
        sys.exit(1)

    _print_section("Abstract Syntax Tree")
    for node in ast:
        print(f"  {node!r}")


def cmd_run(file_path: str):
    """Full pipeline: lex → parse → semantic → interpret."""
    from lexer.lexer import Lexer, LexerError
    from parser.parser import Parser, ParseError
    from semantic.analyzer import SemanticAnalyzer, SemanticError
    from executor.interpreter import Interpreter

    source = _read_source(file_path)
    print(f"[Reparo] Running: {file_path}")

    # Stage 1 — Lexer
    try:
        tokens = Lexer(source).tokenize()
    except LexerError as e:
        print(f"\n[Reparo] Lexer error:\n  {e}")
        sys.exit(1)

    _print_section("Token Stream")
    for tok in tokens:
        print(f"  {tok}")

    # Stage 2 — Parser
    try:
        ast = Parser(tokens).parse()
    except ParseError as e:
        print(f"\n[Reparo] Parse error:\n  {e}")
        sys.exit(1)

    _print_section("Abstract Syntax Tree")
    for node in ast:
        print(f"  {node!r}")

    # Stage 3 — Semantic analyser (stub)
    try:
        SemanticAnalyzer().analyze(ast)
    except SemanticError as e:
        print(f"\n[Reparo] Semantic error:\n  {e}")
        sys.exit(1)

    # Stage 4 — Interpreter (stub)
    _print_section("Execution")
    Interpreter().run(ast)

    print("\n[Reparo] Done.\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """
    Dispatches CLI sub-commands.

    reparo run   <file.rpl>
    reparo lex   <file.rpl>
    reparo parse <file.rpl>
    """
    usage = (
        "Usage:\n"
        "  reparo run   <file.rpl>   — compile and run a Replon program\n"
        "  reparo lex   <file.rpl>   — show the token stream only\n"
        "  reparo parse <file.rpl>   — show the AST only\n"
    )

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(0)

    command   = sys.argv[1].lower()
    file_path = sys.argv[2]

    commands = {
        'run':   cmd_run,
        'lex':   cmd_lex,
        'parse': cmd_parse,
    }

    if command not in commands:
        print(f"[Reparo] Unknown command: '{command}'\n")
        print(usage)
        sys.exit(1)

    commands[command](file_path)


if __name__ == "__main__":
    main()
