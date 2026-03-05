from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_range_easy():
    # Easy mode should give range 1-20, not 1-100
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_hard():
    # Hard mode should give range 1-50
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- Edge Case Tests ---

def test_parse_negative_number():
    # Edge case: negative numbers parse successfully but are out of game range
    ok, value, err = parse_guess("-5")
    assert ok == True
    assert value == -5
    assert err is None

def test_parse_decimal_truncates():
    # Edge case: decimals like "3.7" should be accepted and truncated to 3
    ok, value, err = parse_guess("3.7")
    assert ok == True
    assert value == 3
    assert err is None

def test_parse_non_numeric_string():
    # Edge case: letters should return an error, not crash the app
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert value is None
    assert err == "That is not a number."
