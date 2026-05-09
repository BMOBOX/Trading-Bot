import questionary
from bot.helpers.symbols import validate_symbol_input_api
from cli.commands.buy import buy
from cli.commands.sell import sell
from utils.validators import (
    validate_positive_number_input,
)


def interactive_menu():

    action = questionary.select("Action:", choices=["Buy", "Sell"]).ask()

    ticker = questionary.text(
        "Ticker:",
        validate=validate_symbol_input_api,
    ).ask()

    amount = float(
        questionary.text(
            "Amount:",
            validate=validate_positive_number_input,
        ).ask()
    )

    order_type = questionary.select(
        "Order type:",
        choices=["market", "limit", "stop-limit"],
    ).ask()

    price = None
    stop_price = None

    if order_type in {"limit", "stop-limit"}:
        price = float(
            questionary.text(
                "Limit price:",
                validate=validate_positive_number_input,
            ).ask()
        )

    if order_type == "stop-limit":
        stop_price = float(
            questionary.text(
                "Stop price:",
                validate=validate_positive_number_input,
            ).ask()
        )

    actions = {
        "Buy": buy,
        "Sell": sell,
    }

    actions[action](
        ticker=ticker,
        amount=amount,
        order_type=order_type,
        price=price,
        stop_price=stop_price,
    )
