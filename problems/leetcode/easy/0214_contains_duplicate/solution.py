class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        count = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1
            if count[num] > 1:  # early exit on first duplicate
                return True
        return False
