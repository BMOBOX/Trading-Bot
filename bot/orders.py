from binance.exceptions import BinanceAPIException

from bot.client import BinanceConnect
from utils.logger import logger

client = BinanceConnect()


def market_order(symbol: str, side: str, quantity: float) -> dict:
    try:
        order = client.create_order(
            symbol=symbol.upper(),
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        logger.info(f"Market order placed: {side} {quantity} {symbol.upper()}")
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
        order = client.create_order(
            symbol=symbol.upper(),
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=str(price),
            timeInForce=time_in_force,
        )
        logger.info(f"Limit order placed: {side} {quantity} {symbol.upper()} @ {price}")
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
        order = client.create_order(
            symbol=symbol.upper(),
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=quantity,
            stopPrice=str(stop_price),
            price=str(limit_price),
            timeInForce=time_in_force,
        )
        logger.info(
            "Stop-limit order placed: "
            f"{side} {quantity} {symbol.upper()} stop {stop_price} limit {limit_price}"
        )
        return order
    except BinanceAPIException as e:
        logger.error(f"Failed to place stop-limit order: {e}")
        raise
