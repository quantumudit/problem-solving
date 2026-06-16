import re

# -------------------------------------------------------
# Compiled Patterns
# -------------------------------------------------------

_SPECIAL    = re.compile(r"[^\w\s]")
_UPPERCASE  = re.compile(r"[A-Z]")
_LOWERCASE  = re.compile(r"[a-z]")
_WHITESPACE = re.compile(r"\s")
_DIGIT      = re.compile(r"\d")


# -------------------------------------------------------
# TextAnalysis Class
# -------------------------------------------------------

class TextAnalysis:
    def __init__(self, text: str):
        self.text = text

    def special_chars_pos(self) -> list[tuple[str, int]]:
        return [(m.group(), m.start()) for m in _SPECIAL.finditer(self.text)]

    def char_counts(self) -> dict[str, int]:
        return {
            "special_chars":     len(_SPECIAL.findall(self.text)),
            "uppercase_letters": len(_UPPERCASE.findall(self.text)),
            "lowercase_letters": len(_LOWERCASE.findall(self.text)),
            "whitespaces":       len(_WHITESPACE.findall(self.text)),
            "digits":            len(_DIGIT.findall(self.text)),
            "total":             len(self.text),
        }
