import time
from requests.exceptions import ConnectionError, Timeout, RequestException
from binance.exceptions import BinanceAPIException
from utils.logger import logger, api_logger
from bot.client import BinanceConnect

client = BinanceConnect()

def get_filled_order(symbol: str, order_id: int, retries: int = 5, delay: float = 0.5) -> dict | None:
    """
    Polls Binance until order is FILLED or retries exhausted.
    Used after market orders which fill near-instantly.
    """
    last_known = None

    for attempt in range(retries):
        try:
            order = client.futures_get_order(symbol=symbol.upper(), orderId=order_id)
            last_known = order

            if order["status"] == "FILLED":
                logger.info(f"Order {order_id} filled after {attempt + 1} poll(s)")
                return order

            time.sleep(delay)

        except BinanceAPIException as e:
            api_logger.error(f"ERROR polling order {order_id}: code={e.status_code} msg={e.message}")
            break

        except Timeout:
            api_logger.error(f"NETWORK  timeout polling order {order_id} on attempt {attempt + 1}")
            time.sleep(delay)

        except ConnectionError:
            api_logger.error(f"NETWORK  connection lost polling order {order_id} on attempt {attempt + 1}")
            break

        except RequestException as e:
            api_logger.error(f"NETWORK  unexpected error polling order {order_id}: {e}")
            break

    if last_known:
        logger.warning(f"Order {order_id} not filled after {retries} attempts, returning last known state")
        return last_known

    logger.error(f"Order {order_id} could not be retrieved — all attempts failed")
    return None

def get_filled_algo_order(symbol: str, algo_id: int, retries: int = 5, delay: float = 0.5) -> dict | None:
    """Poll until FILLED or retries exhausted — stop-limit (algo) orders."""
    last_known = None

    for attempt in range(retries):
        try:
            order = client.futures_get_algo_order(algoId=algo_id)
            last_known = order

            if order.get("algoStatus") == "FILLED":
                logger.info(f"Algo order {algo_id} filled after {attempt + 1} poll(s)")
                return order

            time.sleep(delay)

        except BinanceAPIException as e:
            api_logger.error(f"ERROR polling algo order {algo_id}: {e.message}")
            break
        except Timeout:
            api_logger.error(f"NETWORK  timeout polling algo order {algo_id}")
            time.sleep(delay)
        except ConnectionError:
            api_logger.error(f"NETWORK  connection lost polling algo order {algo_id}")
            break
        except RequestException as e:
            api_logger.error(f"NETWORK  error polling algo order {algo_id}: {e}")
            break

    if last_known:
        logger.warning(f"Algo order {algo_id} not filled after {retries} attempts")
        return last_known

    logger.error(f"Algo order {algo_id} could not be retrieved")
    return None
