import logging

from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_level=True,
            show_path=False,
        )
    ],
)



logger = logging.getLogger("trading_bot")

