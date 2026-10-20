"""The five Tallyo accounts from the lesson's worked example (made-up data)."""

from scoring import Account, rank_accounts

# Weights are set from lift. The negative signal gets a negative weight
# so it pulls the score down. Maximum = 3 * (4 + 5 + 3) = 36.
TALLYO_WEIGHTS: dict[str, int] = {
    "fit": 4,
    "product_usage": 5,
    "pricing_visits": 3,
    "negative": -4,
}


def make_account(name: str, fit: int, usage: int, pricing: int, negative: int) -> Account:
    """Build one Tallyo account from its four 0 to 3 ratings."""
    return Account(
        name=name,
        ratings={
            "fit": fit,
            "product_usage": usage,
            "pricing_visits": pricing,
            "negative": negative,
        },
    )


# Step 1 of the worked example: rate each account 0 to 3.
TALLYO_ACCOUNTS: list[Account] = [
    make_account("A", fit=3, usage=2, pricing=1, negative=0),
    make_account("B", fit=3, usage=3, pricing=3, negative=2),
    make_account("C", fit=1, usage=3, pricing=2, negative=0),
    make_account("D", fit=2, usage=0, pricing=3, negative=0),
    make_account("E", fit=3, usage=1, pricing=0, negative=3),
]


if __name__ == "__main__":
    for name, score in rank_accounts(TALLYO_ACCOUNTS, TALLYO_WEIGHTS):
        print(f"{name}: {score}")
