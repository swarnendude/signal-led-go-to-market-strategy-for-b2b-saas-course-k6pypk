# Set thresholds and signal decay: sample code

This sample turns the lesson's spreadsheet steps into a small Python script. It shows how **tier thresholds** turn a score into a decision, and how **signal decay** makes event points fade when an account goes quiet, so the account can drop to a lower tier.

## How it ties to the lesson

| Lesson step | Spreadsheet | Python (`decay.py`) |
|---|---|---|
| Tier cut-offs (Hot 70+, Warm 40-69, Cold below 40) | `=IF(score>=70,"Hot",IF(score>=40,"Warm","Cold"))` | `tier(score, hot=70, warm=40)` |
| Straight-line decay over a 60-day window | `=MAX(0,1-days/60)` | `decay_factor(days, window=60)` |
| Decay event points only; fit points do not age | `fit + events * factor` | `rescore(fit, event_points, days, window)` |
| Re-tier after decay to see who went quiet | Tier column reads the decayed score | `retier_accounts(accounts)` |

The script uses the lesson's worked example: three made-up accounts, 30 days with no new activity, so the decay factor is 1 - 30/60 = 0.5.

| Account | Fit | Events | Old score | Old tier | New score | New tier |
|---|---|---|---|---|---|---|
| A | 40 | 45 | 85 | Hot | 62.5 | Warm |
| B | 20 | 50 | 70 | Hot | 45 | Warm |
| C | 45 | 10 | 55 | Warm | 50 | Warm |

The accounts that were Hot because of recent activity cool to Warm. The strong-fit account barely moves. A drop in tier is useful information, not a fault in the model.

The cut-offs (70 and 40) and the window (60 days) are starting points. Change them with the `hot`, `warm` and `window` arguments once your back-test shows better values.

## How to run it

```
pip install pytest
python decay.py   # prints the old and new score and tier table
pytest -q         # runs the tests
```

You need Python 3.11 and only the standard library, plus pytest for the tests.

## What the tests check (`test_decay.py`)

- **Decay factor:** 1 at day 0, 0.5 at day 30 and 0 at day 60. It never goes negative past the window (day 90 and day 365). A 30-day window fades twice as fast. A window of zero days is rejected.
- **Thresholds:** 70 is Hot, 69.9 is Warm, 40 is Warm and 39.9 is Cold.
- **Fit points never change:** an account with no event points keeps its fit score at any age, and the table carries fit points through unchanged.
- **Worked example:** the three accounts score 62.5, 45 and 50 after 30 days. They start as Hot, Hot and Warm and re-tier to Warm, Warm and Warm.
- **The idea:** the activity-driven accounts lose far more points than the strong-fit account.