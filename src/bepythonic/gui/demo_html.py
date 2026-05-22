"""Embedded Ace editor page rendered inside QWebEngineView."""

EDITOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>bePythonic Code Editor</title>
  <style>
    :root {
      --bg: #091019;
      --panel: #0f1724;
      --panel-2: #152032;
      --text: #e6edf7;
      --muted: #8ca0ba;
      --accent: #4fd1c5;
      --warn: #f6ad55;
      --radius: 14px;
    }

    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 15% 10%, rgba(79, 209, 197, 0.13) 0, transparent 35%),
        radial-gradient(circle at 85% 100%, rgba(246, 173, 85, 0.14) 0, transparent 35%),
        var(--bg);
    }

    #root {
      width: 100%;
      height: 100%;
      padding: 14px;
      display: grid;
      gap: 10px;
      grid-template-rows: auto 1fr auto;
    }

    .top {
      border: 1px solid #1f2d44;
      border-radius: var(--radius);
      background: linear-gradient(130deg, #0f1724, #1a2640);
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .title {
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: 0.02em;
    }

    .subtitle {
      color: var(--muted);
      font-size: 0.86rem;
    }

    .status {
      color: var(--accent);
      font-size: 0.82rem;
      text-align: right;
    }

    #editor-wrap {
      border: 1px solid #22334d;
      border-radius: var(--radius);
      overflow: hidden;
      background: var(--panel-2);
    }

    #editor {
      width: 100%;
      height: 100%;
      min-height: 320px;
    }

    #fallback-editor {
      width: 100%;
      height: 100%;
      border: 0;
      outline: none;
      resize: none;
      color: var(--text);
      background: #121b2b;
      padding: 16px;
      font-size: 14px;
      line-height: 1.55;
      font-family: "Cascadia Code", "Fira Code", monospace;
      display: none;
    }

    .bottom {
      border: 1px solid #1f2d44;
      border-radius: var(--radius);
      background: var(--panel);
      padding: 8px 12px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
      font-size: 0.85rem;
      color: var(--muted);
    }

    .badge {
      background: rgba(79, 209, 197, 0.08);
      border: 1px solid rgba(79, 209, 197, 0.25);
      color: var(--accent);
      border-radius: 999px;
      padding: 4px 10px;
      font-weight: 600;
    }

    .warn {
      color: var(--warn);
    }
  </style>
</head>
<body>
  <div id="root">
    <section class="top">
      <div>
        <div class="title">bePythonic AI Editor</div>
        <div class="subtitle">Python code workspace powered by Ace + QWebEngine</div>
      </div>
      <div id="engine-status" class="status">Loading editor engine...</div>
    </section>

    <section id="editor-wrap">
      <div id="editor"></div>
      <textarea id="fallback-editor" spellcheck="false"></textarea>
    </section>

    <section class="bottom">
      <span class="badge">Language: Python</span>
      <span id="line-count">Lines: 0</span>
      <span id="char-count">Chars: 0</span>
      <span id="selection-count">Selection: 0</span>
      <span class="warn">Tip: Use toolbar actions to Generate/Open/Save/Syntax Check.</span>
    </section>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/ace.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/mode-python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/theme-monokai.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/ext-language_tools.min.js"></script>
  <script>
    const engineStatus = document.getElementById("engine-status");
    const lineCount = document.getElementById("line-count");
    const charCount = document.getElementById("char-count");
    const selectionCount = document.getElementById("selection-count");
    const fallbackEl = document.getElementById("fallback-editor");
    const editorHost = document.getElementById("editor");

    const STARTER_CODE = [
      "def greet(name):",
      "    print(f'Hello, {name}!')",
      "",
      "if __name__ == '__main__':",
      "    greet('bePythonic')",
      "",
    ].join("\\n");

    let editor = null;
    let fallbackMode = false;

    function getCodeValue() {
      if (editor) {
        return editor.getValue();
      }
      return fallbackEl.value;
    }

    function setCodeValue(nextCode) {
      const safeCode = typeof nextCode === "string" ? nextCode : "";
      if (editor) {
        editor.setValue(safeCode, -1);
      } else {
        fallbackEl.value = safeCode;
      }
      updateStats();
    }

    function getSelectedLength() {
      if (editor) {
        return editor.getSelectedText().length;
      }
      const start = fallbackEl.selectionStart || 0;
      const end = fallbackEl.selectionEnd || 0;
      return Math.max(0, end - start);
    }

    function updateStats() {
      const text = getCodeValue();
      const lines = text ? text.split("\\n").length : 0;
      lineCount.textContent = `Lines: ${lines}`;
      charCount.textContent = `Chars: ${text.length}`;
      selectionCount.textContent = `Selection: ${getSelectedLength()}`;
    }

    function useFallbackEditor(message) {
      fallbackMode = true;
      editorHost.style.display = "none";
      fallbackEl.style.display = "block";
      fallbackEl.value = STARTER_CODE;
      fallbackEl.addEventListener("input", updateStats);
      fallbackEl.addEventListener("select", updateStats);
      engineStatus.textContent = message;
      updateStats();
    }

    function initAceEditor() {
      if (!window.ace) {
        useFallbackEditor("Ace CDN unavailable, using fallback textarea.");
        return;
      }

      editor = window.ace.edit("editor");
      editor.session.setMode("ace/mode/python");
      editor.setTheme("ace/theme/monokai");
      editor.setShowPrintMargin(false);
      editor.session.setTabSize(4);
      editor.session.setUseSoftTabs(true);
      editor.setOptions({
        fontSize: "14px",
        enableBasicAutocompletion: true,
        enableLiveAutocompletion: false,
      });
      editor.setValue(STARTER_CODE, -1);
      editor.session.on("change", updateStats);
      editor.selection.on("changeSelection", updateStats);
      engineStatus.textContent = "Ace loaded.";
      updateStats();
    }

    window.setEditorCode = function setEditorCode(code) {
      setCodeValue(code);
      return true;
    };

    window.getEditorCode = function getEditorCode() {
      return getCodeValue();
    };

    window.clearEditor = function clearEditor() {
      setCodeValue("");
      return true;
    };

    window.getEditorStats = function getEditorStats() {
      const text = getCodeValue();
      return {
        lines: text ? text.split("\\n").length : 0,
        chars: text.length,
        fallback: fallbackMode,
      };
    };

    initAceEditor();
  </script>
</body>
</html>
"""
