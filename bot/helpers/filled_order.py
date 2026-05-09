import time
from utils.logger import logger
from bot.client import BinanceConnect

client = BinanceConnect()

def get_filled_order(symbol: str, order_id: int, retries: int = 5, delay: float = 0.5) -> dict:
    """
    Polls Binance until order is FILLED or retries exhausted.
    Used after market orders which fill near-instantly.
    """
    for attempt in range(retries):
        order = client.futures_get_order(symbol=symbol.upper(), orderId=order_id)
        if order["status"] == "FILLED":
            logger.info(f"Order {order_id} filled after {attempt + 1} poll(s)")
            return order
        time.sleep(delay)

    logger.warning(f"Order {order_id} not filled after {retries} attempts, returning last known state")
    return order
