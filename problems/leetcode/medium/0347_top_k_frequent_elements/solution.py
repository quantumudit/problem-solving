class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1

        # sort descending by frequency, take top k keys
        return [
            num for num, _ in sorted(count.items(), key=lambda item: item[1], reverse=True)
        ][:k]
