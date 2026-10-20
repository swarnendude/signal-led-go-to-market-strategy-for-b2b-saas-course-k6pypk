# Build an account score

This sample is the spreadsheet account score from the lesson, written as a small Python function. It weights fit, intent and negative signals into one 0 to 100 number per account, then ranks the accounts.

## How it ties to the lesson

| Lesson step | In the code |
|---|---|
| Rate every signal on the same 0 to 3 scale | `check_ratings` raises a `ValueError` if a rating is outside 0 to 3 or a signal is unrated |
| Set weights from lift; negatives subtract | `TALLYO_WEIGHTS` in `tallyo.py`: fit 4, product usage 5, pricing visits 3, negative -4 |
| `=SUMPRODUCT(ratings, weights)` | `weighted_total` |
| Divide by 3 times the sum of positive weights | `max_positive_total` (36 for Tallyo) |
| `MAX(0, ...) * 100`, then round | `score_account` |
| Sort by score to get your ranking | `rank_accounts` (ties keep their input order) |

The score works on a whole company, not one person, so each `Account` holds one rating per signal for the organization.

With the five Tallyo accounts from the worked example, the ranking is **B 78, A 69, C 69, D 47, E 14**. B ranks first despite a negative signal because its intent is strong everywhere. A and C tie: A fits well, while C is busy but a weak fit. E fits perfectly, but its negative signal sinks it to last.

Rounding works like a spreadsheet's ROUND, so a half rounds up.

## How to run it

```
pip install pytest
pytest -q
```

To print the Tallyo ranking, run `python tallyo.py`.

## What the tests check

- `test_tallyo_accounts_rank_b_a_c_d_e_with_lesson_scores`: the five Tallyo accounts give B 78, A 69, C 69, D 47, E 14, in that order.
- `test_tallyo_raw_totals_match_sumproduct_step`: the totals before scaling are A 25, B 28, C 25, D 17, E 5, and the maximum is 36.
- `test_perfect_account_scores_100`: an account rated 3 on every positive signal and 0 on the negative one scores 100.
- `test_heavy_negatives_never_go_below_zero`: strong negatives stop at 0 and never go below it.
- `test_rating_above_three_raises_error` and `test_rating_below_zero_raises_error`: ratings outside 0 to 3 are rejected.
- `test_missing_rating_raises_error`: every signal must be rated.
- `test_higher_fit_account_scores_higher`: this shows the idea of the score. A better ICP fit raises the score.
- `test_negative_signal_pulls_score_down`: a negative weight lowers the score instead of being ignored.