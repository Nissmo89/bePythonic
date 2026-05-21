# bePythonic

> **Backbone AI to learn Python — better, faster, optimal.**  
> A terminal-based Python learning platform where learners read lessons, fix broken code, solve challenges, and ask an AI tutor for help whenever they misunderstand a concept.

---

## What is bePythonic?

**bePythonic** is an AI-powered Python learning app built for the terminal.

The goal is simple:

> Help beginners learn Python step-by-step without feeling lost.

Instead of only reading theory, the learner actively writes code, fixes bugs, runs examples, solves problems, and receives AI-powered explanations when something is confusing.

bePythonic is inspired by apps like SoloLearn, Codecademy, and coding challenge platforms, but it is designed as a lightweight **CLI/TUI learning system** using Python tools like **Textual** and **Rich**.

The AI acts like a **backbone tutor** — always available to explain, guide, debug, and generate extra practice.

---

## Core Philosophy

Most beginners fail to learn programming because they misunderstand small concepts early.

For example:

- What is a variable?
- Why is indentation important?
- Why does `NameError` happen?
- Why does `input()` return a string?
- Why is `=` different from `==`?
- Why does a loop never stop?

bePythonic tries to fix that problem by giving the learner a helper at every step.

The learner should never be stuck thinking:

> “I do not understand what went wrong.”

Instead, bePythonic should respond like a tutor:

> “You used `nam` but your variable is called `name`. Python variable names must match exactly.”

---

## Project Goals

### Main Goals

- Teach Python from absolute beginner level.
- Provide structured lessons.
- Give coding tasks after every concept.
- Include broken code challenges that the learner must fix.
- Run user code safely with timeouts.
- Judge output automatically.
- Save progress locally.
- Use AI as a tutor, not as the whole course.
- Work inside terminal with a beautiful TUI.

### Secondary Goals

- Generate extra practice using AI.
- Explain errors in simple language.
- Give hints without directly revealing the answer.
- Allow offline lessons when AI is not available.
- Support beginner-friendly learning flow.
- Become a portfolio-level Python project.

---

## Why Terminal / TUI?

A normal CLI is easy to build but can feel boring.

A full GUI is attractive but takes more development time.

bePythonic chooses the middle path:

> **TUI: Terminal User Interface**

Using libraries like **Textual** and **Rich**, bePythonic can look modern while still being easier to build than a desktop GUI.

Example layout:

```txt
┌─ Lessons ───────────────┐ ┌─ Lesson Content ─────────────────────┐
│ 01. Variables           │ │ Variables are used to store data...  │
│ 02. Input / Output      │ │                                      │
│ 03. Conditions          │ │ Example:                             │
│ 04. Loops               │ │ name = "Ali"                         │
│ 05. Functions           │ │ print(name)                          │
└─────────────────────────┘ └──────────────────────────────────────┘

┌─ Code Challenge ─────────────────────────────────────────────────┐
│ Write code that prints your name.                                │
│                                                                  │
│ > name = "Ali"                                                   │
│ > print(name)                                                    │
└──────────────────────────────────────────────────────────────────┘

┌─ Output ─────────────────────────────────────────────────────────┐
│ ✅ Correct! Lesson passed.                                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Main Features

### 1. Structured Lessons

Lessons are stored locally as JSON files.

Each lesson contains:

- Title
- Difficulty
- Explanation
- Examples
- Broken code tasks
- Practice problems
- Expected outputs
- Hints
- Concept tags

Example topics:

- Variables
- Print
- Input
- Data types
- Conditions
- Loops
- Functions
- Lists
- Dictionaries
- File handling
- Error handling
- OOP basics

---

### 2. Broken Code Challenges

bePythonic will not only ask the learner to write code from scratch.

It will also give broken code.

Example:

```python
name = "Ali"
print(nam)
```

Expected learner fix:

```python
name = "Ali"
print(name)
```

This teaches debugging naturally.

Broken code challenges are important because real programmers spend a lot of time reading and fixing code.

---

### 3. Code Runner

The app runs learner code using Python itself.

Basic flow:

1. User writes code.
2. bePythonic saves code to a temporary file.
3. bePythonic runs it using `subprocess`.
4. Output is captured.
5. Errors are captured.
6. Code is stopped if it takes too long.
7. Output is compared with expected output.

Example:

```python
subprocess.run(
    ["python3", temp_file],
    capture_output=True,
    text=True,
    timeout=3
)
```

---

### 4. Output Judge

The judge checks whether the learner output is correct.

For beginner lessons, output comparison should be forgiving.

Example:

```txt
Expected:
Hello Ali

