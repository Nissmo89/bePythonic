# bePythonic Desktop Starter Spec

## Direction

`bePythonic` is now a native desktop starter, not a web UI embedded inside Qt.

The current phase is meant to keep the useful backend pieces in place while
reducing UI complexity:

- local JSON course content
- native Qt widgets
- local code execution
- Gemini-backed helper actions

## UI Surface

The starter window is split into three panes:

1. Course navigation
2. Lesson and practice workspace
3. AI tools

### Course Navigation

- Shows modules and lessons from `courses/python_beginner/course.json`
- Restores the current lesson from saved progress
- Allows a lesson to be marked complete

### Workspace

- `Lessons` tab for local course pages
- `Practice` tab for editing and running Python code
- File open/save support for `.py` files
- Syntax checking through `ast.parse`

### AI Tools

- Tutor chat
- Broken code generation
- Custom lesson outline generation

## Qt Strategy

The app should run on either:

- `PySide6`
- `PyQt6`

The binding is selected at install/build time, and `src/bepythonic/gui/qt_compat.py`
normalizes imports for the rest of the UI code.

## Data

- Course content is read from `courses/`
- Seed progress can be copied from `user_data/progress.json`
- Runtime progress is written to the user data directory for the current OS

## Out Of Scope For This Phase

- Web frontend assets
- `QWebEngine`
- `QWebChannel`
- Frameless window wrappers
- Browser-based editors
- TTK/Tk migration work

## Next Reasonable Steps

1. Add richer lesson rendering and exercises per page type.
2. Add a better code editor widget with line numbers and shortcuts.
3. Replace modal error dialogs with inline notifications.
4. Add tests around course loading and progress persistence.
5. Decide whether the long-term desktop path should stay on `PySide6` or `PyQt6`.
