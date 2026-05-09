from typing import Optional
from bot.orders import limit_order, market_order, stop_limit_order
from bot.helpers.symbols import ensure_symbol_exists, normalize_symbol
from utils.formatter import print_order_response
from utils.validators import (
    normalize_order_type,
    parse_positive_float,
)
from utils import logger
import typer

def buy(
    ticker: str = typer.Argument(..., help="Trading pair e.g. BTCUSDT"),
    quantity: float = typer.Argument(..., help="Quantity to buy e.g. 0.01"),
    order_type: str = typer.Option("market", help="market | limit | stop-limit"),
    price: Optional[float] = typer.Option(None, help="Limit price (required for limit/stop-limit)"),
    stop_price: Optional[float] = typer.Option(None, help="Stop trigger price (required for stop-limit)"),
):
    try:
        symbol = ensure_symbol_exists(normalize_symbol(ticker))
        quantity = parse_positive_float(quantity, "quantity")
        normalized_order_type = normalize_order_type(order_type)

        parsed_price = parse_positive_float(price, "price") if price is not None else None
        parsed_stop_price = (
            parse_positive_float(stop_price, "stop_price")
            if stop_price is not None
            else None
        )

        if normalized_order_type == "MARKET":
            response = market_order(symbol=symbol, side="BUY", quantity=quantity)

        elif normalized_order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for limit orders")
            limit_price = parse_positive_float(price, "price")
            response = limit_order(
                symbol=symbol,
                side="BUY",
                quantity=quantity,
                price=limit_price,
            )

        else:
            if price is None or stop_price is None:
                raise ValueError("price and stop_price are required for stop-limit orders")
            limit_price = parse_positive_float(price, "price")
            validated_stop_price = parse_positive_float(stop_price, "stop_price")

            response = stop_limit_order(
                symbol=symbol,
                side="BUY",
                quantity=quantity,
                stop_price=validated_stop_price,
                limit_price=limit_price,
            )
        
        if response is None:
            return

        print_order_response(response, side="BUY", symbol=symbol)
    
        return response
    
    except ValueError as e:
        logger.error(str(e))
        raise typer.Exit(1)

    except BinanceAPIException as e:
        api_logger.error(f"ERROR code={e.status_code} msg={e.message}")
        logger.error(f"Binance rejected the order: {e.message}")
        raise typer.Exit(1)

    except Timeout:
        api_logger.error("NETWORK  request timed out on order placement")
        logger.error("Request timed out — check your connection and try again")
        raise typer.Exit(1)

    except ConnectionError:
        api_logger.error("NETWORK  connection error on order placement")
        logger.error("Could not reach Binance — check your internet connection")
        raise typer.Exit(1)

    except RequestException as e:
        api_logger.error(f"NETWORK  unexpected request error: {e}")
        logger.error(f"Network error: {e}")
        raise typer.Exit(1)