User output:
Hello Ali
```

Passed.

Later, output normalization can be added.

For example:

```txt
0 1 2
```

and

```txt
0
1
2
```

can optionally be treated as similar depending on challenge settings.

---

### 5. AI Tutor

AI is the heart of bePythonic.

But AI should not replace the course.

The best design is:

> Fixed lessons first, AI tutor second.

This makes the app reliable even when the API is unavailable.

The AI tutor can help with:

- Explaining a concept
- Explaining an error
- Giving hints
- Reviewing user code
- Generating extra practice
- Creating new broken code examples
- Explaining code line-by-line
- Simplifying difficult explanations

Example commands:

```txt
:hint
:explain
:explain-error
:debug
:generate-practice
:explain-like-beginner
:why-failed
```

---

### 6. AI Lesson Generator

bePythonic can use AI to generate extra lessons or practice sets.

However, generated lessons should be saved locally and reviewed before being added to the official lesson path.

Generated content should follow a strict JSON schema.

This prevents messy AI output.

---

### 7. Progress Tracking

bePythonic stores learner progress locally.

Progress data includes:

- Completed lessons
- Failed attempts
- Passed challenges
- Last opened lesson
- Current streak
- Total practice count
- Concepts that need revision

Example file:

```txt
data/progress.json
```

Example structure:

```json
{
    "user": "default",
    "last_lesson": "01_variables",
    "completed_lessons": ["01_variables"],
    "stats": {
        "total_runs": 20,
        "passed_challenges": 8,
        "failed_challenges": 12
    },
    "weak_topics": ["variables", "input"]
}
```

---

## Tech Stack

### Language

```txt
Python
```

### UI

```txt
Textual + Rich
```

### Code Execution

```txt
subprocess + tempfile + timeout
```

### AI

```txt
OpenRouter API
```

### Storage

For MVP:

```txt
JSON files
```

Later:

```txt
SQLite
```

### Packaging

Possible options:

```txt
pipx
uv
PyInstaller
```

---

## Proposed Folder Structure

```txt
bepythonic/
  README.md
  pyproject.toml
  .env.example
  .gitignore

  bepythonic/
    __init__.py
    main.py

    app.py

    screens/
      __init__.py
      home_screen.py
      lesson_screen.py
      challenge_screen.py
      progress_screen.py
      settings_screen.py
      ai_chat_screen.py

    widgets/
      __init__.py
      lesson_list.py
      code_editor.py
      output_panel.py
      status_bar.py
      progress_card.py

    core/
      __init__.py
      lesson_loader.py
      lesson_models.py
      runner.py
      judge.py
      progress.py
      config.py
      ai_agent.py
      prompt_builder.py
      lesson_generator.py

    lessons/
      index.json
      beginner/
        01_variables.json
        02_print.json
        03_input.json
        04_conditions.json
        05_loops.json

    data/
      progress.json
      generated_lessons/

    themes/
      default.tcss
      bepythonic_dark.tcss
      bepythonic_light.tcss

  tests/
    test_judge.py
    test_runner.py
    test_lesson_loader.py
