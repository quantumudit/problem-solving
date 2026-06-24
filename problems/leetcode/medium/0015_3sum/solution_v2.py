class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()

        result = []

        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:  # skip duplicate anchor
                continue
            left = i + 1
            right = len(nums) - 1
            while left < right:
                if nums[i] + nums[left] + nums[right] < 0:
                    left += 1
                elif nums[i] + nums[left] + nums[right] > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:  # skip duplicate left
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:  # skip duplicate right
                        right -= 1
        return result
