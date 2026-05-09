from bot.client import BinanceConnect

client = BinanceConnect()


def normalize_symbol(symbol: str) -> str:
    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValueError("Ticker is required")
    return cleaned


def ensure_symbol_exists(symbol: str) -> str:
    symbol_info = client.get_symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol '{symbol}' not found on Binance")
    return symbol


def validate_symbol_input_api(value: str) -> bool | str:
    try:
        ensure_symbol_exists(normalize_symbol(value))
        return True
    except ValueError as e:
        return str(e)
