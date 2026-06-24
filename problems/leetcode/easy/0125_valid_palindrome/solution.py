import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = re.sub(r"[\W_]", "", s, flags=re.IGNORECASE).lower()
        return cleaned == cleaned[::-1]
