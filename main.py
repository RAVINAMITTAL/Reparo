# =============================================================================
# main.py — Reparo Compiler Entry Point
#
# Usage:
#   python main.py <file.rpl>
#   python main.py              (defaults to lexer/tests/test1.rpl)
#
# Pipeline (current):
#   Source (.rpl)
#     └─► Lexer        → Token stream
#           └─► Parser → AST
#
# Pipeline (full — future):
#   Source → Lexer → Parser → Semantic Analyser → Interpreter
#                                                       └─► AI Self-Healing Engine
# =============================================================================

import sys
import os


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_section(title: str):
    """Print a clearly visible section header."""
    bar = "─" * 60
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def _print_tokens(tokens):
    """Pretty-print the token stream from the lexer."""
    _print_section("LEXER OUTPUT — Token Stream")
    for tok in tokens:
        print(f"  {tok}")


def _print_ast(nodes):
    """Pretty-print the AST nodes from the parser."""
    _print_section("PARSER OUTPUT — Abstract Syntax Tree")
    for node in nodes:
        print(f"  {node!r}")


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def compile_file(file_path: str):
    """
    Run the Reparo compiler pipeline on a .rpl source file.

    Currently executes: Lexer → Parser
    Prints both outputs so you can verify each stage.
    """

    # --- Read source ---
    if not os.path.exists(file_path):
        print(f"[Reparo] Error: file not found — '{file_path}'")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"\n[Reparo] Compiling: {file_path}")

    # ── Stage 1: Lexer ────────────────────────────────────────────────
    from lexer.lexer import Lexer, LexerError

    try:
        lexer  = Lexer(source)
        tokens = lexer.tokenize()
    except LexerError as e:
        print(f"\n[Reparo] Lexer error:\n  {e}")
        # TODO: pass error to BugDetector / ErrorFixer once implemented
        sys.exit(1)

    _print_tokens(tokens)

    # ── Stage 2: Parser ───────────────────────────────────────────────
    from parser.parser import Parser, ParseError

    try:
        parser = Parser(tokens)
        ast    = parser.parse()
    except ParseError as e:
        print(f"\n[Reparo] Parse error:\n  {e}")
        # TODO: pass error to BugDetector / ErrorFixer once implemented
        sys.exit(1)

    _print_ast(ast)

    # ── Stage 3: Semantic Analyser (stub) ─────────────────────────────
    from semantic.analyzer import SemanticAnalyzer, SemanticError

    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
    except SemanticError as e:
        print(f"\n[Reparo] Semantic error:\n  {e}")
        sys.exit(1)

    # ── Stage 4: Interpreter (stub) ───────────────────────────────────
    from executor.interpreter import Interpreter

    interpreter = Interpreter()
    interpreter.run(ast)

    # ── Done ──────────────────────────────────────────────────────────
    _print_section("Done")
    print("  Compilation finished successfully.\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "lexer/tests/test1.rpl"
    compile_file(path)
