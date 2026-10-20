"""Tests for tier thresholds and signal decay."""
import pytest

from decay import WORKED_EXAMPLE, Account, decay_factor, rescore, retier_accounts, tier


def test_decay_factor_is_one_on_day_zero():
    assert decay_factor(0) == 1.0


def test_decay_factor_is_half_at_day_30():
    assert decay_factor(30) == 0.5


def test_decay_factor_is_zero_at_day_60():
    assert decay_factor(60) == 0.0


def test_decay_factor_never_negative_past_the_window():
    assert decay_factor(90) == 0.0
    assert decay_factor(365) == 0.0


def test_shorter_30_day_window_fades_twice_as_fast():
    assert decay_factor(15, window=30) == 0.5


def test_zero_day_window_is_rejected():
    with pytest.raises(ValueError):
        decay_factor(10, window=0)


def test_score_of_70_is_hot():
    assert tier(70) == "Hot"


def test_score_of_69_9_is_warm():
    assert tier(69.9) == "Warm"


def test_score_of_40_is_warm():
    assert tier(40) == "Warm"


def test_score_of_39_9_is_cold():
    assert tier(39.9) == "Cold"


def test_fit_points_never_change_with_age():
    for days in (0, 30, 60, 200):
        assert rescore(55, 0, days) == 55


def test_fit_points_carry_through_the_table_unchanged():
    rows = retier_accounts(WORKED_EXAMPLE)
    assert [row["fit_points"] for row in rows] == [40, 20, 45]


def test_worked_example_new_scores_after_30_days():
    rows = retier_accounts(WORKED_EXAMPLE)
    assert [row["new_score"] for row in rows] == pytest.approx([62.5, 45, 50])


def test_worked_example_old_tiers_before_decay():
    rows = retier_accounts(WORKED_EXAMPLE)
    assert [row["old_tier"] for row in rows] == ["Hot", "Hot", "Warm"]


def test_worked_example_retiers_to_warm_warm_warm():
    rows = retier_accounts(WORKED_EXAMPLE)
    assert [row["new_tier"] for row in rows] == ["Warm", "Warm", "Warm"]


def test_activity_driven_accounts_lose_more_than_strong_fit_account():
    rows = {row["name"]: row for row in retier_accounts(WORKED_EXAMPLE)}
    drop = {name: row["old_score"] - row["new_score"] for name, row in rows.items()}
    assert drop["Account A"] > drop["Account C"]
    assert drop["Account B"] > drop["Account C"]


def test_quiet_account_past_window_falls_back_to_fit_only():
    quiet = Account("Quiet", fit_points=30, event_points=50, days_since_last_seen=75)
    row = retier_accounts([quiet])[0]
    assert row["old_tier"] == "Hot"
    assert row["new_score"] == 30
    assert row["new_tier"] == "Cold"
