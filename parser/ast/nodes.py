# =============================================================================
# nodes.py — AST (Abstract Syntax Tree) node definitions for Reparo
#
# Each class represents one kind of syntactic construct in the Replon language.
# The parser builds a tree of these nodes; later stages (semantic analyser,
# interpreter, code generator) walk that tree.
#
# Node hierarchy (so far):
#
#   Expression nodes
#   ├── NumberNode       — numeric literal  e.g. 42, 3.14
#   ├── StringNode       — string literal   e.g. "hello"
#   ├── BoolNode         — boolean literal  true / false
#   ├── NullNode         — null literal
#   ├── IdentifierNode   — variable name    e.g. x
#   ├── BinOpNode        — binary operation e.g. a + b
#   └── UnaryOpNode      — unary operation  e.g. -x, not flag
#
#   Statement nodes
#   ├── AssignmentNode   — variable assignment  e.g. x = 5
#   ├── PrintNode        — print statement      e.g. print(x)
#   ├── IfNode           — if / elif / else      e.g. if a > b { … }
#   └── WhileNode        — while loop            e.g. while x > 0 { … }
# =============================================================================


# ---------------------------------------------------------------------------
# Expression nodes
# ---------------------------------------------------------------------------

class NumberNode:
    """
    A numeric literal (integer or float).

    Attributes:
        token: The original NUMBER token.
        value: Python int or float parsed from the token.
    """

    def __init__(self, token):
        self.token = token
        # Store as float if the literal contains a '.', otherwise int.
        self.value = float(token.value) if '.' in token.value else int(token.value)

    def __repr__(self) -> str:
        return repr(self.value)


class StringNode:
    """
    A string literal.

    Attributes:
        token: The original STRING token.
        value: The string content (escape sequences already resolved by lexer).
    """

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f'"{self.value}"'


class BoolNode:
    """
    A boolean literal: true or false.

    Attributes:
        token: The original KEYWORD token ('true' or 'false').
        value: Python bool.
    """

    def __init__(self, token):
        self.token = token
        self.value = token.value == 'true'

    def __repr__(self) -> str:
        return str(self.value)


class NullNode:
    """
    The null literal.

    Attributes:
        token: The original KEYWORD token ('null').
    """

    def __init__(self, token):
        self.token = token

    def __repr__(self) -> str:
        return 'null'


class IdentifierNode:
    """
    A reference to a variable or name.

    Attributes:
        token: The original IDENTIFIER token.
        name:  The identifier string.
    """

    def __init__(self, token):
        self.token = token
        self.name  = token.value

    def __repr__(self) -> str:
        return self.name


class BinOpNode:
    """
    A binary operation: left OP right.

    Examples: a + b,  x == y,  i * 2

    Attributes:
        left:     Left-hand side expression node.
        op_token: The operator Token (e.g. '+', '==').
        right:    Right-hand side expression node.
    """

    def __init__(self, left, op_token, right):
        self.left     = left
        self.op_token = op_token
        self.right    = right

    def __repr__(self) -> str:
        return f"({self.left} {self.op_token.value} {self.right})"


class UnaryOpNode:
    """
    A unary operation: OP operand.

    Examples: -x,  not flag

    Attributes:
        op_token: The operator Token (e.g. '-', 'not').
        operand:  The expression the operator applies to.
    """

    def __init__(self, op_token, operand):
        self.op_token = op_token
        self.operand  = operand

    def __repr__(self) -> str:
        return f"({self.op_token.value} {self.operand})"


# ---------------------------------------------------------------------------
# Statement nodes
# ---------------------------------------------------------------------------

class AssignmentNode:
    """
    A variable assignment: name = value.

    Attributes:
        name_token: The IDENTIFIER token for the variable name.
        name:       The variable name string.
        value:      The expression node for the assigned value.
    """

    def __init__(self, name_token, value):
        self.name_token = name_token
        self.name       = name_token.value
        self.value      = value

    def __repr__(self) -> str:
        return f"(ASSIGN {self.name} = {self.value})"


class PrintNode:
    """
    A print statement: print(expr).

    Attributes:
        expr: The expression node whose value will be printed.
    """

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self) -> str:
        return f"(PRINT {self.expr})"


class IfNode:
    """
    An if / elif / else construct.

    Attributes:
        condition:   Expression node for the if condition.
        body:        List of statement nodes for the if branch.
        elif_cases:  List of (condition, body) tuples for elif branches.
        else_body:   List of statement nodes for the else branch (or None).
    """

    def __init__(self, condition, body, elif_cases=None, else_body=None):
        self.condition  = condition
        self.body       = body
        self.elif_cases = elif_cases or []
        self.else_body  = else_body

    def __repr__(self) -> str:
        return f"(IF {self.condition} THEN {self.body})"


class WhileNode:
    """
    A while loop: while condition { body }.

    Attributes:
        condition: Expression node for the loop condition.
        body:      List of statement nodes forming the loop body.
    """

    def __init__(self, condition, body):
        self.condition = condition
        self.body      = body

    def __repr__(self) -> str:
        return f"(WHILE {self.condition} DO {self.body})"
