// Editor integration (Monaco & fallback textarea)
window.initMonacoEditor = function() {
  const MONACO_BASE_PATH = "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs";
  
  const enableFallback = () => {
    window.ui.editorHost.style.display = "none";
    window.ui.sourceCode.classList.add("fallback-active");
    window.state.fallbackEditor = window.ui.sourceCode;
    if (!window.state.fallbackEditorBound) {
      window.ui.sourceCode.addEventListener("input", () => {
        window.setDirty(true);
        window.updateEditorStats();
      });
      window.state.fallbackEditorBound = true;
    }
    window.updateEditorStats();
  };

  const mountMonaco = () => {
    if (window.state.monacoEditor) {
      return window.state.monacoEditor;
    }

    if (!window.monaco || !window.monaco.editor) {
      enableFallback();
      return null;
    }

    window.state.monaco = window.monaco;
    window.ui.editorHost.style.display = "block";
    window.ui.sourceCode.classList.remove("fallback-active");

    window.state.monacoEditor = window.state.monaco.editor.create(window.ui.editorHost, {
      value: window.ui.sourceCode.value,
      language: "python",
      theme: "vs",
      automaticLayout: true,
      minimap: { enabled: false },
      fontFamily: "IBM Plex Mono",
      fontSize: 13,
      tabSize: 4,
      insertSpaces: true,
      autoClosingBrackets: "always",
      matchBrackets: "always",
      scrollBeyondLastLine: false,
      padding: { top: 12, bottom: 12 }
    });

    window.state.monacoEditor.onDidChangeModelContent(() => {
      window.setDirty(true);
      window.updateEditorStats();
    });

    window.state.monacoEditor.onDidChangeCursorPosition(() => {
      window.updateEditorStats();
    });

    window.updateEditorStats();
    return window.state.monacoEditor;
  };

  if (!window.require) {
    enableFallback();
    return Promise.resolve(null);
  }

  window.MonacoEnvironment = {
    getWorkerUrl: function(workerId, label) {
      const source = [
        `self.MonacoEnvironment = { baseUrl: '${MONACO_BASE_PATH}/' };`,
        `importScripts('${MONACO_BASE_PATH}/base/worker/workerMain.js');`
      ].join("\n");
      return `data:text/javascript;charset=utf-8,${encodeURIComponent(source)}`;
    }
  };

  if (window.monaco && window.monaco.editor) {
    return Promise.resolve(mountMonaco());
  }

  if (!window.state.monacoConfigured) {
    window.require.config({ paths: { vs: MONACO_BASE_PATH } });
    window.state.monacoConfigured = true;
  }

  if (window.state.monacoLoadPromise) {
    return window.state.monacoLoadPromise;
  }

  window.state.monacoLoadPromise = new Promise((resolve) => {
    window.require(["vs/editor/editor.main"], () => {
      resolve(mountMonaco());
    }, () => {
      enableFallback();
      resolve(null);
    });
  });

  return window.state.monacoLoadPromise;
};

window.getCodeValue = function() {
  return window.state.monacoEditor ? window.state.monacoEditor.getValue() : window.ui.sourceCode.value;
};

window.setCodeValue = function(nextCode) {
  if (window.state.monacoEditor) {
    window.state.monacoEditor.setValue(nextCode);
  } else {
    window.ui.sourceCode.value = nextCode;
  }
  window.setDirty(false);
  window.updateEditorStats();
};

window.updateEditorStats = function() {
  let cursorStr = "Ln 1, Col 1";
  if (window.state.monacoEditor) {
    const pos = window.state.monacoEditor.getPosition();
    if (pos) {
      cursorStr = `Ln ${pos.lineNumber}, Col ${pos.column}`;
    }
  }
  window.ui.cursorPos.textContent = cursorStr;
};

window.setDirty = function(dirty) {
  window.state.isDirty = Boolean(dirty);
  if (window.state.isDirty) {
    window.ui.dirtyLabel.textContent = "Unsaved";
    window.ui.dirtyLabel.className = "text-amber-500 font-bold";
    window.ui.dirtyDot.style.backgroundColor = "#f59e0b"; // Thunder Yellow
  } else {
    window.ui.dirtyLabel.textContent = "Clean";
    window.ui.dirtyLabel.className = "text-indigo-600 font-bold";
    window.ui.dirtyDot.style.backgroundColor = "#0b84e6"; // Sea Blue
  }
};
