def check(nums: list[int]) -> bool:
    return nums.count(19) == 2 and nums.count(5) >= 3


if __name__ == "__main__":
    test_cases = [
        ([19, 19, 15, 5, 3, 5, 5, 2], True),
        ([19, 15, 15, 5, 3, 3, 5, 2], False),
        ([19, 19, 5, 5, 5, 5, 5], True),
        ([19, 5, 5, 5], False),
        ([5, 5, 5], False),
        ([19, 19], False),
        ([], False),
    ]

    for i, (nums, expected) in enumerate(test_cases, start=1):
        result = check(nums)
        print(
            f"Test Case {i}: {'PASS' if result == expected else 'FAIL'} - Expected {expected}, Got {result}"
        )
