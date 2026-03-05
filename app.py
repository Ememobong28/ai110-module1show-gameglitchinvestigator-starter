import random
import json
import os
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# Challenge 2: High score persistence — Claude Code added file-based high score tracking
HIGHSCORE_FILE = "highscore.json"

def load_high_score() -> int:
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE) as f:
            return json.load(f).get("high_score", 0)
    return 0

def save_high_score(score: int):
    current = load_high_score()
    if score > current:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)

OUTCOME_MESSAGES = {
    "Win": "🎉 CORRECT! You cracked the code!",
    "Too High": "🔴 Go LOWER!",
    "Too Low": "🟢 Go HIGHER!",
}

# Challenge 4: Neon Arcade UI — Claude Code redesigned the theme to match the game aesthetic
st.set_page_config(page_title="Game Glitch Investigator 🎮", page_icon="🎮")

st.markdown("""
<style>
    .stApp { background-color: #0d1b2a; color: #e8f0f7; }

    [data-testid="stSidebar"] {
        background-color: #112236;
        border-right: 1px solid #1e3a5f;
    }

    h1, h2, h3 { color: #f4c542; font-weight: 700; }

    .stButton>button {
        background-color: #f4c542;
        color: #0d1b2a;
        border: none;
        border-radius: 6px;
        font-weight: 700;
        padding: 0.4rem 1.2rem;
    }
    .stButton>button:hover {
        background-color: #e0b030;
        color: #0d1b2a;
    }

    .stTextInput>div>input {
        background-color: #112236;
        color: #e8f0f7;
        border: 1px solid #1e3a5f;
        border-radius: 6px;
    }

    .stCaption { color: #7a9bbf; }
    [data-testid="stMetricValue"] { color: #f4c542; font-weight: bold; }
    [data-testid="stProgress"] > div { background-color: #f4c542 !important; }
    .stSelectbox label, .stCheckbox label { color: #e8f0f7; }
</style>
""", unsafe_allow_html=True)

st.title("🎮 Game Glitch Investigator")
st.caption("Debugged, refactored, and ready to play.")

st.sidebar.header("🕹️ Settings")

# Challenge 2: High score display in sidebar
high_score = load_high_score()
st.sidebar.metric("🏆 High Score", high_score)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: When difficulty changes, reset the whole game so the secret matches the new range.
# Claude Code identified that the old secret stayed in session_state when difficulty was switched.
if "secret" not in st.session_state or st.session_state.get("last_difficulty") != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_difficulty = difficulty

st.subheader("Make a guess")

# FIX: Hint text now uses low/high variables instead of hardcoded "1 and 100". Claude Code identified the mismatch
# between the computed range and the static string. Verified by switching to Easy mode and confirming hint updated.

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# FIX: Removed debug expander that exposed the secret number. Claude Code flagged it as leftover debug code that
# should never ship. Verified by reloading the app and confirming the dropdown no longer appears.

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game now resets all session state — attempts, secret (using correct difficulty range), score, status,
# and history. Claude Code identified the original reset was missing score/status/history and used hardcoded 1-100.
# Verified by playing a partial game, clicking New Game, and confirming score and history cleared.
if new_game:
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(OUTCOME_MESSAGES[outcome])

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            save_high_score(st.session_state.score)  # Challenge 2: persist high score
            st.success(
                f"🎮 You cracked the code! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Challenge 2: Guess history sidebar — visualizes how close each guess was
if st.session_state.history:
    st.sidebar.divider()
    st.sidebar.subheader("🕹️ Guess History")
    secret = st.session_state.secret
    game_range = high - low
    for i, guess in enumerate(st.session_state.history):
        if isinstance(guess, int):
            distance = abs(guess - secret)
            closeness = max(0, 1 - distance / game_range)
            if guess == secret:
                icon = "🎯"
            elif closeness > 0.8:
                icon = "🔥"
            elif closeness > 0.5:
                icon = "🌡️"
            elif closeness > 0.2:
                icon = "🔵"
            else:
                icon = "❄️"
            st.sidebar.write(f"{icon} Guess {i+1}: **{guess}**")
            st.sidebar.progress(closeness)
        else:
            st.sidebar.write(f"⚠️ Guess {i+1}: `{guess}` (invalid)")

st.divider()
st.caption("Built by an AI that claims this code is production-ready. 🎮")
