from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from utils.logger import logger
from bot.helpers.filled_order import get_filled_order, get_filled_algo_order

console = Console()

def order_printer(response: dict, side: str, symbol: str):
    side_color = "green" if side == "BUY" else "red"

    # handle both regular and algo (stop-limit) response shapes
    is_algo = "algoId" in response
    status = response.get("algoStatus" if is_algo else "status", "")
    order_type = response.get("orderType" if is_algo else "type", "")
    order_id = response.get("algoId" if is_algo else "orderId", "N/A")

    content = Text()
    content.append(f"{side} ", style=f"bold {side_color}")
    content.append(f"{symbol} · ", style="bold white")
    content.append(f"{status}\n", style="bold cyan")
    content.append(f"order id · {order_id}\n\n")

    fields = [
        ("executed qty ", response.get("executedQty", "0")),
        ("orig qty     ", response.get("quantity" if is_algo else "origQty", "0")),
        ("avg price    ", response.get("avgPrice", "0")),
        ("price        ", response.get("price", "0")),
        ("stop price   ", response.get("triggerPrice" if is_algo else "stopPrice", "0")),
        ("time in force", response.get("timeInForce", "-")),
        ("client id    ", response.get("clientAlgoId" if is_algo else "clientOrderId", "-")),
    ]

    for label, value in fields:
        if value in ("0.00", "0.0000", "0", None):
            continue
        content.append(f"  {label}  ", style="dim")
        content.append(f"{value}\n", style="white")

    console.print(Panel(content, border_style="dim", padding=(0, 1)))

    if status == "NEW" and order_type in ("LIMIT", "STOP"):
        console.print("  [dim]avg price and executed qty will appear once the order fills[/dim]\n")
    elif status == "FILLED":
        console.print("  [dim]order fully executed[/dim]\n")
    elif status == "PARTIALLY_FILLED":
        console.print("  [dim]order partially filled — remainder still open[/dim]\n")

def print_order_response(response: dict, side: str, symbol: str):
    if response is None:
        return

    order_printer(response, side, symbol)

    is_algo = "algoId" in response

    if is_algo:
        refreshed = get_filled_algo_order(symbol, response["algoId"])
    else:
        refreshed = get_filled_order(symbol, response["orderId"])
    
    order_printer(refreshed, side, symbol)



