# =============================================================================
# interpreter.py — Tree-Walk Interpreter (STUB) for the Reparo compiler
#
# The interpreter walks the AST and *executes* each node directly —
# no bytecode or machine code is generated; values are computed in Python.
#
# TODO (implement after the semantic analyser):
#   1. Environment / variable store — a dict mapping names → values.
#   2. visit_* methods for every AST node type:
#        visit_NumberNode, visit_StringNode, visit_BoolNode, visit_NullNode
#        visit_BinOpNode  — evaluate left/right, apply operator
#        visit_UnaryOpNode
#        visit_AssignmentNode — evaluate RHS, store in environment
#        visit_PrintNode      — evaluate expr, call Python print()
#        visit_IfNode         — evaluate condition, execute correct branch
#        visit_WhileNode      — loop until condition is false
#   3. Runtime error handling — division by zero, undefined variable, etc.
#   4. Later: function calls, return values, closures.
# =============================================================================


class RuntimeError_(Exception):
    """Raised when a runtime error occurs during interpretation."""
    pass


class Interpreter:
    """
    Executes an AST by walking each node recursively.

    Usage (once implemented):
        interpreter = Interpreter()
        interpreter.run(ast_nodes)
    """

    def __init__(self):
        # TODO: Replace with a proper Environment / scope-stack class.
        self.environment: dict = {}

    def run(self, nodes: list):
        """
        Entry point — receives the list of AST nodes from the semantic analyser.

        TODO: Replace this stub with real node dispatch.
        """
        # Stub: nothing executed yet.
        print("[Interpreter] Execution not yet implemented — coming soon.")
