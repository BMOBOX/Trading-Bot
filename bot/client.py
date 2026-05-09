from binance.client import Client
from binance.exceptions import BinanceAPIException
from utils import logger
import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_SECRET_KEY")

if not api_key or not api_secret:
    logger.error("Binance API credentials missing. Check your .env file.")
    sys.exit(1)

def BinanceConnect() -> Client:
    """
    Establishes an authenticated sync connection to the Binance Testnet API.

    Returns:
        Client: An authenticated Binance async client instance ready to use
                     for making API calls (orders, balances, etc.)

    Raises:
        BinanceAPIException: If authentication fails due to invalid or missing keys,
                             or insufficient API permissions.
        Exception: For any other unexpected errors during client initialization.

    """

    client = None
    try:
        client = Client(
            api_key,
            api_secret,
            testnet=True 
        ) 
        logger.info("Binance service connected")
        return client

    except BinanceAPIException as e:
        logger.error(f"Binance API error (check key permissions or testnet keys): {e}")
        raise

    except Exception as e:
        logger.exception(f"Failed to initialize Binance client: {e}")
        raise
