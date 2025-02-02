# eth_trading_bot
# 🚀 Ethereum Trading Bot

## Overview
This is a Telegram-based Ethereum trading bot that allows users to:
✅ Check wallet balances
✅ Buy/sell tokens on Uniswap
✅ Withdraw ETH to an external address
✅ Monitor price movements

---

## Installation

### 1. Install Dependencies
Run the following command to install required Python libraries:
pip install python-telegram-bot web3 requests python-dotenv

### 2. Set Up Environment Variables
Create a .env file in the project directory and add:
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
ETH_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=your-private-key
WALLET_ADDRESS=your-wallet-address
WITHDRAW_ADDRESS=your-withdrawal-wallet-address

### 3. Run the Bot
Start the bot by running:
python bot.py

---

## Usage
Once the bot is running, use the following Telegram commands:

| Command | Description |
|---------|-------------|
| /start | Start the bot |
| /help | Show available commands |
| /balance | Check ETH balance |
| /buy <token_address> <amount> | Buy a token on Uniswap |
| /sell <token_address> <amount> | Sell a token on Uniswap |
| /withdraw <amount> | Withdraw ETH to the set wallet |

### Example Commands
- /buy 0xdAC17F958D2ee523a2206206994597C13D831ec7 0.1 (Buy 0.1 ETH worth of USDT)
- /sell 0xdAC17F958D2ee523a2206206994597C13D831ec7 50 (Sell 50 USDT)
- /withdraw 0.05 (Withdraw 0.05 ETH to your withdrawal address)

---

## Support
If you encounter any issues, feel free to reach out:
📢 Join our Telegram Group: [Tradenly Telegram](https://t.me/tradenly)
📧 Email us: support@tradenly.xyz

---

### Security Notice
🔴 Never share your private key! Always store it securely in the .env file and never expose it publicly.

---

## License
This project is open-source and available under the MIT License.
