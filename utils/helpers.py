import random

def pick_random(items: list[str]) -> str:
    """Return a random item from a list."""
    return random.choice(items)


def merge_dict_counts(base: dict, additions: dict):
    """Merge two dicts that store item counts."""
    for key, value in additions.items():
        base[key] = base.get(key, 0) + value
    return base


def normalize_style(style: str) -> str:
    """Normalize camping style input."""
    return style.strip().lower()
