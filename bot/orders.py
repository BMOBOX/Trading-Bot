from binance.exceptions import BinanceAPIException

from bot.client import BinanceConnect
from utils.logger import logger

client = BinanceConnect()


def _validate_side(side: str) -> str:
    side_upper = side.upper()
    if side_upper not in {"BUY", "SELL"}:
        raise ValueError("side must be either 'BUY' or 'SELL'")
    return side_upper


def market_order(symbol: str, side: str, quantity: float) -> dict:
    side = _validate_side(side)
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
        logger.error(f"Failed to place market order: {e}")
        raise


def limit_order(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    side = _validate_side(side)
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
        logger.error(f"Failed to place limit order: {e}")
        raise


def stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
    limit_price: float,
    time_in_force: str = "GTC",
) -> dict:
    side = _validate_side(side)
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="STOP_LOSS_LIMIT",
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
        logger.error(f"Failed to place stop-limit order: {e}")
        raise
