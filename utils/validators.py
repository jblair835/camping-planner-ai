def validate_positive_int(value: int, name: str):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer.")


def validate_nonempty_string(value: str, name: str):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")


def validate_float(value: float, name: str):
    if not isinstance(value, (int, float)) or value < 0:
        raise ValueError(f"{name} must be a non-negative number.")
