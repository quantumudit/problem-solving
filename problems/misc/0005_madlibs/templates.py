import re

# -------------------------------------------------------
# Story Templates
# -------------------------------------------------------

TEMPLATES = {
    "adventure": (
        "Once upon a time, a {adjective} {name} set off on a quest to find the lost {noun} "
        "of {place}. Armed with only a {animal} and a strong will to {verb}, {name} crossed "
        "{number} treacherous mountains. The villagers thought it was {emotion}, but {name} "
        "proved them all wrong."
    ),
    "office": (
        "On a {adjective} Monday morning, {name} walked into the office to find the {noun} "
        "completely gone. The manager shouted, 'We need to {verb} before the 9 AM meeting!' "
        "After {number} chaotic hours, the team solved everything using a {food} and sheer "
        "{emotion}. HR sent a {adverb} worded email about it the next day."
    ),
    "space": (
        "Commander {name} piloted the {adjective} spacecraft toward {place}. "
        "The mission: {verb} the rogue {animal} colony before it reached the sun. "
        "With only {number} seconds of oxygen remaining, {name} grabbed the emergency {noun} "
        "and saved the crew. The whole galaxy erupted in {emotion}."
    ),
    "cooking": (
        "Chef {name} was preparing a {adjective} dish for the annual {place} cook-off. "
        "The secret ingredient was {food}, combined {adverb} with exactly {number} drops of "
        "{noun} extract. The judges were so {emotion} that they asked {name} to {verb} the "
        "recipe on live television."
    ),
}

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def get_placeholders(template: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for name in re.findall(r"\{(\w+)\}", template):
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result


def fill_madlib(template: str, words: dict[str, str]) -> str:
    return template.format_map(words)
