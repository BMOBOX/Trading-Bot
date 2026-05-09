VALID_ORDER_TYPES = {"market", "limit", "stop-limit"}


def normalize_order_type(order_type: str) -> str:
    mapping = {
        "market":     "MARKET",
        "limit":      "LIMIT",
        "stop-limit": "STOP",
        "stop limit": "STOP",
        "stoplimit":  "STOP",
    }
    normalized = mapping.get(order_type.strip().lower())
    if not normalized:
        raise ValueError(f"Invalid order type: '{order_type}'")
    return normalized


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
        parse_positive_float(value, "Quantity")
        return True
    except ValueError as e:
        return str(e)
