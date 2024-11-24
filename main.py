import requests
import os
from dotenv import load_dotenv
from acc_list import main_wallets, WALLET_GROUP_1, WALLET_GROUP_2, WALLET_GROUP_3
import json

# Force reload environment variables
load_dotenv(override=True)

API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL_1 = "https://your-ngrok-url-1.ngrok-free.app"  # for port 8001
WEBHOOK_URL_2 = "https://your-ngrok-url-2.ngrok-free.app"  # for port 8002
WEBHOOK_URL_3 = "https://your-ngrok-url-3.ngrok-free.app"  # for port 8003


def get_existing_webhooks():
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    response = requests.get(url)
    webhooks = response.json()
    print(f"\nFound {len(webhooks)} existing webhooks")
    return webhooks


def delete_webhook(webhook_id):
    url = f"https://api.helius.xyz/v0/webhooks/{webhook_id}?api-key={API_KEY}"
    response = requests.delete(url)
    print(f"Deleted webhook {webhook_id}: {response.status_code}")


def register_webhooks(accounts, webhook_url):
    # Get existing webhooks
    existing = get_existing_webhooks()

    # Only delete webhooks that match our specific webhook_url
    for webhook in existing:
        if webhook.get("webhookURL") == webhook_url:
            print(
                f"Deleting webhook {webhook['webhookID']} matching URL: {webhook_url}"
            )
            delete_webhook(webhook["webhookID"])

    # Create webhook for this group of accounts
    url = f"https://api.helius.xyz/v0/webhooks?api-key={API_KEY}"
    payload = {
        "webhookURL": webhook_url,
        "transactionTypes": ["TRANSFER"],
        "accountAddresses": accounts,
        "webhookType": "enhanced",
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Successfully registered webhook for {len(accounts)} accounts")
        return True, response.json()
    else:
        print(f"Failed to create webhook: {response.status_code} - {response.text}")
        return False, None


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
