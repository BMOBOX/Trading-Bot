from binance import AsyncClient
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

async def BinanceConnect() -> AsyncClient:
    """
    Establishes an authenticated async connection to the Binance Testnet API.

    Returns:
        AsyncClient: An authenticated Binance async client instance ready to use
                     for making API calls (orders, balances, streams, etc.)

    Raises:
        BinanceAPIException: If authentication fails due to invalid or missing keys,
                             or insufficient API permissions.
        Exception: For any other unexpected errors during client initialization.

    """

    client = None
    try:
        client = await AsyncClient.create(
            api_key,
            api_secret,
            testnet=True  #  Needs keys from testnet.binance.vision
        )
        logger.info("Binance service connected")
        return client

    except BinanceAPIException as e:
        #  Catches invalid key / permission errors specifically
        logger.error(f"Binance API error (check key permissions or testnet keys): {e}")
        if client:
            await client.close_connection()  # Clean up dangling connection
        raise

    except Exception as e:
        logger.exception(f"Failed to initialize Binance client: {e}")
        if client:
            await client.close_connection()
        raise
