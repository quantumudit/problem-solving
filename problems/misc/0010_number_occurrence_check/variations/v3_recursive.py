def check(nums: list[int], count_19: int = 0, count_5: int = 0) -> bool:
    if not nums:
        return count_19 == 2 and count_5 >= 3
    if count_19 > 2:
        return False
    match nums[0]:
        case 19:
            count_19 += 1
        case 5:
            count_5 += 1
    return check(nums[1:], count_19, count_5)


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
