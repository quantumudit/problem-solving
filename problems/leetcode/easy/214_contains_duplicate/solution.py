class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hash = {}
        for i in nums:
            hash[i] = hash.get(i, 0) + 1
            if hash[i] > 1:
                return True
        return False