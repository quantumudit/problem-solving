class Solution:
    def maxArea(self, height: List[int]) -> int:
        area = 0
        l = 0
        r = len(height) - 1

        while l < r:
            h = min(height[l], height[r])
            w = r - l
            area = max(area, h * w)

            if height[l] > height[r]:
                r -= 1
            elif height[l] < height[r]:
                l += 1
            else:  # equal heights: moving either side is fine
                l += 1
                r -= 1

        return area
