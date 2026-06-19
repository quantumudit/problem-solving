class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = {}
        for word in strs:
            signature = [0] * 26  # one slot per letter a-z
            for char in word:
                signature[ord(char) - ord("a")] += 1
            key = tuple(signature)
            anagrams[key] = anagrams.get(key, []) + [word]

        return list(anagrams.values())
