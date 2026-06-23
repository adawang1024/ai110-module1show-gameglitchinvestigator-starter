"""Regression tests for the bugs documented in reflection.md.

These lock in the fixes so the bugs cannot quietly come back.
"""

from logic_utils import check_guess, get_range_for_difficulty, parse_guess


# --- Bug: hints were backwards (guess too high told you to "go higher") ---

def test_high_guess_is_too_high_not_flipped():
    # 60 > 50, so the outcome must be "Too High" (hint should say go LOWER)
    assert check_guess(60, 50) == "Too High"


def test_low_guess_is_too_low_not_flipped():
    # 40 < 50, so the outcome must be "Too Low" (hint should say go HIGHER)
    assert check_guess(40, 50) == "Too Low"


def test_hint_direction_at_extremes():
    assert check_guess(1, 100) == "Too Low"
    assert check_guess(100, 1) == "Too High"


# --- Bug: difficulty range should match the selected difficulty ---

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
