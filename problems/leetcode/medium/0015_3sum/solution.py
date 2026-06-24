class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()

        result = set()  # set handles dedup automatically

        for i in range(len(nums)):
            x = nums[i]
            l = i + 1
            r = len(nums) - 1
            for _ in range(i + 1, len(nums)):  # bounded; l/r control actual movement
                if l < r:
                    if x + nums[l] + nums[r] < 0:
                        l += 1
                    elif x + nums[l] + nums[r] > 0:
                        r -= 1
                    else:
                        result.add((x, nums[l], nums[r]))
                        l += 1
                        r -= 1

        return [list(t) for t in list(result)]
