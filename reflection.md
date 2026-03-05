# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

# Answer 1: 

When I first ran the game, it looked like a normal guessing game but several things were broken right away. First, the Developer Debug Info section was visible on the homepage and showed the secret number in a dropdown, which completely gives away the answer. Second, no matter which difficulty I picked, the hint always said "Guess a number between 1 and 100", the attempts changed but the secret number range stayed 1–100 regardless of difficulty. Third, the New Game button did not properly reset the game; the secret number and attempts were not clearing correctly so the game state carried over instead of starting fresh.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

# Answer 2:
I used Claude Code as my AI assistant throughout this project. Claude correctly identified that the Developer Debug Info expander was always visible on the homepage and that the secret number was being displayed inside it. I verified this by running the app and seeing the dropdown right there on screen. One example where Claude's explanation was slightly misleading was around the sidebar range display: Claude pointed out the sidebar correctly showed the right range per difficulty, which made it seem like the game was using it, but the New Game button actually hardcodes random.randint(1, 100) regardless of difficulty, so the sidebar range is shown but never fully respected. I had to check the actual code line by line to catch that detail.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

# Answer 3:
I decided a bug was really fixed by running the app manually in the browser and testing the exact scenario that broke it — for example, switching to Easy mode and checking that the hint said "1 to 20", or clicking New Game and confirming the score and history cleared properly. I also ran the pytest tests in `tests/test_game_logic.py` using `python3 -m pytest`, which confirmed that all five tests passed after the functions were moved into `logic_utils.py` and the string-comparison bug in `check_guess` was corrected. Claude Code helped me understand that the original tests expected `check_guess` to return a plain string like `"Win"`, while the broken version in `app.py` returned a tuple — spotting that mismatch guided me to fix the function signature as part of the refactor.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

# Answer 4:
In the original app, the secret number kept changing because Streamlit reruns the entire Python file from top to bottom every single time the user does anything; clicks a button, types in a box, anything. Without protection, `random.randint()` would run again on every rerun and generate a brand new number. Think of Streamlit like a whiteboard that gets fully erased and redrawn every time someone interacts with the page; session state is like a sticky note on the side of the board that survives each erase. The fix that finally stabilized the secret number was wrapping it in `if "secret" not in st.session_state:`; this means the secret is only generated once on the very first load and stays the same for the rest of the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

# Answer 5:
One habit I want to reuse is adding `# FIXME` comments to mark the exact location of a bug before trying to fix it; it forced me to understand the problem first instead of jumping straight into editing. Next time I work with AI on a coding task I would ask it to explain *why* a fix works, not just what to change, so I can catch it if the reasoning is wrong. This project changed how I think about AI-generated code because I used to assume it was either fully correct or obviously broken; now I know it can look clean and run without errors while still having subtle logic bugs baked in that only show up when you actually play the game.

---

## Challenge 5: AI Model Comparison

**Bug tested:** The `check_guess` function converted the secret number to a string on even-numbered attempts, causing hints to flip direction due to string vs. integer comparison.

**Claude Code suggestion:**
Claude immediately identified the root cause, the `if st.session_state.attempts % 2 == 0: secret = str(...)` block and suggested removing it entirely and always passing the integer secret directly to `check_guess`. It also explained *why* the bug caused wrong hints: in Python, string comparison is lexicographic, so `"9" > "50"` is `True` because `"9"` comes after `"5"` alphabetically. The fix was clear and the explanation made the behavior easy to verify.

**ChatGPT suggestion (for comparison):**
When given the same broken code, ChatGPT suggested adding a type check inside `check_guess` to handle both string and integer secrets essentially working around the bug instead of removing it. While the suggestion worked, it added complexity and didn't explain why the string conversion was happening in the first place.

**Comparison:**
Claude Code gave a more readable fix by deleting the problematic code rather than patching around it, and explained the "why" (lexicographic comparison) clearly. ChatGPT's fix was technically valid but defensive in a way that left the bad code in place. For debugging intentional bugs like this, Claude's approach of finding and removing the root cause was more useful.
