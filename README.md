# bePythonic

Desktop Python editor app using `PyQt6` + `QWebEngine` + `Ace Editor`, with an
OpenRouter-backed broken-code generator.

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

## OpenRouter Setup

Set your API key before using **Generate Broken Code**:

```bash
export OPENROUTER_API_KEY="your_key_here"
```

Optional model overrides:

```bash
export OPENROUTER_MODEL="qwen/qwen3-next-80b-a3b-instruct:free"
export OPENROUTER_FALLBACK_MODELS="deepseek/deepseek-v4-flash:free,google/gemma-4-26b-a4b-it:free"
```

## Runtime Note (Linux)

`QWebEngine` needs system GUI/OpenGL libraries. If launch fails with
`libGL.so.1` missing, install your distro's OpenGL runtime packages first.

## What You Get

- `QMainWindow` app shell
- `QWebEngineView` surface hosting an Ace Python editor
- Toolbar actions: `Generate Broken Code`, `Syntax Check`, `Open .py`, `Save .py`, `Clear`
- Background AI generation worker so the GUI stays responsive
- OpenRouter model fallback logic for robust code generation

## Project Layout

```text
src/bepythonic/main.py
src/bepythonic/gui/main_window.py
src/bepythonic/gui/demo_html.py
src/bepythonic/ai/broken_code_agent.py
```
