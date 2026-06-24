class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()

        result = set()  # set handles dedup automatically

        for i in range(len(nums)):
            x = nums[i]
            left = i + 1
            right = len(nums) - 1
            for _ in range(i + 1, len(nums)):  # bounded; left/right control actual movement
                if left < right:
                    if x + nums[left] + nums[right] < 0:
                        left += 1
                    elif x + nums[left] + nums[right] > 0:
                        right -= 1
                    else:
                        result.add((x, nums[left], nums[right]))
                        left += 1
                        right -= 1

        return [list(t) for t in list(result)]
