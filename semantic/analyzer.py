# =============================================================================
# analyzer.py — Semantic Analyser (STUB) for the Reparo compiler
#
# The semantic analyser walks the AST produced by the parser and checks for
# meaning-level errors that the parser cannot catch — things like:
#   - Using a variable before it is defined
#   - Type mismatches (e.g. adding a number to a string)
#   - Returning a value from outside a function
#
# TODO (implement in the next phase):
#   1. Build a symbol table — track every variable name and its type.
#   2. Scope management — push/pop scopes for if/while/function bodies.
#   3. Type inference — infer and propagate types through expressions.
#   4. Error collection — gather ALL semantic errors before stopping,
#      so the user sees every problem at once (like a real compiler).
#   5. Hook into the AI self-healing engine to suggest fixes for
#      common semantic mistakes (e.g. undefined variable → "did you mean X?").
# =============================================================================


class SemanticError(Exception):
    """Raised when a semantic rule is violated."""
    pass


class SemanticAnalyzer:
    """
    Walks the AST and enforces semantic rules.

    Usage (once implemented):
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast_nodes)   # raises SemanticError on violations
    """

    def analyze(self, nodes: list):
        """
        Entry point — receives the list of AST nodes from the parser.

        TODO: Replace this stub with a real tree-walk.
        """
        # Stub: nothing to check yet — just pass the AST through unchanged.
        return nodes
