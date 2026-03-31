# =============================================================================
# lexer.py — Lexer (tokeniser) for the Reparo compiler
#
# The lexer reads raw Replon source code character-by-character and produces
# a flat list of Token objects that the parser will consume.
#
# Supported constructs:
#   - Integer and float number literals
#   - String literals (double-quoted, with basic escape sequences)
#   - Identifiers and reserved keywords
#   - Arithmetic, comparison, and logical operators
#   - Punctuation and parentheses
#   - Single-line comments  (#  …)
#   - Newlines (used as statement separators)
# =============================================================================

try:
    # When imported as a package from the project root: `from lexer.lexer import …`
    from lexer.tokens import Token, KEYWORDS
    from lexer.tokens import (
        T_KEYWORD, T_IDENTIFIER, T_NUMBER, T_STRING,
        T_OPERATOR, T_PUNCTUATION, T_PARENTHESIS,
        T_NEWLINE, T_EOF,
    )
except ImportError:
    # When run directly from inside the lexer/ directory: `python lexer.py`
    from tokens import Token, KEYWORDS
    from tokens import (
        T_KEYWORD, T_IDENTIFIER, T_NUMBER, T_STRING,
        T_OPERATOR, T_PUNCTUATION, T_PARENTHESIS,
        T_NEWLINE, T_EOF,
    )


class LexerError(Exception):
    """Raised when the lexer encounters an unexpected character."""

    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"[LexerError] Line {line}, Col {col}: {message}")
        self.line = line
        self.col  = col


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

class Lexer:
    """
    Converts a Replon source string into a list of Token objects.

    Usage:
        lexer  = Lexer(source_code)
        tokens = lexer.tokenize()
    """

    def __init__(self, text: str):
        self.text = text
        self.pos  = 0
        self.line = 1   # current line number (1-based)
        self.col  = 1   # current column number (1-based)

        # Initialise current_char; None when the source is empty.
        self.current_char = self.text[0] if text else None

    # ------------------------------------------------------------------
    # Low-level navigation helpers
    # ------------------------------------------------------------------

    def _advance(self):
        """Move the cursor one character forward, tracking line/col."""
        if self.current_char == '\n':
            self.line += 1
            self.col   = 1
        else:
            self.col += 1

        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def _peek(self) -> str | None:
        """Return the next character without advancing (look-ahead by 1)."""
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def _current_pos(self) -> tuple[int, int]:
        """Return (line, col) snapshot for error reporting."""
        return self.line, self.col

    # ------------------------------------------------------------------
    # Skip helpers
    # ------------------------------------------------------------------

    def _skip_whitespace(self):
        """Consume spaces and tabs (but NOT newlines — they are tokens)."""
        while self.current_char is not None and self.current_char in ' \t':
            self._advance()

    def _skip_comment(self):
        """Consume everything from '#' to the end of the line."""
        while self.current_char is not None and self.current_char != '\n':
            self._advance()

    # ------------------------------------------------------------------
    # Token extraction helpers
    # ------------------------------------------------------------------

    def _read_number(self) -> Token:
        """
        Consume an integer or float literal.
        Examples: 42  |  3.14  |  0.5
        """
        line, col = self._current_pos()
        result = ''

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()

        # Check for a decimal point followed by more digits (float).
        if self.current_char == '.' and self._peek() is not None and self._peek().isdigit():
            result += '.'
            self._advance()  # consume '.'
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self._advance()

        return Token(T_NUMBER, result, line, col)

    def _read_string(self) -> Token:
        """
        Consume a double-quoted string literal.
        Supports escape sequences: \\n  \\t  \\\\ \\"
        Example: "hello world"
        """
        line, col = self._current_pos()
        self._advance()  # consume opening '"'
        result = ''

        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self._advance()  # consume backslash
                escapes = {'n': '\n', 't': '\t', '\\': '\\', '"': '"'}
                if self.current_char in escapes:
                    result += escapes[self.current_char]
                else:
                    # Unknown escape — keep it as-is
                    result += '\\' + (self.current_char or '')
            else:
                result += self.current_char
            self._advance()

        if self.current_char is None:
            raise LexerError("Unterminated string literal", line, col)

        self._advance()  # consume closing '"'
        return Token(T_STRING, result, line, col)

    def _read_word(self) -> Token:
        """
        Consume an identifier or keyword.
        Identifiers start with a letter or '_', followed by letters, digits, or '_'.
        """
        line, col = self._current_pos()
        result = ''

        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == '_'
        ):
            result += self.current_char
            self._advance()

        token_type = T_KEYWORD if result in KEYWORDS else T_IDENTIFIER
        return Token(token_type, result, line, col)

    # ------------------------------------------------------------------
    # Main tokenisation logic
    # ------------------------------------------------------------------

    def get_next_token(self) -> Token:
        """
        Return the next token from the source.
        Raises LexerError on an unrecognised character.
        """
        while self.current_char is not None:

            # --- Whitespace (spaces / tabs) ---
            if self.current_char in ' \t':
                self._skip_whitespace()
                continue

            # --- Single-line comment ---
            if self.current_char == '#':
                self._skip_comment()
                continue

            # --- Newline (statement separator) ---
            if self.current_char == '\n':
                line, col = self._current_pos()
                self._advance()
                return Token(T_NEWLINE, '\n', line, col)

            # --- Parentheses ---
            if self.current_char in '()':
                line, col = self._current_pos()
                ch = self.current_char
                self._advance()
                return Token(T_PARENTHESIS, ch, line, col)

            # --- Punctuation ---
            if self.current_char in '{}[];,':
                line, col = self._current_pos()
                ch = self.current_char
                self._advance()
                return Token(T_PUNCTUATION, ch, line, col)

            # --- Number literal ---
            if self.current_char.isdigit():
                return self._read_number()

            # --- String literal ---
            if self.current_char == '"':
                return self._read_string()

            # --- Identifier / keyword ---
            if self.current_char.isalpha() or self.current_char == '_':
                return self._read_word()

            # --- Two-character operators (must be checked before single-char) ---
            line, col = self._current_pos()

            if self.current_char == '=' and self._peek() == '=':
                self._advance(); self._advance()
                return Token(T_OPERATOR, '==', line, col)

            if self.current_char == '!' and self._peek() == '=':
                self._advance(); self._advance()
                return Token(T_OPERATOR, '!=', line, col)

            if self.current_char == '<' and self._peek() == '=':
                self._advance(); self._advance()
                return Token(T_OPERATOR, '<=', line, col)

            if self.current_char == '>' and self._peek() == '=':
                self._advance(); self._advance()
                return Token(T_OPERATOR, '>=', line, col)

            # --- Single-character operators ---
            if self.current_char in '=+-*/%<>!&|^~':
                ch = self.current_char
                self._advance()
                return Token(T_OPERATOR, ch, line, col)

            # --- Unrecognised character ---
            raise LexerError(
                f"Unexpected character {self.current_char!r}",
                self.line, self.col,
            )

        # End of source
        return Token(T_EOF, None, self.line, self.col)

    def tokenize(self) -> list[Token]:
        """
        Convenience method — tokenise the entire source and return all tokens.
        The list always ends with a T_EOF token.
        """
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == T_EOF:
                break
        return tokens
