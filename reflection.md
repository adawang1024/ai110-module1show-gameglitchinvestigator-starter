# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The app loaded as a "Game Glitch Investigator" number-guessing game with a title, a subtitle that said "An AI-generated guessing game. Something is off," and a "Make a guess" section. A blue info box told me to "Guess a number between 1 and 100. Attempts left: 3," and there was a "Developer Debug Info" panel showing the Secret, Attempts, Score, Difficulty, and a guess History list. At the bottom there was a text box to enter my guess, plus "Submit Guess," "New Game," and "Show hint" controls. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  - The hints are backwards: when I guessed 3 while the secret number was 55, the game told me to "go lower" as the hint. That is incorrect — since 3 is smaller than 55, it should have told me to go higher.
  - The attempt counter does not update correctly as I keep guessing. I think the index starting from 0 is the issue. When I finished attemps, the attempts left on top showed as 1. 
  - when i clicked on new game, the red box says "game over" and did not update the history. 
  - string + number input not handled properly
  - difficulty level does not correspond to correct attempts. 


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `9`, secret `55`, on an even guess | Hint "Go HIGHER" (9 < 55) | Hint "Go LOWER" — backwards | None; TypeError silently caught (`app.py:41`) |
| Guesses on Normal (8 allowed) | "Attempts left" counts down to 0 | Off by one; box always says "1 and 100" | None |
| Type `abc` and Submit | Rejected, no attempt used | Counts as an attempt, added to History | None; caught in `parse_guess` |
| Click "New Game" after losing | Board and History reset | Still shows "Game over"; History not cleared | None |
| Switch between Easy and Normal | Easy should give the most attempts | Easy gives only 6 attempts but Normal gives 8 — Easy has fewer (`app.py:80-84`); box still says "1 and 100" | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
claude

- **Give one example of an AI suggestion that was correct** (including what the AI suggested and how you verified the result).
  - **What the AI suggested:** The hints felt backwards in the game, and the AI said the bug was in `check_guess` — that the comparison branch was flipped, so a guess *greater* than the secret was being reported as "Too Low." It suggested pulling the logic out of the UI into `logic_utils.py` and fixing the branch so `guess > secret` returns `"Too High"` and otherwise returns `"Too Low"`, then mapping those outcomes to hint text in `app.py` (`HINT_MESSAGES`).
  - **Correct or incorrect:** Correct.
  - **How I verified it:** I wrote/ran the pytest regression tests in `tests/test_bug_fixes.py` — `test_high_guess_is_too_high_not_flipped` (`check_guess(60, 50) == "Too High"`), `test_low_guess_is_too_low_not_flipped` (`check_guess(40, 50) == "Too Low"`), and the extremes test — and all 4 passed. I also checked it directly: `check_guess(9, 55)` returns `"Too Low"`, which maps to "📈 Go HIGHER!", the correct hint since 9 < 55. In the running game the hint direction now matches the secret.

- **Give one example of an AI suggestion that was incorrect or misleading** (including what the AI suggested and how you verified the result).
  - **What the AI suggested:** To make `check_guess` "robust," the AI added a `try/except TypeError` fallback (`logic_utils.py:46-57`): if comparing the guess to the secret raised a `TypeError` (because the secret sometimes arrives as a string), it falls back to comparing them *as strings* (`str(guess) > secret`). It presented this as defensive code that prevents a crash.
  - **Correct or incorrect:** Misleading. It does stop the crash, but it silently produces a *wrong* answer. String comparison is lexicographic, not numeric, so on the even-attempt path in `app.py` (lines 146-149) where the secret is turned into a string, `check_guess(9, "55")` returns `"Too High"` → "📉 Go LOWER!" — which is backwards, since 9 is actually less than 55. So the very "backwards hint" bug we thought we fixed reappears on every even-numbered attempt.
  - **How I verified it:** I called the function both ways: `check_guess(9, 55)` → `"Too Low"` (correct), but `check_guess(9, "55")` → `"Too High"` (wrong). I confirmed in the game by reproducing the bug-log row — guessing `9` with secret `55` on an even attempt shows "Go LOWER" instead of "Go HIGHER." The real fix is to keep the secret an int (or coerce input to int before comparing), not to paper over the type mismatch with a string compare.

---

## 3. Debugging and testing your fixes

- **How did you decide whether a bug was really fixed?**
  - I used two checks for every bug. First, a fast automated check: I ran `pytest tests/test_bug_fixes.py` and required all tests to pass, so a fix to one branch couldn't quietly break another. Second, I reproduced the original bug-log row by hand in the running Streamlit game and confirmed the symptom was gone (e.g., the hint now points the right way, the attempt counter actually counts down, "New Game" clears the board and history). A bug only counted as fixed when both the test and the live game agreed.

- **Describe at least one test you ran (manual or using pytest) and what it showed you about your code.**
  - With pytest I ran `tests/test_bug_fixes.py` and got `4 passed in 0.01s`. The hint-direction tests (`check_guess(60, 50) == "Too High"`, `check_guess(40, 50) == "Too Low"`, and the extremes) showed me the comparison branch in `check_guess` is now correct, and `test_difficulty_ranges` confirmed Easy/Normal/Hard return `(1,20)/(1,100)/(1,50)`. Running it directly, I saw `check_guess(9, 55)` → `"Too Low"` (a correct "Go HIGHER" hint). The same exercise also exposed that the passing tests only cover the *int* path — `check_guess(9, "55")` still returns the wrong `"Too High"`, which told me my test suite has a gap and the string-fallback bug isn't yet covered.

- **Did AI help you design or understand any tests? How?**
  - Yes. The AI suggested locking each documented bug into its own regression test so the bugs "can't quietly come back," and it explained *why* `check_guess(60, 50)` should be `"Too High"` rather than just asserting it, which helped me read the test as a statement of expected behavior. It also pointed out I should test the boundary/extreme cases (1 vs 100) instead of only one happy-path value. It did not catch the missing test for the string-secret path — I found that gap myself while verifying the misleading suggestion above.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
