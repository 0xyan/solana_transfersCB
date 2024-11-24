from fastapi import FastAPI, Request
import logging
from datetime import datetime
import uvicorn
from acc_list import WALLET_GROUP_1, WALLET_GROUP_2, WALLET_GROUP_3, TRACKED_TOKENS
import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv(override=True)


def create_app(wallet_group, group_name):
    app = FastAPI()

    # Configure logging for this instance
    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s",
        handlers=[
            logging.FileHandler(f"token_transfers_{group_name}.log"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(group_name)

    processed_txs = {}

    # Add Telegram sending function
    def send_telegram_message(message):
        token_tg = os.getenv("TELEGRAM_TOKEN")
        id_tg = os.getenv("TELEGRAM_ID")

        url = f"https://api.telegram.org/bot{token_tg}/sendMessage"
        params = {
            "chat_id": id_tg,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

    @app.post("/")
    async def webhook(request: Request):
        try:
            data = await request.json()
            if isinstance(data, list):
                for event in data:
                    await process_event(event, wallet_group)
            else:
                await process_event(data, wallet_group)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def process_event(event, allowed_wallets):
        try:
            if not event.get("tokenTransfers"):
                return

            tx_signature = event.get("signature")
            if tx_signature in processed_txs:
                return

            processed_txs[tx_signature] = datetime.now()

            for transfer in event["tokenTransfers"]:
                token_address = transfer.get("mint")

                if token_address not in TRACKED_TOKENS:
                    continue

                to_address = transfer.get("toUserAccount")

                # Only process incoming transfers to our wallets
                if to_address not in allowed_wallets:
                    continue

                token_name = TRACKED_TOKENS[token_address]
                from_address = transfer.get("fromUserAccount")
                amount = float(transfer.get("tokenAmount", 0))

                transfer_info = (
                    f"\n{'='*50}\n"
                    f"NEW {token_name} INCOMING TRANSFER on ROBINHOOD!\n"
                    f"Amount: {amount:,.6f}\n"
                    f"From: {from_address}\n"
                    f"To: {to_address}\n"
                    f"Transaction: {tx_signature}\n"
                    f"Timestamp: {datetime.now()}\n"
                    f"{'='*50}"
                )

                # Log to console/file
                logger.warning(transfer_info)

                # Telegram notification
                message = (
                    f"🔔 <b>New {token_name} Incoming Transfer</b>\n\n"
                    f"Amount: {amount:,.6f}\n"
                    f"From: <code>{from_address[:8]}...{from_address[-8:]}</code>\n"
                    f"To: <code>{to_address[:8]}...{to_address[-8:]}</code>\n"
                    f"<a href='https://solscan.io/tx/{tx_signature}'>View Transaction</a>"
                )

                logger.debug("Attempting to send Telegram message...")
                send_telegram_message(message)
                logger.debug("Telegram message sent (or attempted)")

        except Exception as e:
            logger.error(f"Error in process_event: {str(e)}", exc_info=True)

    @app.get("/")
    async def health_check():
        return {"status": "healthy", "group": group_name}

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    # Select wallet group based on argument
    wallet_groups = {
        1: (WALLET_GROUP_1, "group1"),
        2: (WALLET_GROUP_2, "group2"),
        3: (WALLET_GROUP_3, "group3"),
    }

    wallets, group_name = wallet_groups[args.group]
    app = create_app(wallets, group_name)

    print(f"Server starting on port {args.port}...")
    print(
        f"Monitoring incoming transfers to wallets: Group {args.group} ({len(wallets)} wallets)"
    )
    print(f"Tracking tokens: {list(TRACKED_TOKENS.values())}")

    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
