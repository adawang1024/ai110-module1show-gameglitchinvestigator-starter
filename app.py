import random
import streamlit as st

# FIX: refactored the core logic into logic_utils.py using AI agent mode so it
# can be unit-tested separately from the Streamlit UI.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# FIX: AI suggested keeping check_guess pure (returns only the outcome) and
# mapping the outcome to display text here in the UI layer.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

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

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: attempts started at 1, which made "Attempts left" off by one. AI flagged
# the counter should start at 0.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: AI helped add a "flash" queue so hint/win/lose messages survive the
# st.rerun() we now call after each guess (see the submit handler below).
if "flash" not in st.session_state:
    st.session_state.flash = []

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    # FIX: AI suggested numbering the history from 1 (enumerate start=1) instead
    # of dumping a raw 0-indexed list.
    st.write("History:")
    if st.session_state.history:
        for i, guess in enumerate(st.session_state.history, start=1):
            st.write(f"{i}. {guess}")
    else:
        st.write("(no guesses yet)")

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

# FIX: New Game used to leave the "Game over" box and stale history. With the AI
# we made it reset history/score/status (and use the difficulty range, not 1-100).
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.flash = [("success", "New game started.")]
    st.rerun()

# Show any messages saved from the previous run (they survive st.rerun()).
for level, text in st.session_state.flash:
    getattr(st, level)(text)
st.session_state.flash = []

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# FIX: history showed the new guess only after another interaction. The AI
# explained Streamlit's top-to-bottom rerun model, so we st.rerun() at the end
# of this block to redraw the panel with the just-added guess.
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.flash.append(("error", err))
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)
        message = HINT_MESSAGES[outcome]

        if show_hint:
            st.session_state.flash.append(("warning", message))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.show_balloons = True
            st.session_state.status = "won"
            st.session_state.flash.append((
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            ))
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.session_state.flash.append((
                    "error",
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}",
                ))

    st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
