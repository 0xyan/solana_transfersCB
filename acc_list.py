import pandas as pd

TRACKED_TOKENS = {
    "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": "RAY",
    "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3": "PYTH",
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": "JUP",
    "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ": "W",
    "Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs": "GRASS",
    "METAewgxyPbgwsseH8T16a39CQ5VyVxZi9zXiDPY18m": "MPLX",
    "KMNo3nJsBXfcpJTVhZcXLW7RmTwTt4GVFE7suUBo9sS": "KMNO",
    "6CAsXfiCXZfP8APCG6Vma2DFMindopxiqYQN4LSQfhoC": "POKT",
    "CLoUDKc4Ane7HeQcPpE3YHnznRxhMimJ4MyaUqyHFzAu": "CLOUD",
    "ZEUS1aR7aX8DFFJf5QjWj2ftDDdNTroMNGo8YoQm3Gq": "ZEUS",
    "Hax9LTgsQkze1YFychnBLtFH8gYbQKtKfWKKg2SP6gdD": "TAI",
    "DBRiDgJAMsM95moTzJs7M9LnkGErpbv9v6CUR1DXnUu5": "DBR",
    "poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk": "POLIS",
    "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr": "POPCAT",
    "2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump": "PNUT",
    "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump": "GOAT",
    "MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5": "MEW",
    "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ": "BOME",
    "A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump": "FWOG",
    "8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn": "ZEREBRO",
    "GJAFwWjJ3vnTsrQVabjBVK2TYB1YtRCQXRDfDgUnpump": "ACT",
    "ED5nyyWEzpPPiWimP8vYm7sD7TD3LAt3Q3gRTWHzPJBY": "MOODENG",
    "63LfDmNb3MQ8mw9MtZ2To9bEA2M71kZUUGq5tiJxcqj9": "GIGA",
    "Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump": "CHILLGUY",
    "5z3EqYQo9HiCEs3R84RCDMu2n7anpDMxRhdK8PSWmrRC": "PONKE",
    "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump": "FARTCOIN",
    "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC": "AI16Z",
    "7BgBvyjrZX1YKz4oh9mjb8ZScatkkwb8DzFx7LoiVkM3": "SLERF",
    "5mbK36SZ7J19An8jFochhQS4of8g6BwUjbeCSxBSoWdp": "MICHI",
    "5LafQUrVco6o7KMz42eqVEJ9LW31StPyGjeeu5sKoMtA": "MUMU",
    "CBdCxKo9QavR9hfShgpEBG3zekorAeD7W1jfq2o3pump": "LUCE",
    "HhJpBhRRn4g56VsyLuT8DL5Bv31HkXqsrahTTUCZeZg4": "MYRO",
    "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk": "WEN",
    "GJtJuWD9qYcCkrwMBmtY1tpapV1sKfB2zUv9Q4aqpump": "RIF",
    "FQ1tyso61AH1tzodyJfSwmzsD3GToybbRNoZxUBz21p8": "VVAIFU",
    "79yTpy8uwmAkrdgZdq6ZSBTvxKsgPrNqTLvYQBh1pump": "BULLY",
    "H2c31USxu35MDkBrGph8pUDUnmzo2e4Rf4hnvL2Upump": "SHOGGOTH",
    "Bz4MhmVRQENiCou7ZpJ575wpjNFjBjVBSiVhuNg1pump": "PROJECT89",
    "39qibQxVzemuZTEvjSB7NePhw9WyyHdQCqP8xmBMpump": "MEMESAI",
    "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU": "SAMO",
    "DwDtUqBZJtbRpdjsFw3N7YKB5epocSru25BGcVhfcYtg": "WORM",
    "BoAQaykj3LtkM2Brevc7cQcRAzpqcsP47nJ2rkyopump": "FOREST",
    "6d5zHW5B8RkGKd51Lpb9RqFQSqDudr9GJgZ1SgQZpump": "AVB",
    "66gsTs88mXJ5L4AtJnWqFW6H2L5YQDRy4W41y6zbpump": "CENTS",
    "66gsTs88mXJ5L4AtJnWqFW6H2L5YQDRy4W41y6zbpump": "YOUSIM",
}


# Load deposit wallets from CSV
df = pd.read_csv("deposit_wallets.csv")
wallet_column = df.columns[0]
main_wallets = df[wallet_column].unique().tolist()

# Split wallets into groups of 100k
WALLET_GROUP_1 = main_wallets[:100000]
WALLET_GROUP_2 = main_wallets[100000:200000]
WALLET_GROUP_3 = main_wallets[200000:]
