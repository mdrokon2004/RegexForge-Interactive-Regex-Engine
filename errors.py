"""
RegexForge Custom Error Types
Defines custom exception classes for lexical, syntax, and processing errors.
"""

class RegexEngineError(Exception):
    """Base exception for all RegexForge engine errors."""
    def __init__(self, message: str, position: int = -1, error_type: str = "EngineError"):
        super().__init__(message)
        self.message = message
        self.position = position
        self.error_type = error_type

    def to_dict(self) -> dict:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "position": self.position
        }


class LexicalError(RegexEngineError):
    """Raised when an invalid character or token sequence is encountered during lexical analysis."""
    def __init__(self, message: str, position: int, found_char: str = ""):
        super().__init__(message, position, "Lexical Error")
        self.found_char = found_char

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["found"] = self.found_char
        return d


class ParseError(RegexEngineError):
    """Raised when syntax rule violations occur during regex parsing."""
    def __init__(self, message: str, position: int, expected: str = "", found: str = ""):
        super().__init__(message, position, "Parse Error")
        self.expected = expected
        self.found = found

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["expected"] = self.expected
        d["found"] = self.found
        return d
