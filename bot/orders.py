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
        api_logger.info(f"RESPONSE futures_create_order | orderId={order['orderId']} status={order['status']} executedQty={order['executedQty']} avgPrice={order['avgPrice']}")
        logger.success(f"Market order placed successfully: {side} {quantity} {symbol.upper()}")
        return order
    except BinanceAPIException as e:
        api_logger.error(f"ERROR    POST futures/order | code={e.status_code} msg={e.message}")
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        api_logger.error("NETWORK  POST futures/order | request timed out")
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        api_logger.error("NETWORK  POST futures/order | connection lost")
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        api_logger.error(f"NETWORK  POST futures/order | unexpected error: {e}")
        logger.error(f"Network error: {e}")

def limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC") -> dict:
    side = _validate_side(side)
    api_logger.info(f"REQUEST  futures_create_order | symbol={symbol} side={side} type=LIMIT quantity={quantity} price={price}")
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=str(price),
            timeInForce=time_in_force,
        )
        api_logger.info(f"RESPONSE  futures_create_order | orderId={order['orderId']} status={order['status']} price={order['price']} origQty={order['origQty']}")
        logger.success(f"Limit order placed successfully: {side} {quantity} {symbol.upper()} @ {price}")
        return order
    except BinanceAPIException as e:
        api_logger.error(f"ERROR futures_create_order | code={e.status_code} msg={e.message}")
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        api_logger.error("NETWORK  POST futures/order | request timed out")
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        api_logger.error("NETWORK  POST futures/order | connection lost")
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        api_logger.error(f"NETWORK  POST futures/order | unexpected error: {e}")
        logger.error(f"Network error: {e}")

def stop_limit_order(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float, time_in_force: str = "GTC") -> dict:
    side = _validate_side(side)
    api_logger.info(f"REQUEST  futures_create_order | symbol={symbol} side={side} type=STOP quantity={quantity} stopPrice={stop_price} limitPrice={limit_price}")
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
        api_logger.info(f"RESPONSE futures_create_order | algoId={order.get('algoId')} algoStatus={order.get('algoStatus')} triggerPrice={order.get('triggerPrice')} price={order.get('price')}")
        logger.success(f"Stop-limit order placed successfully: {side} {quantity} {symbol.upper()} stop {stop_price} limit {limit_price}")
        return order
    except BinanceAPIException as e:
        api_logger.error(f"ERROR    POST futures/order | code={e.status_code} msg={e.message}")
        logger.error(f"Binance rejected the order: {e.message}")
    except Timeout:
        api_logger.error("NETWORK  POST futures/order | request timed out")
        logger.error("Request timed out — check your connection and try again")
    except ConnectionError:
        api_logger.error("NETWORK  POST futures/order | connection lost")
        logger.error("Could not reach Binance — check your internet connection")
    except RequestException as e:
        api_logger.error(f"NETWORK  POST futures/order | unexpected error: {e}")
        logger.error(f"Network error: {e}")
