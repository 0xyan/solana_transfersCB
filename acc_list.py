import pandas as pd

MAIN_WALLETS = [
    "AeBwztwXScyNNuQCEdhS54wttRQrw3Nj1UtqddzB4C7b",  # Solana dep wallet + USDC from Circle treasury
    "8Tp9fFkZ2KcRBLYDTUNXo98Ez6ojGb6MZEPXfGDdeBzG",  # Cold (only interacts with MM receiver)
    "6brjeZNfSpqjWoo16z1YbywKguAruXZhNz9bJMVZE8pD",  # MM receiver
    "CdkLi5GK8kGTNmHCTe1dem2dXxgU2V2Yxh5s4xPuk9UY",  # USDC hot wallet
]

TRACKED_TOKENS = {
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "BONK",
    "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm": "WIF",
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": "JUP",
    # "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC", #for testing
}


def load_all_wallets(csv_path="deposit_wallets.csv"):
    try:
        # Load deposit wallets from CSV
        df = pd.read_csv(csv_path)
        wallet_column = df.columns[0]
        deposit_wallets = df[wallet_column].unique().tolist()

        # Combine with main wallets and remove any duplicates
        all_wallets = list(set(MAIN_WALLETS + deposit_wallets))

        print(f"Loaded unique wallets: {len(all_wallets)}")

        return all_wallets
    except Exception as e:
        print(f"Error loading wallets: {e}")
        return MAIN_WALLETS  # Fallback to main wallets if CSV loading fails


# Load combined wallet list
main_wallets = load_all_wallets()
