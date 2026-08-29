class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = {}
        for word in strs:
            freq = {}
            for char in word:
                freq[char] = freq.get(char, 0) + 1
            key = "".join([f"{k}{v}" for k, v in sorted(freq.items())])
            anagrams[key] = anagrams.get(key, []) + [word]

        return list(anagrams.values())
