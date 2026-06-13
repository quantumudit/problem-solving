def count_chars(text: str, ignore_case: bool = True) -> list[tuple[str, int]]:
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    processed = text.lower() if ignore_case else text
    freq = {char: processed.count(char) for char in set(processed)}
    return sorted(freq.items(), key=lambda x: -x[1])


def filter_students(students: list[dict], age_limit: int = 21) -> list[dict]:
    return [s for s in students if s["age"] < age_limit]


def get_ranked_sales(transactions: list[dict]) -> list[tuple[str, float]]:
    totals = {
        product: sum(t["sales"] for t in transactions if t["product"] == product)
        for product in {t["product"] for t in transactions}
    }
    return sorted(totals.items(), key=lambda x: -x[1])
