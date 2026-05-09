from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from utils.logger import logger
from bot.helpers.filled_order import get_filled_order

console = Console()

def order_printer(response: dict, side: str, symbol: str):
    side_color = "green" if side == "BUY" else "red"
    status = response.get("status", "")
    order_type = response.get("type", "")

    content = Text()
    # header line inside the panel — left aligned
    content.append(f"{side} ", style=f"bold {side_color}")
    content.append(f"{symbol} · ", style="bold white")
    content.append(f"{status}\n", style="bold cyan")

    content.append(f"order id · {response['orderId']}\n\n")

    fields = [
        ("executed qty ", response.get("executedQty", "0")),
        ("orig qty     ", response.get("origQty", "0")),
        ("avg price    ", response.get("avgPrice", "0")),
        ("price        ", response.get("price", "0")),
        ("stop price   ", response.get("stopPrice", "0")),
        ("time in force", response.get("timeInForce", "-")),
        ("client id    ", response.get("clientOrderId", "-")),
    ]
    for label, value in fields:
        if value == "0.00" or value == "0.0000" or value == "0":
            continue  # skip empty/zero fields
        content.append(f"  {label}  ", style="dim")
        content.append(f"{value}\n", style="white")

    console.print(Panel(content, border_style="dim", padding=(0, 1)))
    if status == "NEW" and order_type == "LIMIT":
        console.print("  [dim]avg price and executed qty will appear once the order fills[/dim]\n")
    elif status == "NEW" and order_type == "STOP":
        console.print("  [dim]order will activate when stop price is triggered[/dim]\n")
    elif status == "FILLED":
        console.print("  [dim]order fully executed[/dim]\n")
    elif status == "PARTIALLY_FILLED":
        console.print("  [dim]order partially filled — remainder still open[/dim]\n")


def print_order_response(response: dict, side: str, symbol: str):
    order_printer(response, side, symbol)
    
    refreshed_response = get_filled_order(symbol, response["orderId"])

    order_printer(refreshed_response, side, symbol)



