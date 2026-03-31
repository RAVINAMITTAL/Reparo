# =============================================================================
# tokens.py — Token type definitions and Token class for the Reparo compiler
#
# A token is the smallest meaningful unit in source code.
# The lexer breaks raw source text into a stream of these tokens.
# =============================================================================

# ---------------------------------------------------------------------------
# Token type constants
# ---------------------------------------------------------------------------

T_KEYWORD     = 'KEYWORD'      # Reserved words: if, else, return, print, etc.
T_IDENTIFIER  = 'IDENTIFIER'   # Variable / function names: x, myVar, foo
T_NUMBER      = 'NUMBER'       # Integer or float literals: 42, 3.14
T_STRING      = 'STRING'       # String literals: "hello"
T_OPERATOR    = 'OPERATOR'     # Arithmetic / comparison / logical operators
T_PUNCTUATION = 'PUNCTUATION'  # Structural chars: { } ; ,
T_PARENTHESIS = 'PARENTHESIS'  # Grouping chars: ( )
T_NEWLINE     = 'NEWLINE'      # Line separator (used for statement boundaries)
T_EOF         = 'EOF'          # End of file — signals the lexer is done

# ---------------------------------------------------------------------------
# Reserved keywords for the Replon language
# Centralised here so both the lexer and parser share the same source of truth.
# ---------------------------------------------------------------------------

KEYWORDS = {
    'if', 'else', 'elif', 'while', 'for',
    'return', 'print', 'true', 'false', 'null',
    'and', 'or', 'not',
}


# ---------------------------------------------------------------------------
# Token class
# ---------------------------------------------------------------------------

class Token:
    """
    Represents a single lexical token produced by the lexer.

    Attributes:
        type  (str): One of the T_* constants defined above.
        value (str | None): The raw text of the token, or None for EOF.
        line  (int): Source line number (1-based) — useful for error messages.
        col   (int): Column number (1-based) — useful for error messages.
    """

    def __init__(self, type_: str, value, line: int = 0, col: int = 0):
        self.type  = type_
        self.value = value
        self.line  = line
        self.col   = col

    def __repr__(self) -> str:
        if self.type == T_NEWLINE:
            return f"Token({self.type}, '\\n')"
        if self.type == T_EOF:
            return f"Token({self.type})"
        return f"Token({self.type}, {self.value!r})"
