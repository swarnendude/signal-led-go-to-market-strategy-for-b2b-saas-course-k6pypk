"""Tier thresholds and signal decay, from the lesson 'Set thresholds and signal decay'.

Fit points describe who the company is and never age.
Event points (intent, pricing visits, hiring) fade in a straight line over a
decay window. After decay, each account is re-tiered as Hot, Warm or Cold.
"""
from dataclasses import dataclass

HOT_CUTOFF = 70
WARM_CUTOFF = 40
DECAY_WINDOW_DAYS = 60


@dataclass(frozen=True)
class Account:
    """One account row: fit points, event points and days since last activity."""

    name: str
    fit_points: float
    event_points: float
    days_since_last_seen: int


def decay_factor(days: float, window: float = DECAY_WINDOW_DAYS) -> float:
    """Spreadsheet =MAX(0, 1 - days/window): 1 on day 0, 0 at the window and beyond."""
    if window <= 0:
        raise ValueError("window must be a positive number of days")
    return max(0.0, 1 - days / window)


def rescore(fit: float, event_points: float, days: float,
            window: float = DECAY_WINDOW_DAYS) -> float:
    """Decayed score: fit points stay, event points are multiplied by the decay factor."""
    return fit + event_points * decay_factor(days, window)


def tier(score: float, hot: float = HOT_CUTOFF, warm: float = WARM_CUTOFF) -> str:
    """Spreadsheet =IF(score>=70,'Hot',IF(score>=40,'Warm','Cold'))."""
    if score >= hot:
        return "Hot"
    if score >= warm:
        return "Warm"
    return "Cold"


def retier_accounts(accounts: list[Account],
                    window: float = DECAY_WINDOW_DAYS) -> list[dict[str, object]]:
    """Build the table: old score, new score, old tier and new tier per account."""
    rows: list[dict[str, object]] = []
    for account in accounts:
        old_score = account.fit_points + account.event_points
        new_score = rescore(account.fit_points, account.event_points,
                            account.days_since_last_seen, window)
        rows.append({
            "name": account.name,
            "fit_points": account.fit_points,
            "old_score": old_score,
            "new_score": new_score,
            "old_tier": tier(old_score),
            "new_tier": tier(new_score),
        })
    return rows


def format_table(rows: list[dict[str, object]]) -> str:
    """Lay the rows out as a plain-text table, like the spreadsheet columns."""
    lines = [f"{'Account':<10} {'Old score':>9} {'New score':>9} {'Old tier':>8} {'New tier':>8}"]
    for row in rows:
        lines.append(f"{row['name']:<10} {row['old_score']:>9.1f} {row['new_score']:>9.1f} "
                     f"{row['old_tier']:>8} {row['new_tier']:>8}")
    return "\n".join(lines)


# The lesson's worked example: made-up accounts, 30 days with no new activity.
WORKED_EXAMPLE = [
    Account("Account A", fit_points=40, event_points=45, days_since_last_seen=30),
    Account("Account B", fit_points=20, event_points=50, days_since_last_seen=30),
    Account("Account C", fit_points=45, event_points=10, days_since_last_seen=30),
]


if __name__ == "__main__":
    print(format_table(retier_accounts(WORKED_EXAMPLE)))
