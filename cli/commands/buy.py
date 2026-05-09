from typing import Optional

from bot.orders import limit_order, market_order, stop_limit_order
from bot.helpers.symbols import ensure_symbol_exists, normalize_symbol
from utils.formatter import print_order_response
from utils.validators import (
    normalize_order_type,
    parse_positive_float,
)


def buy(
    ticker: str,
    amount: float,
    order_type: str = "market",
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
):
    symbol = ensure_symbol_exists(normalize_symbol(ticker))
    quantity = parse_positive_float(amount, "amount")
    normalized_order_type = normalize_order_type(order_type)

    parsed_price = parse_positive_float(price, "price") if price is not None else None
    parsed_stop_price = (
        parse_positive_float(stop_price, "stop_price")
        if stop_price is not None
        else None
    )

    if normalized_order_type == "market":
        response = market_order(symbol=symbol, side="BUY", quantity=quantity)

    elif normalized_order_type == "limit":
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
    
    print_order_response(response, side="BUY", symbol=symbol)
   
    return response
