# =============================================================================
# error_fixer.py — AI Error Fixer (STUB) for the Reparo self-healing engine
#
# Given a BugReport from bug_detector.py, this module suggests (or applies)
# a fix to the source code.
#
# TODO:
#   1. Accept a BugReport and the original source string.
#   2. Rule-based fixes first:
#        - Missing closing bracket/brace → insert it
#        - Undefined variable → suggest closest name (Levenshtein distance)
#        - Wrong operator (= vs ==) → suggest correction
#   3. Return a FixSuggestion: { description, patched_source (optional) }.
#   4. Later: use an LLM to generate natural-language explanations + patches.
# =============================================================================

from ai_engine.bug_detector import BugReport


class FixSuggestion:
    """A human-readable fix suggestion, optionally with a patched source."""

    def __init__(self, description: str, patched_source: str | None = None):
        self.description    = description
        self.patched_source = patched_source

    def __repr__(self) -> str:
        return f"[FixSuggestion] {self.description}"


class ErrorFixer:
    """
    Produces fix suggestions from BugReports.

    TODO: Implement rule-based and later ML-based fix generation.
    """

    def suggest(self, report: BugReport, source: str) -> FixSuggestion | None:
        """
        Stub — returns None until fix logic is implemented.
        """
        return None
