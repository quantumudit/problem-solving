class Solution:
    def maxArea(self, height: List[int]) -> int:
        area = 0
        left = 0
        right = len(height) - 1

        while left < right:
            h = min(height[left], height[right])
            w = right - left
            area = max(area, h * w)

            if height[left] > height[right]:
                right -= 1
            elif height[left] < height[right]:
                left += 1
            else:  # equal heights: moving either side is fine
                left += 1
                right -= 1

        return area
