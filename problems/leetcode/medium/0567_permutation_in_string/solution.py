class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1_map = {}

        for i in range(len(s1)):
            s1_map[s1[i]] = s1_map.get(s1[i], 0) + 1

        lo = 0
        hi = lo + len(s1)

        while hi <= len(s2):
            s2_map = {}
            for i in range(lo, hi):
                s2_map[s2[i]] = s2_map.get(s2[i], 0) + 1

            if s1_map == s2_map:
                return True
            else:
                lo += 1
                hi = lo + len(s1)
        return False
