"""Tests for the weighted account score."""

import pytest

from scoring import (
    Account,
    max_positive_total,
    rank_accounts,
    score_account,
    weighted_total,
)
from tallyo import TALLYO_ACCOUNTS, TALLYO_WEIGHTS, make_account


def test_tallyo_accounts_rank_b_a_c_d_e_with_lesson_scores() -> None:
    ranking = rank_accounts(TALLYO_ACCOUNTS, TALLYO_WEIGHTS)
    assert ranking == [("B", 78), ("A", 69), ("C", 69), ("D", 47), ("E", 14)]


def test_tallyo_raw_totals_match_sumproduct_step() -> None:
    totals = {a.name: weighted_total(a.ratings, TALLYO_WEIGHTS) for a in TALLYO_ACCOUNTS}
    assert totals == {"A": 25, "B": 28, "C": 25, "D": 17, "E": 5}
    assert max_positive_total(TALLYO_WEIGHTS) == 36


def test_perfect_account_scores_100() -> None:
    perfect = make_account("Perfect", fit=3, usage=3, pricing=3, negative=0)
    assert score_account(perfect, TALLYO_WEIGHTS) == 100


def test_heavy_negatives_never_go_below_zero() -> None:
    weights = {"fit": 2, "competitor_contract": -5, "layoffs": -5}
    doomed = Account("Doomed", {"fit": 1, "competitor_contract": 3, "layoffs": 3})
    assert weighted_total(doomed.ratings, weights) < 0
    assert score_account(doomed, weights) == 0


def test_rating_above_three_raises_error() -> None:
    bad = make_account("Bad", fit=4, usage=0, pricing=0, negative=0)
    with pytest.raises(ValueError):
        score_account(bad, TALLYO_WEIGHTS)


def test_rating_below_zero_raises_error() -> None:
    bad = make_account("Bad", fit=1, usage=-1, pricing=0, negative=0)
    with pytest.raises(ValueError):
        score_account(bad, TALLYO_WEIGHTS)


def test_missing_rating_raises_error() -> None:
    unrated = Account("Unrated", {"fit": 2, "product_usage": 1})
    with pytest.raises(ValueError):
        score_account(unrated, TALLYO_WEIGHTS)


def test_higher_fit_account_scores_higher() -> None:
    weak_fit = make_account("Weak fit", fit=1, usage=2, pricing=2, negative=0)
    strong_fit = make_account("Strong fit", fit=3, usage=2, pricing=2, negative=0)
    assert score_account(strong_fit, TALLYO_WEIGHTS) > score_account(
        weak_fit, TALLYO_WEIGHTS
    )


def test_negative_signal_pulls_score_down() -> None:
    clean = make_account("Clean", fit=3, usage=2, pricing=2, negative=0)
    flagged = make_account("Flagged", fit=3, usage=2, pricing=2, negative=2)
    assert score_account(flagged, TALLYO_WEIGHTS) < score_account(
        clean, TALLYO_WEIGHTS
    )