```

---

## Architecture Overview

```txt
┌──────────────────────────────────────┐
│              Textual UI               │
│ Home / Lessons / Challenge / AI Chat  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│             Core Services             │
│ LessonLoader / Runner / Judge         │
│ ProgressManager / AIAgent             │
└──────────────────┬───────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌────────────┐ ┌─────────┐ ┌─────────────┐
│ Lessons    │ │ Progress│ │ OpenRouter  │
│ JSON Files │ │ JSON    │ │ AI API      │
└────────────┘ └─────────┘ └─────────────┘
```

---

## Main Modules

### `main.py`

Entry point of the application.

Responsibilities:

- Start the Textual app.
- Load configuration.
- Initialize required folders.

---

### `app.py`

Main Textual application class.

Responsibilities:

- Register screens.
- Manage navigation.
- Hold global app state.

---

### `lesson_loader.py`

Loads lessons from JSON files.

Responsibilities:

- Read `lessons/index.json`.
- Load individual lessons.
- Validate lesson schema.
- Return lesson objects.

---

### `lesson_models.py`

Contains dataclasses or Pydantic models for lesson data.

Possible models:

- `Lesson`
- `Example`
- `Challenge`
- `TestCase`
- `Hint`

---

### `runner.py`

Runs learner code.

Responsibilities:

- Create temporary Python file.
- Execute code using subprocess.
- Capture stdout.
- Capture stderr.
- Stop infinite loops using timeout.
- Return result object.

---

### `judge.py`

Checks if output is correct.

Responsibilities:

- Compare user output with expected output.
- Normalize whitespace when needed.
- Return pass/fail result.
- Give simple failure reason.

---

### `progress.py`

Handles local progress.

Responsibilities:

- Load progress file.
- Save progress file.
- Mark lesson completed.
- Track attempts.
- Track weak concepts.

---

### `ai_agent.py`

Handles AI communication.

Responsibilities:

- Send prompts to OpenRouter.
- Receive AI response.
- Handle API errors.
- Avoid exposing API key.
- Support tutor commands.

---

### `prompt_builder.py`

Builds safe and structured prompts for AI.

Responsibilities:

- Create hint prompt.
- Create debug prompt.
- Create explanation prompt.
- Create lesson generation prompt.
- Keep AI responses beginner-friendly.

---

### `lesson_generator.py`

Generates optional AI-based lessons and practice tasks.

Responsibilities:

- Ask AI for lesson JSON.
- Validate generated JSON.
- Save generated lessons locally.
- Mark generated lessons as unofficial until reviewed.

---

## Lesson JSON Format

Example lesson:

```json
{
    "id": "01_variables",
    "title": "Variables",
    "level": "beginner",
    "concepts": ["variables", "print"],
    "description": "Learn how to store values using variables.",
    "explanation": "A variable is like a named box that stores a value.",
    "examples": [
        {
            "title": "Store a name",
            "code": "name = \"Ali\"\nprint(name)",
            "output": "Ali"
        }
    ],
    "challenges": [
        {
            "id": "fix_variable_name",
            "type": "fix_broken_code",
            "title": "Fix the variable name",
            "instruction": "Fix the code so it prints Ali.",
            "starter_code": "name = \"Ali\"\nprint(nam)",
            "expected_output": "Ali",
            "hints": [
                "Check the spelling of the variable name.",
                "Python variable names must match exactly."
            ]
        },
        {
            "id": "print_your_name",
            "type": "write_code",
            "title": "Print a name",
            "instruction": "Create a variable called name and print it.",
            "starter_code": "# write your code here\n",
            "expected_output": "Ali"
        }
    ]
}
```

---

## Challenge Types

bePythonic can support multiple challenge types.

### 1. Read Lesson

Learner reads explanation and examples.

### 2. Predict Output

Learner guesses what code will print.

### 3. Fix Broken Code

Learner fixes a buggy program.

### 4. Write Code

Learner writes code from scratch.

### 5. Mini Quiz

Learner answers simple multiple-choice questions.

### 6. Final Mission

Learner solves a slightly bigger problem using all learned concepts.

---

## AI Tutor Flow

When code fails, bePythonic can send structured context to AI.

```txt
User is learning: Variables
Challenge: Fix the variable name
Instruction: Fix the code so it prints Ali.
User code:
name = "Ali"
print(nam)

Error:
NameError: name 'nam' is not defined

Expected output:
Ali

Explain the issue in very simple beginner language.
Do not give the full answer immediately.
Give one hint first.
```

AI response should be beginner-friendly:

```txt
You are very close. The problem is that Python cannot find a variable named `nam`.
You created a variable called `name`, but you tried to print `nam`.

Hint: Check if both variable names are spelled the same.
```

---

## OpenRouter Configuration

Use environment variables for API keys.

`.env.example`:

```env
OPENROUTER_API_KEY=your_api_key_here
BEPYTHONIC_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

Never commit `.env` to GitHub.

`.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.pytest_cache/
dist/
build/
.venv/
```

---

## Code Runner Safety

