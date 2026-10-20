"""Build an account score.

Each account gets a 0 to 3 rating per signal. Each rating is multiplied by
the signal's weight and the results are added up (like SUMPRODUCT in a
spreadsheet). The total is divided by the highest possible positive total
(3 times the sum of positive weights), multiplied by 100, floored at 0 with
MAX(0, ...) and rounded.
"""

import math
from dataclasses import dataclass

MIN_RATING = 0  # 0 = signal absent
MAX_RATING = 3  # 3 = signal strong


@dataclass(frozen=True)
class Account:
    """One company (not one person) with a 0 to 3 rating per signal."""

    name: str
    ratings: dict[str, int]


def check_ratings(account: Account, weights: dict[str, int]) -> None:
    """Raise ValueError if a signal is unrated or a rating is outside 0 to 3."""
    for signal in weights:
        if signal not in account.ratings:
            raise ValueError(f"{account.name}: no rating for signal '{signal}'")
        rating = account.ratings[signal]
        if not isinstance(rating, int) or not MIN_RATING <= rating <= MAX_RATING:
            raise ValueError(
                f"{account.name}: rating {rating!r} for '{signal}' is not 0 to 3"
            )


def weighted_total(ratings: dict[str, int], weights: dict[str, int]) -> int:
    """Multiply each rating by its weight and add them up (SUMPRODUCT)."""
    return sum(ratings[signal] * weight for signal, weight in weights.items())


def max_positive_total(weights: dict[str, int]) -> int:
    """Return the highest possible total: 3 times the sum of positive weights."""
    positive_sum = sum(weight for weight in weights.values() if weight > 0)
    if positive_sum == 0:
        raise ValueError("at least one signal needs a positive weight")
    return MAX_RATING * positive_sum


def round_half_up(value: float) -> int:
    """Round like a spreadsheet ROUND, where 0.5 goes up."""
    return math.floor(value + 0.5)


def score_account(account: Account, weights: dict[str, int]) -> int:
    """Score one account from 0 to 100: MAX(0, total / max * 100), rounded."""
    check_ratings(account, weights)
    total = weighted_total(account.ratings, weights)
    scaled = total / max_positive_total(weights) * 100
    return round_half_up(max(0.0, scaled))


def rank_accounts(
    accounts: list[Account], weights: dict[str, int]
) -> list[tuple[str, int]]:
    """Score every account and sort from highest to lowest score.

    Ties keep their input order, so the ranking is always the same.
    """
    scored = [(account.name, score_account(account, weights)) for account in accounts]
    return sorted(scored, key=lambda pair: pair[1], reverse=True)
