def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive range for random number generation.
        Defaults to (1, 100) for unrecognized difficulty values.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts whole numbers and decimals (decimals are truncated to int).
    Rejects empty input, None, and non-numeric strings.

    Args:
        raw: The raw string input from the user.

    Returns:
        A tuple of (ok, value, error_message):
            - ok (bool): True if parsing succeeded.
            - value (int | None): The parsed integer, or None on failure.
            - error_message (str | None): A human-readable error, or None on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare a player's guess to the secret number and return the outcome.

    Args:
        guess: The player's guessed integer.
        secret: The secret integer to guess.

    Returns:
        "Win" if guess equals secret, "Too High" if guess exceeds secret,
        or "Too Low" if guess is below secret.

    Note:
        FIX — Refactored from app.py into logic_utils.py using Claude Code.
        Always compares as integers. The original code converted secret to a string
        on even-numbered attempts, causing backwards hints due to lexicographic comparison.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the guess outcome.

    Winning awards points scaled by how early the player guessed (min 10 points).
    Wrong guesses deduct 5 points.

    Args:
        current_score: The player's score before this guess.
        outcome: One of "Win", "Too High", or "Too Low".
        attempt_number: The 1-based attempt number for this guess.

    Returns:
        The updated integer score.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(100, "Too Low", 3)
        95
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number + 1))
        return current_score + points
    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5
    return current_score
