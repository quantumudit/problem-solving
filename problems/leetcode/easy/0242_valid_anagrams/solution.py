class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) == len(t):
            s_count = {}
            t_count = {}
            for i in range(len(s)):
                s_count[s[i]] = s_count.get(s[i], 0) + 1
                t_count[t[i]] = t_count.get(t[i], 0) + 1
            return s_count == t_count
        return False
