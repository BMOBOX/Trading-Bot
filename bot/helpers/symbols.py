from requests.exceptions import ConnectionError, Timeout, RequestException
from binance.exceptions import BinanceAPIException
from bot.client import BinanceConnect

client = BinanceConnect()

def normalize_symbol(symbol: str) -> str:
    """
        Strip and uppercase symbol, enforce USDT suffix for USDT-M futures.
    """

    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValueError("Ticker is required")
    if not cleaned.endswith("USDT"):
        raise ValueError(f"Symbol must end with USDT for USDT-M futures, got '{cleaned}'")
    return cleaned

def ensure_symbol_exists(symbol: str) -> str:
    """
        Hit Binance to confirm symbol is tradeable. Raises ValueError on any failure.
    """

    try:
        if client.get_symbol_info(symbol) is None:
            raise ValueError(f"'{symbol}' not found on Binance")
        return symbol
    except BinanceAPIException as e:
        raise ValueError(f"Binance rejected symbol check: {e.message}")
    except Timeout:
        raise ValueError("Timed out validating symbol — check your connection")
    except ConnectionError:
        raise ValueError("Could not reach Binance — check your internet")
    except RequestException as e:
        raise ValueError(f"Network error: {e}")

def validate_symbol_input_api(value: str) -> bool | str:
    """
        Questionary validate= callback — returns True or an error string.
    """

    try:
        ensure_symbol_exists(normalize_symbol(value))
        return True
    except ValueError as e:
        return str(e)
