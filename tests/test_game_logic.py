from logic_utils import check_guess, get_range_for_difficulty, parse_guess


# --- Basic contract ---

def test_winning_guess():
    assert check_guess(50, 50) == "Win"

def test_guess_too_high():
    assert check_guess(60, 50) == "Too High"

def test_guess_too_low():
    assert check_guess(40, 50) == "Too Low"


# --- Regression: hints were backwards ---

def test_hint_direction_at_extremes():
    assert check_guess(1, 100) == "Too Low"
    assert check_guess(100, 1) == "Too High"


# --- Regression: non-numeric input ---

def test_non_numeric_input_is_rejected():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_empty_input_is_rejected():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_valid_number_is_parsed():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


# --- Regression: difficulty ranges ---

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
