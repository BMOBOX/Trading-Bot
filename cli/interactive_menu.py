import questionary
from cli.commands.buy import buy
from cli.commands.sell import sell


def interactive_menu():

    action = questionary.select(
        "Action:",
        choices=["Buy", "Sell"]
    ).ask()

    ticker = questionary.text(
        "Ticker:",
        validate = 
    ).ask()

    amount = float(
        questionary.text(
            "Amount:"
        ).ask()
    )

    actions = {
        "Buy": buy,
        "Sell": sell,
    }

    actions[action](ticker, amount)
