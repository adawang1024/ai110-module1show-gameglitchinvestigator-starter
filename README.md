# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User opens the app on Normal difficulty (range 1–100, 8 attempts allowed). A
  new secret number is picked.
2. User guesses **40** → hint shows "📈 Go HIGHER!" and History immediately
  updates to show "1. 40".
3. User guesses **70** → hint shows "📉 Go LOWER!" and History updates to "1. 40
   2. 70". Score adjusts after each guess.
4. User guesses **55** → hint shows "📈 Go HIGHER!". Attempts left counts down
  correctly with each submission.
5. User guesses **62** → 🎉 Correct! Balloons appear, score is displayed, and
  the game sets status to "won".
6. User clicks "New Game 🔁" → board fully resets: History clears, attempts
  return to 8, and a fresh secret is picked.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->
 ![Game screenshot](screenshot.png)

## 🧪 Test Results

```
# pytest tests/
# ========================= X passed in 0.XXs =========================
```
============================== test session starts ==============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\HUAWEI\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.9.0
collected 7 items                                                                

tests\test_bug_fixes.py ....                                               [ 57%]
tests\test_game_logic.py ...                                               [100%]

=============================== 7 passed in 0.02s ===============================

