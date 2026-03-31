# =============================================================================
# parser.py — Recursive-descent parser for the Reparo compiler
#
# The parser consumes the flat token stream produced by the lexer and builds
# an Abstract Syntax Tree (AST) made up of the node types in ast/nodes.py.
#
# Grammar (informal, top-down):
#
#   program        → statement* EOF
#   statement      → assignment | print_stmt | if_stmt | while_stmt | expression
#   assignment     → IDENTIFIER '=' expression NEWLINE?
#   print_stmt     → 'print' '(' expression ')' NEWLINE?
#   if_stmt        → 'if' expression '{' statement* '}'
#                    ('elif' expression '{' statement* '}')*
#                    ('else' '{' statement* '}')?
#   while_stmt     → 'while' expression '{' statement* '}'
#   expression     → comparison (('and'|'or') comparison)*
#   comparison     → term (('=='|'!='|'<'|'>'|'<='|'>=') term)*
#   term           → factor (('+' | '-') factor)*
#   product        → unary  (('*' | '/' | '%') unary)*
#   unary          → ('-' | 'not') unary | primary
#   primary        → NUMBER | STRING | 'true' | 'false' | 'null'
#                  | IDENTIFIER | '(' expression ')'
# =============================================================================

import sys
import os

# ---------------------------------------------------------------------------
# Path fix: allow `from lexer.tokens import …` when running from project root,
# and also allow running parser/ directly during development.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer.tokens import (
    Token, KEYWORDS,
    T_KEYWORD, T_IDENTIFIER, T_NUMBER, T_STRING,
    T_OPERATOR, T_PUNCTUATION, T_PARENTHESIS,
    T_NEWLINE, T_EOF,
)
from parser.ast.nodes import (
    NumberNode, StringNode, BoolNode, NullNode,
    IdentifierNode, BinOpNode, UnaryOpNode,
    AssignmentNode, PrintNode, IfNode, WhileNode,
)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class ParseError(Exception):
    """Raised when the parser encounters unexpected tokens."""

    def __init__(self, message: str, token: Token):
        location = f"line {token.line}, col {token.col}" if token.line else ""
        super().__init__(f"[ParseError] {message} (got {token!r}{' at ' + location if location else ''})")
        self.token = token


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class Parser:
    """
    Recursive-descent parser for the Replon language.

    Usage:
        parser = Parser(tokens)
        ast    = parser.parse()   # returns a list of statement nodes
    """

    def __init__(self, tokens: list[Token]):
        # Filter out newlines at the top level — we handle them explicitly
        # only where they matter (e.g. as statement terminators).
        self.tokens = tokens
        self.pos    = 0
        self.current_tok: Token = self.tokens[0] if tokens else Token(T_EOF, None)

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def _advance(self) -> Token:
        """Move to the next token and return it."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]
        return self.current_tok

    def _peek(self, offset: int = 1) -> Token | None:
        """Look ahead by `offset` positions without consuming tokens."""
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def _skip_newlines(self):
        """Consume any number of consecutive NEWLINE tokens."""
        while self.current_tok.type == T_NEWLINE:
            self._advance()

    def _expect(self, type_: str, value=None) -> Token:
        """
        Assert the current token matches the expected type (and optionally value).
        Consumes and returns the token on success; raises ParseError on failure.
        """
        tok = self.current_tok
        if tok.type != type_:
            expected = f"{type_!r}" + (f" '{value}'" if value is not None else "")
            raise ParseError(f"Expected {expected}", tok)
        if value is not None and tok.value != value:
            raise ParseError(f"Expected '{value}'", tok)
        self._advance()
        return tok

    def _match(self, type_: str, value=None) -> bool:
        """Return True (without consuming) if the current token matches."""
        if self.current_tok.type != type_:
            return False
        if value is not None and self.current_tok.value != value:
            return False
        return True

    # ------------------------------------------------------------------
    # Top-level entry point
    # ------------------------------------------------------------------

    def parse(self) -> list:
        """
        Parse the entire token stream and return a list of statement nodes.
        This is the root of the grammar: program → statement* EOF
        """
        statements = []
        self._skip_newlines()

        while self.current_tok.type != T_EOF:
            stmt = self._statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()

        return statements

    # ------------------------------------------------------------------
    # Statement parsing
    # ------------------------------------------------------------------

    def _statement(self):
        """
        Dispatch to the correct statement parser based on the current token.
        Falls back to parsing a bare expression (e.g. a function call).
        """
        tok = self.current_tok

        # Assignment: IDENTIFIER '=' …
        if tok.type == T_IDENTIFIER:
            next_tok = self._peek()
            if next_tok and next_tok.type == T_OPERATOR and next_tok.value == '=':
                return self._assignment()

        # print(…)
        if tok.type == T_KEYWORD and tok.value == 'print':
            return self._print_stmt()

        # if …
        if tok.type == T_KEYWORD and tok.value == 'if':
            return self._if_stmt()

        # while …
        if tok.type == T_KEYWORD and tok.value == 'while':
            return self._while_stmt()

        # Bare expression (e.g. a standalone arithmetic expression)
        return self._expression()

    def _assignment(self):
        """
        assignment → IDENTIFIER '=' expression NEWLINE?
        """
        name_tok = self._expect(T_IDENTIFIER)
        self._expect(T_OPERATOR, '=')
        value = self._expression()
        # Optional trailing newline
        if self._match(T_NEWLINE):
            self._advance()
        return AssignmentNode(name_tok, value)

    def _print_stmt(self):
        """
        print_stmt → 'print' '(' expression ')' NEWLINE?
        """
        self._expect(T_KEYWORD, 'print')
        self._expect(T_PARENTHESIS, '(')
        expr = self._expression()
        self._expect(T_PARENTHESIS, ')')
        if self._match(T_NEWLINE):
            self._advance()
        return PrintNode(expr)

    def _if_stmt(self):
        """
        if_stmt → 'if' expression '{' statement* '}'
                  ('elif' expression '{' statement* '}')*
                  ('else' '{' statement* '}')?
        """
        self._expect(T_KEYWORD, 'if')
        condition = self._expression()
        body      = self._block()

        elif_cases = []
        while self._match(T_KEYWORD, 'elif'):
            self._advance()  # consume 'elif'
            elif_cond = self._expression()
            elif_body = self._block()
            elif_cases.append((elif_cond, elif_body))

        else_body = None
        if self._match(T_KEYWORD, 'else'):
            self._advance()  # consume 'else'
            else_body = self._block()

        return IfNode(condition, body, elif_cases, else_body)

    def _while_stmt(self):
        """
        while_stmt → 'while' expression '{' statement* '}'
        """
        self._expect(T_KEYWORD, 'while')
        condition = self._expression()
        body      = self._block()
        return WhileNode(condition, body)

    def _block(self) -> list:
        """
        block → '{' NEWLINE? statement* '}'
        Parse a brace-delimited block and return its statements as a list.
        """
        self._expect(T_PUNCTUATION, '{')
        self._skip_newlines()

        statements = []
        while not self._match(T_PUNCTUATION, '}'):
            if self.current_tok.type == T_EOF:
                raise ParseError("Unexpected EOF — missing closing '}'", self.current_tok)
            stmt = self._statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()

        self._expect(T_PUNCTUATION, '}')
        return statements

    # ------------------------------------------------------------------
    # Expression parsing  (operator precedence via recursive descent)
    # ------------------------------------------------------------------

    def _expression(self):
        """
        expression → comparison (('and' | 'or') comparison)*
        Lowest precedence — logical operators.
        """
        left = self._comparison()

        while self.current_tok.type == T_KEYWORD and self.current_tok.value in ('and', 'or'):
            op_tok = self.current_tok
            self._advance()
            right = self._comparison()
            left  = BinOpNode(left, op_tok, right)

        return left

    def _comparison(self):
        """
        comparison → term (('==' | '!=' | '<' | '>' | '<=' | '>=') term)*
        """
        left = self._term()

        while (
            self.current_tok.type == T_OPERATOR
            and self.current_tok.value in ('==', '!=', '<', '>', '<=', '>=')
        ):
            op_tok = self.current_tok
            self._advance()
            right = self._term()
            left  = BinOpNode(left, op_tok, right)

        return left

    def _term(self):
        """
        term → product (('+' | '-') product)*
        """
        left = self._product()

        while self.current_tok.type == T_OPERATOR and self.current_tok.value in ('+', '-'):
            op_tok = self.current_tok
            self._advance()
            right = self._product()
            left  = BinOpNode(left, op_tok, right)

        return left

    def _product(self):
        """
        product → unary (('*' | '/' | '%') unary)*
        """
        left = self._unary()

        while self.current_tok.type == T_OPERATOR and self.current_tok.value in ('*', '/', '%'):
            op_tok = self.current_tok
            self._advance()
            right = self._unary()
            left  = BinOpNode(left, op_tok, right)

        return left

    def _unary(self):
        """
        unary → ('-' | 'not') unary | primary
        Handles unary minus and logical not.
        """
        # Unary minus
        if self.current_tok.type == T_OPERATOR and self.current_tok.value == '-':
            op_tok = self.current_tok
            self._advance()
            return UnaryOpNode(op_tok, self._unary())

        # Logical not
        if self.current_tok.type == T_KEYWORD and self.current_tok.value == 'not':
            op_tok = self.current_tok
            self._advance()
            return UnaryOpNode(op_tok, self._unary())

        return self._primary()

    def _primary(self):
        """
        primary → NUMBER | STRING | 'true' | 'false' | 'null'
                | IDENTIFIER | '(' expression ')'
        Highest precedence — atomic values and grouped expressions.
        """
        tok = self.current_tok

        # Number literal
        if tok.type == T_NUMBER:
            self._advance()
            return NumberNode(tok)

        # String literal
        if tok.type == T_STRING:
            self._advance()
            return StringNode(tok)

        # Boolean literals
        if tok.type == T_KEYWORD and tok.value in ('true', 'false'):
            self._advance()
            return BoolNode(tok)

        # Null literal
        if tok.type == T_KEYWORD and tok.value == 'null':
            self._advance()
            return NullNode(tok)

        # Identifier (variable reference)
        if tok.type == T_IDENTIFIER:
            self._advance()
            return IdentifierNode(tok)

        # Grouped expression: '(' expression ')'
        if tok.type == T_PARENTHESIS and tok.value == '(':
            self._advance()
            expr = self._expression()
            self._expect(T_PARENTHESIS, ')')
            return expr

        raise ParseError("Unexpected token in expression", tok)
