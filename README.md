# Trading Bot CLI

A Python CLI for placing Binance **USDT-M Futures** orders on Testnet.

https://github.com/user-attachments/assets/7f761112-4956-44ec-872a-d459eaf71994

It supports:
- `BUY` / `SELL`
- order types: `market`, `limit`, `stop-limit`
- interactive mode and direct CLI commands
- has validation, formatted output, and API/network logging

## Requirements

- Python `3.13+`
- Binance Testnet API credentials

## Installation
### Clone the repo

```bash
git clone https://github.com/BMOBOX/Trading-Bot.git && cd Trading-Bot
```

### Option 1 (recommended): `uv`

```bash
# from project root
uv sync
```

### Option 2: `pip` + virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Setup

1. Copy environment template:

```bash
cp .env.example .env
```

2. Edit `.env` with your Binance Testnet keys:

```env
BINANCE_API_KEY=<your-api-key>
BINANCE_SECRET_KEY=<your-secret-key>
```

3. Make sure keys are enabled for Futures trading on testnet.

## How to Run

### Interactive mode

```bash
uv run main.py
```

```bash
python main.py
```

You will be prompted for:
- action (`Buy` or `Sell`)
- ticker (must end with `USDT`, e.g. `BTCUSDT`)
- quantity
- order type
- optional limit/stop values depending on order type

### Direct CLI commands

```bash
uv run main.py buy BTCUSDT 0.01 --order-type market
uv run main.py sell BTCUSDT 0.01 --order-type market

uv run main.py buy BTCUSDT 0.01 --order-type limit --price 64000
uv run main.py sell BTCUSDT 0.01 --order-type limit --price 67000

uv run main.py buy BTCUSDT 0.01 --order-type stop-limit --price 64500 --stop-price 65000
uv run main.py sell BTCUSDT 0.01 --order-type stop-limit --price 65500 --stop-price 65000
```

```bash
python main.py buy BTCUSDT 0.01 --order-type market
python main.py sell BTCUSDT 0.01 --order-type market

python main.py buy BTCUSDT 0.01 --order-type limit --price 64000
python main.py sell BTCUSDT 0.01 --order-type limit --price 67000

python main.py buy BTCUSDT 0.01 --order-type stop-limit --price 64500 --stop-price 65000
python main.py sell BTCUSDT 0.01 --order-type stop-limit --price 65500 --stop-price 65000
```

## Output and Logs

- order responses are printed with rich formatting in terminal
- API activity is logged to `logs/`

## Log Samples
- [BUY Market order log](logs/2026-05-09_18-31-15.log)
- [SELL Limit order log](logs/2026-05-09_18-39-26.log)

## Assumptions

- Symbols must be **USDT-M futures symbols** (for example: `BTCUSDT`, `ETHUSDT`).
- Quantity/price inputs must be positive numbers.
- For `limit` orders, `--price` is required.
- For `stop-limit` orders, both `--price` and `--stop-price` are required.

