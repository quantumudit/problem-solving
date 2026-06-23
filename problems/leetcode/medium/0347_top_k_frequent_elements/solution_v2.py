class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        buckets = [[] for _ in range(len(nums) + 1)]  # index = frequency

        for n in nums:
            count[n] = count.get(n, 0) + 1

        for n, c in count.items():
            buckets[c].append(n)

        result = []

        for i in range(len(buckets) - 1, 0, -1):
            for n in buckets[i]:
                result.append(n)
                if len(result) == k:
                    return result
