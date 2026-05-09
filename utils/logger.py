import logging
from collections.abc import Mapping
from typing import Any
from typing import cast

from rich.logging import RichHandler
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

api_logger = logging.getLogger("binance.api")
api_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(f"logs/{session_id}.log")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))
api_logger.addHandler(file_handler)
api_logger.propagate = False

SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class TradingLogger(logging.Logger):
    def success(self, message: str, *args, **kwargs) -> None:
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, **kwargs)


logging.setLoggerClass(TradingLogger)

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


logger = cast(TradingLogger, logging.getLogger("trading_bot"))


