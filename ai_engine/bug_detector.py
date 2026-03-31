# =============================================================================
# bug_detector.py — AI Bug Detector (STUB) for the Reparo self-healing engine
#
# This module will analyse errors (lexer, parser, semantic, runtime) and
# classify them so the error_fixer can suggest or apply corrections.
#
# TODO:
#   1. Accept an exception + the original source string as input.
#   2. Pattern-match against known error signatures (rule-based first).
#   3. Return a structured BugReport: { error_type, line, col, description }.
#   4. Later: feed the BugReport into an ML model for smarter suggestions.
# =============================================================================


class BugReport:
    """Structured description of a detected bug."""

    def __init__(self, error_type: str, line: int, col: int, description: str):
        self.error_type  = error_type
        self.line        = line
        self.col         = col
        self.description = description

    def __repr__(self) -> str:
        return (
            f"[BugReport] {self.error_type} at line {self.line}, col {self.col}: "
            f"{self.description}"
        )


class BugDetector:
    """
    Analyses compiler errors and produces BugReports.

    TODO: Implement rule-based pattern matching against common Replon mistakes.
    """

    def detect(self, error: Exception, source: str) -> BugReport | None:
        """
        Stub — returns None until detection logic is implemented.
        """
        return None
