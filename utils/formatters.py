def header(text: str) -> str:
    """Format a section header."""
    return f"\n{text}\n" + ("-" * len(text))


def bullet_list(items: list[str]) -> str:
    """Format a list of items as bullet points."""
    return "\n".join(f"- {item}" for item in items)


def indent(text: str, spaces: int = 2) -> str:
    """Indent text by a number of spaces."""
    prefix = " " * spaces
    return "\n".join(prefix + line for line in text.splitlines())
