import requests
import os
from dotenv import load_dotenv
from acc_list import main_wallets, WALLET_GROUP_1, WALLET_GROUP_2, WALLET_GROUP_3
import json

load_dotenv(override=True)

API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL_1 = "http://113.30.188.29:8001"  # for port 8001
WEBHOOK_URL_2 = "http://113.30.188.29:8002"  # for port 8002
WEBHOOK_URL_3 = "http://113.30.188.29:8003"  # for port 8003


def register_webhooks(accounts, webhook_url):
    print(f"\nRegistering new webhook for URL: {webhook_url}")
    print(f"Number of accounts in this group: {len(accounts)}")

    # Create webhook
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    payload = {
        "webhookURL": webhook_url,
        "transactionTypes": ["TRANSFER"],
        "accountAddresses": accounts,
        "webhookType": "enhanced",
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Successfully registered webhook")
        return True, response.json()
    else:
        print(f"Failed to register webhook: {response.text}")
        return False, response.text


if __name__ == "__main__":
    print("Starting webhook registration...")
    print(
        f"Using API key: {API_KEY[:4]}...{API_KEY[-4:]}"
    )  # Show first/last 4 chars of API key
    print(f"Webhook URL 1: {WEBHOOK_URL_1}")
    print(f"Webhook URL 2: {WEBHOOK_URL_2}")
    print(f"Webhook URL 3: {WEBHOOK_URL_3}")
    print(f"Monitoring wallets: {len(main_wallets)}")

    # Register webhooks for each group
    print("\nRegistering Group 1...")
    status1, response1 = register_webhooks(WALLET_GROUP_1, WEBHOOK_URL_1)

    print("\nRegistering Group 2...")
    status2, response2 = register_webhooks(WALLET_GROUP_2, WEBHOOK_URL_2)

    print("\nRegistering Group 3...")
    status3, response3 = register_webhooks(WALLET_GROUP_3, WEBHOOK_URL_3)

    # Check overall status
    if status1 and status2 and status3:
        print("\nAll webhook registrations successful!")
    else:
        print("\nSome webhook registrations failed!")
