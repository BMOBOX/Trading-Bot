from binance.exceptions import BinanceAPIException
from requests.exceptions import Timeout, ConnectionError, RequestException
from bot.client import BinanceConnect
from utils.logger import logger, api_logger


client = BinanceConnect()


def _validate_side(side: str) -> str:
    side_upper = side.upper()
    if side_upper not in {"BUY", "SELL"}:
        raise ValueError("side must be either 'BUY' or 'SELL'")
    return side_upper


def market_order(symbol: str, side: str, quantity: float) -> dict:
    side = _validate_side(side)
    api_logger.info(f"REQUEST  futures_create_order | symbol={symbol} side={side} type=MARKET quantity={quantity}")
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        logger.success(f"Market order placed successfully: {side} {quantity} {symbol.upper()}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        logger.error(f"Network error: {e}")

def limit_order(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    side = _validate_side(side)
    api_logger.info(f"REQUEST  futures_create_order | symbol={symbol} side={side} type=LIMIT quantity={quantity}")
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=str(price),
            timeInForce=time_in_force,
        )
        logger.success(f"Limit order placed successfully: {side} {quantity} {symbol.upper()} @ {price}")
        return order
    except BinanceAPIException as e:
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        logger.error(f"Network error: {e}")


def stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
    limit_price: float,
    time_in_force: str = "GTC",
) -> dict:
    side = _validate_side(side)
    api_logger.info(f"REQUEST  futures_create_order | symbol={symbol} side={side} type=STOP_LIMIT quantity={quantity}")
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=str(stop_price),
            price=str(limit_price),
            timeInForce=time_in_force,
        )
        logger.success(
            "Stop-limit order placed successfully: "
            f"{side} {quantity} {symbol.upper()} stop {stop_price} limit {limit_price}"
        )
        return order
    except BinanceAPIException as e:
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        logger.error(f"Network error: {e}")
