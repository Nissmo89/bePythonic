# bePythonic

Desktop Python editor app using `PyQt6` + `QWebEngine` + `Ace Editor`, with an
Gemini-backed broken-code generator.

## Install

```bash
pip install -e .
```

If you want lint/type/test tooling too:

```bash
pip install -e .[dev]
```

## Run

```bash
bepythonic
```

## One-Command Build + Run (Linux/Windows)

```bash
python3 build.py
```

Useful variants:

```bash
python3 build.py --build-only   # build executable only
python3 build.py --run-source   # run directly from source
python3 build.py --onefile      # build single-file executable
```

## Gemini API Setup

Set your API key before using **Generate Broken Code**:

```bash
export GEMINI_API_KEY="your_key_here"
```

Or create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_key_here
```

Optional model overrides:

```bash
export GEMINI_MODEL="gemini-3.5-flash"
export GEMINI_FALLBACK_MODELS="gemini-3.5-flash-lite,gemini-2.5-flash,gemini-2.5-flash-lite,gemini-2.0-flash,gemini-2.0-flash-lite"
# Optional: switch API version (defaults to v1beta)
export GEMINI_API_VERSION="v1beta"
# Optional: disable automatic model discovery (enabled by default)
export GEMINI_DISCOVER_MODELS="1"
```

## Runtime Note (Linux)

`QWebEngine` needs system GUI/OpenGL libraries. If launch fails with
`libGL.so.1` missing, install your distro's OpenGL runtime packages first.

## What You Get

- `QMainWindow` app shell
- `QWebEngineView` surface hosting an Ace Python editor
- Toolbar actions: `Generate Broken Code`, `Syntax Check`, `Open .py`, `Save .py`, `Clear`
- Background AI generation worker so the GUI stays responsive
- Gemini model fallback logic for robust code generation

## Project Layout

```text
src/bepythonic/main.py
src/bepythonic/gui/main_window.py
src/bepythonic/gui/demo_html.py
src/bepythonic/ai/broken_code_agent.py
```
