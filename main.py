import asyncio
from utils import logger
from bot.client import BinanceConnect

async def main():
    client = await BinanceConnect()
    try:

        order = await client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.001,
        )

        print(order)

    except Exception as e:
        logger.exception(
            f"Order failed: {e}"
        )

    await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
