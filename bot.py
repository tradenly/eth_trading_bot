import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from web3 import Web3

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ETH_RPC_URL = os.getenv("ETH_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")  # Your Ethereum wallet

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
if not w3.isConnected():
    print("Error: Unable to connect to Ethereum network.")
    exit()

# Uniswap Router contract address (v2)
UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
ROUTER_ABI_URL = "https://api.etherscan.io/api?module=contract&action=getabi&address=" + UNISWAP_ROUTER
router_abi = requests.get(ROUTER_ABI_URL).json()["result"]
uniswap = w3.eth.contract(address=UNISWAP_ROUTER, abi=router_abi)

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- Bot Commands ---
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🤖 Welcome to the Crypto Trading Bot! Use /help for commands.")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "/balance - Check ETH & Token balance\n"
        "/buy <token> <amount> - Buy token on Uniswap\n"
        "/sell <token> <amount> - Sell token on Uniswap\n"
        "/withdraw <amount> - Withdraw profits\n"
    )

def get_balance(update: Update, context: CallbackContext) -> None:
    eth_balance = w3.eth.get_balance(WALLET_ADDRESS)
    eth_balance = w3.from_wei(eth_balance, "ether")
    update.message.reply_text(f"💰 ETH Balance: {eth_balance} ETH")

def buy_token(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /buy <token_address> <amount>")
            return
        
        token_address = args[0]
        amount = float(args[1])

        amount_in_wei = w3.to_wei(amount, "ether")
        path = [w3.to_checksum_address(w3.to_eth_address("ETH")), w3.to_checksum_address(token_address)]
        deadline = w3.eth.get_block("latest")["timestamp"] + 60 * 5  # 5 min

        txn = uniswap.functions.swapExactETHForTokens(
            0, path, WALLET_ADDRESS, deadline
        ).build_transaction({
            "from": WALLET_ADDRESS,
            "value": amount_in_wei,
            "gas": 250000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": w3.eth.get_transaction_count(WALLET_ADDRESS),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        update.message.reply_text(f"✅ Bought {amount} ETH worth of tokens! TX: {tx_hash.hex()}")
    
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def sell_token(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /sell <token_address> <amount>")
            return
        
        token_address = args[0]
        amount = float(args[1])

        token_contract = w3.eth.contract(address=token_address, abi=router_abi)
        decimals = token_contract.functions.decimals().call()
        amount_in_wei = int(amount * (10 ** decimals))

        path = [w3.to_checksum_address(token_address), w3.to_checksum_address(w3.to_eth_address("ETH"))]
        deadline = w3.eth.get_block("latest")["timestamp"] + 60 * 5

        txn = uniswap.functions.swapExactTokensForETH(
            amount_in_wei, 0, path, WALLET_ADDRESS, deadline
        ).build_transaction({
            "from": WALLET_ADDRESS,
            "gas": 250000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": w3.eth.get_transaction_count(WALLET_ADDRESS),
        })