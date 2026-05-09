VALID_ORDER_TYPES = {"market", "limit", "stop-limit"}


def normalize_order_type(order_type: str) -> str:
    cleaned = order_type.strip().lower()
    if cleaned not in VALID_ORDER_TYPES:
        raise ValueError("order_type must be one of: market, limit, stop-limit")
    return cleaned


def parse_positive_float(value: float | str, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number")

    if parsed <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    return parsed


def validate_positive_number_input(value: str) -> bool | str:
    try:
        parse_positive_float(value, "Amount")
        return True
    except ValueError as e:
        return str(e)