For MVP, bePythonic should protect itself from basic beginner mistakes.

Minimum safety features:

- Run code in a temporary file.
- Use timeout.
- Capture output.
- Kill long-running code.
- Limit output length.
- Do not run as administrator/root.

Example dangerous beginner code:

```python
while True:
    print("hello")
```

bePythonic should stop it after a few seconds.

Future sandbox improvements:

- Run in isolated process.
- Limit memory.
- Restrict file access.
- Use Docker or another sandbox for advanced safety.

---

## MVP Roadmap

### Phase 1 — Basic CLI Prototype

- Create project structure.
- Add lesson JSON loader.
- Add 3 beginner lessons.
- Let user select lesson from terminal.
- Show explanation.
- Run simple code challenge.
- Compare output.
- Save progress.

### Phase 2 — Textual TUI

- Add Textual app.
- Home screen.
- Lesson list screen.
- Lesson content screen.
- Code challenge screen.
- Output panel.
- Progress screen.

### Phase 3 — AI Tutor

- Add OpenRouter API support.
- Add `:hint` command.
- Add `:explain-error` command.
- Add `:debug` command.
- Add AI fallback error messages.

### Phase 4 — Better Lessons

- Add more beginner lessons.
- Add broken code challenges.
- Add mini quizzes.
- Add final missions.
- Add weak-topic detection.

### Phase 5 — AI Practice Generator

- Generate extra practice tasks.
- Validate generated JSON.
- Save generated practice locally.
- Let learner retry weak topics.

### Phase 6 — Packaging

- Add `pyproject.toml` scripts.
- Support install with `pipx` or `uv`.
- Build standalone binary later with PyInstaller.

---

## MVP Command Ideas

```txt
bepythonic start
bepythonic lesson 01_variables
bepythonic progress
bepythonic practice
bepythonic ai "explain loops"
```

Inside TUI:

```txt
:run
:hint
:debug
:explain
:next
:back
:progress
:quit
```

---

## Example User Flow

```txt
1. User opens bePythonic.
2. User selects Lesson 01: Variables.
3. bePythonic explains variables.
4. User reads example.
5. User gets broken code.
6. User fixes code.
7. bePythonic runs the code.
8. Judge checks output.
9. If failed, AI tutor explains the mistake.
10. If passed, progress is saved.
11. User unlocks next lesson.
```

---

## Visual Identity

### Name

```txt
bePythonic
```

### Tagline

```txt
Backbone AI to learn Python — better, faster, optimal.
```

### Meaning

The name comes from the idea that learning needs a strong backbone.

bePythonic acts like a support system behind the learner.

It does not let the learner collapse because of confusion.

---

## Possible UI Theme

Recommended default theme:

```txt
Dark terminal theme
Soft blue / cyan accents
Green success messages
Yellow hints
Red error messages
```

Example status colors:

```txt
✅ Passed     -> green
❌ Failed     -> red
💡 Hint       -> yellow
🤖 AI Tutor   -> cyan
📘 Lesson     -> blue
```

---

## Future Ideas

- Multi-language support later.
- Python interview preparation mode.
- Daily challenge mode.
- Streak system.
- XP and levels.
- Local leaderboard.
- AI-generated revision plan.
- Voice explanation mode.
- Export progress report.
- Teacher mode to create lessons.
- Built-in beginner Python notes.
- Offline-only mode without AI.

---

## Development Principles

bePythonic should be:

- Beginner-friendly
- Fast
- Clean
- Offline-first
- AI-assisted, not AI-dependent
- Easy to extend
- Safe enough for beginner code execution
- Fun to use

---

## Initial Priority

The first working version should not try to do everything.

The first version only needs:

```txt
Lesson JSON -> Show Lesson -> Run Code -> Judge Output -> Save Progress
```

After that, AI tutor can be added.

This keeps the project realistic and buildable.

---

## License

License can be decided later.

Recommended:

```txt
MIT License
```

---

## Final Vision

bePythonic should feel like this:

> A beginner opens the terminal, starts a Python lesson, writes code, makes mistakes, gets help instantly, understands the mistake, fixes it, and keeps moving forward.

Not just a course.

Not just an AI chatbot.

Not just a code runner.

**bePythonic is a backbone for learning Python.**
