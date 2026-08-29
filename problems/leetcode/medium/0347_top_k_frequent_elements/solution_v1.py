class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        buckets = [[] for _ in range(len(nums) + 1)]  # index = frequency
        count = {}

        for num in nums:
            count[num] = count.get(num, 0) + 1

        for num, freq in count.items():
            buckets[freq].append(num)

        result = []

        for bucket in buckets[::-1]:
            for num in bucket:
                result.append(num)
                if len(result) == k:
                    return result
