// Interactive paginated Lesson engine in the style of TutorialKit and Sololearn
window.state.activeLesson = null;
window.state.activePageIndex = 0;
window.state.selectedMcqOption = null;
window.state.filledBlankWord = null;
window.state.isStepSolved = false;
window.markdownToHtml = function(md) {
  return window.parseMarkdown ? window.parseMarkdown(md) : (md || "");
};

// Toggle Slide-over Syllabus Sidebar
window.toggleSyllabusSidebar = function(show) {
  const sidebar = document.getElementById("lesson-syllabus-sidebar");
  if (!sidebar) return;
  if (show) {
    sidebar.classList.remove("-translate-x-full");
  } else {
    sidebar.classList.add("-translate-x-full");
  }
};

// Render Course Syllabus (grouped by Modules)
window.renderSyllabusList = function() {
  const container = document.getElementById("lesson-syllabus-list");
  if (!container) return;
  
  if (!window.COURSE_CURRICULUM || window.COURSE_CURRICULUM.length === 0) {
    container.innerHTML = `<div class="text-xs text-slate-400 p-4">No modules found.</div>`;
    return;
  }

  let html = "";
  window.COURSE_CURRICULUM.forEach((mod, idx) => {
    const isCompletedModule = mod.lessons.every(l => window.state.completedLessons && window.state.completedLessons.has(l.lesson_id));
    html += `
      <div class="space-y-1.5">
        <div class="px-2.5 py-1.5 bg-slate-100 flex items-center justify-between border border-slate-200 select-none">
          <span class="text-[9px] font-mono font-bold text-slate-600 uppercase tracking-wide">${window.escapeHtml(mod.title)}</span>
          ${isCompletedModule ? '<span class="text-[9px] text-emerald-600 font-bold">✓ DONE</span>' : ''}
        </div>
        <div class="space-y-1 pl-1">
          ${mod.lessons.map(lesson => {
            const isCompleted = window.state.completedLessons && window.state.completedLessons.has(lesson.lesson_id);
            const isActive = window.state.activeLesson && window.state.activeLesson.lesson_id === lesson.lesson_id;
            return `
              <button class="w-full text-left p-2 border border-slate-200 bg-white hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex items-center justify-between gap-2 lesson-card-btn ${isActive ? 'ring-2 ring-indigo-500 font-semibold' : ''}" data-id="${window.escapeHtml(lesson.lesson_id)}">
                <div class="flex flex-col gap-0.5 truncate">
                  <span class="text-[8px] font-mono text-slate-400 uppercase">Lesson</span>
                  <span class="text-xs text-slate-800 truncate block">${window.escapeHtml(lesson.title)}</span>
                </div>
                ${isCompleted ? '<span class="text-emerald-500 text-xs shrink-0 select-none">✓</span>' : ''}
              </button>
            `;
          }).join("")}
        </div>
      </div>`;
  });
  
  container.innerHTML = html;
  container.querySelectorAll(".lesson-card-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      window.selectLesson(btn.dataset.id);
    });
  });
};

// Select a Lesson
window.selectLesson = function(lessonId, isResume = false) {
  if (!isResume) {
    window.switchMainTab("lessons");
  }
  // Check if it's a custom lesson in memory
  if (window.state.customLessons && window.state.customLessons[lessonId]) {
    window.loadLessonContent(window.state.customLessons[lessonId], isResume);
    window.toggleSyllabusSidebar(false);
    return;
  }
  
  if (!window.state.backend) {
    // Mock a lesson in browser preview mode!
    const mockLessons = {
      "what_is_python": {
        lesson_id: "what_is_python",
        title: "What is Python?",
        module_title: "Getting Started",
        estimated_minutes: 5,
        topics: ["Introduction"],
        pages: [
          {
            page_id: "theory_1",
            title: "Introduction to Python",
            page_type: "theory",
            content: "Python is a high-level, interpreted programming language known for its readability and simplicity. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability.\n\nIt is used for:\n* Web Development\n* Data Science & ML\n* Scripting & Automation\n* Desktop Applications"
          },
          {
            page_id: "code_1",
            title: "Your First Code",
            page_type: "code_example",
            content: "Below is a simple Python statement that prints a welcome message.",
            code: "print(\"Python is awesome!\")"
          },
          {
            page_id: "mcq_1",
            title: "Quick Test",
            page_type: "mcq",
            question: "Who created Python?",
            options: ["Guido van Rossum", "Dennis Ritchie", "Bjarne Stroustrup", "Linus Torvalds"],
            answer: "Guido van Rossum",
            explanation: "Guido van Rossum created Python in the late 1980s."
          }
        ]
      },
      "first_program": {
        lesson_id: "first_program",
        title: "Your First Program",
        module_title: "Getting Started",
        estimated_minutes: 5,
        topics: ["First Program"],
        pages: [
          {
            page_id: "theory_2",
            title: "Hello, World!",
            page_type: "theory",
            content: "In Python, we use the `print()` function to output text to the screen."
          },
          {
            page_id: "fill_1",
            title: "Fill in the blank",
            page_type: "fill_in_the_blank",
            content: "Complete the code to print the text.",
            prompt_text: "[blank](\"I love Python!\")",
            options: ["print", "output", "echo", "show"],
            answers: ["print"]
          }
        ]
      }
    };
    
    if (mockLessons[lessonId]) {
      window.loadLessonContent(mockLessons[lessonId], isResume);
      window.toggleSyllabusSidebar(false);
    }
    return;
  }
  
  // Fetch via Qt Bridge
  window.callBackend("getLesson", lessonId);
  window.toggleSyllabusSidebar(false);
};


// Load Lesson Content
window.loadLessonContent = function(lesson, isResume = false) {
  window.state.activeLesson = lesson;
  window.state.currentLessonId = lesson.lesson_id;
  window.state.lessonWorkspaceExpanded = false;
  window.state.lessonWorkspaceActiveTab = "console";
  
  // Set page index (either resume or start at 0)
  if (isResume && window.state.currentLessonPageIndex < lesson.pages.length) {
    window.state.activePageIndex = window.state.currentLessonPageIndex;
  } else {
    window.state.activePageIndex = 0;
  }
  
  // Update path breadcrumb
  window.ui.activePathBreadcrumb.textContent = `Lesson: ${lesson.title}`;
  
  // Initialize Monaco Editor if not done
  window.initLessonMonacoEditor();
  window.initLessonWorkspaceShell();
  
  // Clear Console and Tutor
  window.resetLessonWorkspaceOutput();
  
  const messagesPane = document.getElementById("lesson-tutor-messages");
  if (messagesPane) messagesPane.innerHTML = window.getLessonTutorIntroMarkup();
  
  // Render active page step
  window.renderLessonPage();
  
  // Render Syllabus sidebar list to reflect selection
  window.renderSyllabusList();
};

window.getLessonTutorIntroMarkup = function() {
  return `<div class="lesson-sol-tutor-intro">Ask for a hint when you get stuck on this step.</div>`;
};

window.resetLessonWorkspaceOutput = function() {
  const consolePane = document.getElementById("lesson-console-pane");
  const outputShell = document.getElementById("lesson-inline-output-shell");
  if (consolePane) {
    consolePane.innerHTML = `<div class="lesson-sol-console-empty">Console output will display here when you run code.</div>`;
  }
  if (outputShell) outputShell.classList.remove("show");
};

window.isLessonWorkspacePage = function(page) {
  return Boolean(page && (page.page_type === "code_example" || (page.page_type === "theory" && page.code)));
};

window.updateLessonWorkspaceHeader = function(lesson, page, pageIndex) {
  const editorTabEl = document.getElementById("lesson-editor-tab-label");

  if (editorTabEl) {
    editorTabEl.textContent = page && page.code_filename ? page.code_filename : "py";
  }
};

window.setLessonEditorValue = function(nextCode) {
  const safeCode = nextCode || "";
  window.state.pendingLessonCode = safeCode;

  if (window.state.lessonEditor) {
    window.state.lessonEditor.setValue(safeCode);
  } else {
    window.initLessonMonacoEditor();
  }
};

window.layoutLessonInlineEditor = function() {
  if (!window.state.lessonEditor) return;
  setTimeout(() => {
    if (window.state.lessonEditor) {
      window.state.lessonEditor.layout();
    }
  }, 0);
};

window.setLessonEditorInteractionState = function(unlocked) {
  const isUnlocked = Boolean(unlocked);
  const stage = document.getElementById("lesson-editor-body-container");
  const editButton = document.getElementById("lesson-inline-edit-btn");

  window.state.lessonEditorUnlocked = isUnlocked;

  if (stage) {
    stage.classList.toggle("lesson-widget-editor-stage--editing", isUnlocked);
  }

  if (editButton) {
    editButton.classList.toggle("hidden", isUnlocked);
  }

  if (window.state.lessonEditor) {
    window.state.lessonEditor.updateOptions({
      readOnly: !isUnlocked,
      domReadOnly: !isUnlocked,
      renderLineHighlight: isUnlocked ? "all" : "line"
    });
  }
};

window.resetLessonEditorInteraction = function(page) {
  if (!window.isLessonWorkspacePage(page)) {
    window.setLessonEditorInteractionState(false);
    return;
  }

  window.setLessonEditorInteractionState(true);
};

window.focusLessonEditor = function() {
  if (!window.state.lessonEditor) {
    window.initLessonMonacoEditor();
    setTimeout(window.focusLessonEditor, 120);
    return;
  }

  window.setLessonEditorInteractionState(true);

  const model = window.state.lessonEditor.getModel();
  if (model) {
    const lastLine = model.getLineCount();
    const lastColumn = model.getLineMaxColumn(lastLine);
    window.state.lessonEditor.setPosition({ lineNumber: lastLine, column: lastColumn });
  }

  window.state.lessonEditor.focus();
};

window.openLessonInPlayground = function() {
  const lesson = window.state.activeLesson;
  const page = lesson ? lesson.pages[window.state.activePageIndex] : null;
  const currentCode = window.state.lessonEditor
    ? window.state.lessonEditor.getValue()
    : (window.state.pendingLessonCode || "");

  if (currentCode) {
    window.setCodeValue(currentCode);
  }

  const playgroundTitle = document.getElementById("playground-instructions-title");
  const playgroundBody = document.getElementById("playground-instructions-body");
  if (playgroundTitle) {
    playgroundTitle.textContent = page && page.title ? page.title : "Lesson Playground";
  }
  if (playgroundBody && lesson && page) {
    playgroundBody.innerHTML = `
      <p class="text-xs text-slate-500 leading-relaxed font-medium">${window.escapeHtml(lesson.title)}</p>
      <div class="p-3.5 border border-slate-100 bg-slate-50/50 text-[11px] leading-relaxed text-slate-600 rounded-lg">
        Continue editing this lesson code in the full playground view.
      </div>
      <div class="text-xs text-slate-600 leading-relaxed prose">
        ${window.markdownToHtml(page.content || "")}
      </div>`;
  }

  window.switchMainTab("playground");
};

window.setLessonWorkspaceVisibility = function(page) {
  const editorWrapper = document.getElementById("lesson-inline-editor-wrapper");
  if (!editorWrapper) return;

  if (!window.isLessonWorkspacePage(page)) {
    editorWrapper.classList.add("hidden");
    window.setLessonEditorInteractionState(false);
    return;
  }

  editorWrapper.classList.remove("hidden");
  window.resetLessonEditorInteraction(page);
  setTimeout(window.layoutLessonInlineEditor, 80);
};

window.initLessonWorkspaceShell = function() {
  if (window.state.lessonWorkspaceInitialized) {
    window.layoutLessonInlineEditor();
    return;
  }

  const stage = document.getElementById("lesson-editor-body-container");
  if (stage && !stage.dataset.lessonBound) {
    stage.addEventListener("pointerdown", (event) => {
      if (window.state.lessonEditorUnlocked) return;
      if (event.target.closest && event.target.closest("#lesson-inline-edit-btn")) return;

      const placeholder = document.getElementById("lesson-editor-placeholder");
      if (placeholder && !placeholder.classList.contains("hidden")) return;

      window.focusLessonEditor();
    });
    stage.dataset.lessonBound = "true";
  }

  window.addEventListener("resize", window.layoutLessonInlineEditor);

  window.state.lessonWorkspaceInitialized = true;
  window.layoutLessonInlineEditor();
};

// Initialize Lesson Monaco Editor
window.initLessonMonacoEditor = function() {
  if (window.state.lessonEditor) return;
  const host = document.getElementById("lesson-editor-host");
  if (!host) return;
  
  // Ensure monaco is available
  if (!window.monaco || !window.monaco.editor) {
    setTimeout(window.initLessonMonacoEditor, 100);
    return;
  }

  if (!window.state.lessonMonacoThemeReady) {
    window.monaco.editor.defineTheme("bepythonic-sololearn", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "", foreground: "C8D2DB", background: "171A1C" },
        { token: "comment", foreground: "6B7F99" },
        { token: "keyword", foreground: "149EF2" },
        { token: "number", foreground: "FFA310" },
        { token: "string", foreground: "40BF9C" },
        { token: "delimiter", foreground: "C8D2DB" },
        { token: "identifier", foreground: "F9F9FA" }
      ],
      colors: {
        "editor.background": "#171A1C",
        "editor.foreground": "#C8D2DB",
        "editorCursor.foreground": "#F9F9FA",
        "editor.lineHighlightBackground": "#20262B",
        "editorLineNumber.foreground": "#6B7F99",
        "editorLineNumber.activeForeground": "#F9F9FA",
        "editor.selectionBackground": "#244E74",
        "editor.inactiveSelectionBackground": "#20384C",
        "editorIndentGuide.background1": "#2D3846",
        "editorIndentGuide.activeBackground1": "#6B7F99",
        "editorWhitespace.foreground": "#2D3846",
        "editorBracketMatch.background": "#20384C",
        "editorBracketMatch.border": "#149EF2",
        "scrollbarSlider.background": "#79797966",
        "scrollbarSlider.hoverBackground": "#646464B2",
        "scrollbarSlider.activeBackground": "#A1A3A499"
      }
    });
    window.state.lessonMonacoThemeReady = true;
  }
  
  window.state.lessonEditor = window.monaco.editor.create(host, {
    value: window.state.pendingLessonCode || "",
    language: "python",
    theme: "bepythonic-sololearn",
    automaticLayout: true,
    minimap: { enabled: false },
    fontFamily: "Fira Mono, monospace",
    fontSize: 14,
    lineHeight: 17,
    tabSize: 4,
    insertSpaces: true,
    autoClosingBrackets: "always",
    matchBrackets: "always",
    scrollBeyondLastLine: false,
    glyphMargin: false,
    folding: false,
    lineNumbers: "on",
    lineNumbersMinChars: 2,
    lineDecorationsWidth: 10,
    overviewRulerLanes: 0,
    hideCursorInOverviewRuler: true,
    renderLineHighlight: "all",
    roundedSelection: false,
    readOnly: false,
    domReadOnly: false,
    scrollbar: {
      verticalScrollbarSize: 9,
      horizontalScrollbarSize: 9,
      useShadows: false
    },
    padding: { top: 17, bottom: 17 }
  });

  window.state.lessonEditor.onDidFocusEditorText(() => {
    window.setLessonEditorInteractionState(true);
  });

  window.state.pendingLessonCode = null;
  window.setLessonEditorInteractionState(true);
};

// Render active page step
window.renderLessonPage = function() {
  const lesson = window.state.activeLesson;
  if (!lesson) return;
  
  const pageIndex = window.state.activePageIndex;
  const page = lesson.pages[pageIndex];
  if (!page) return;
  
  // Save progress state on backend
  window.state.currentLessonPageIndex = pageIndex;
  window.callBackend("saveProgress", lesson.lesson_id, pageIndex, JSON.stringify(Array.from(window.state.completedLessons || [])));
  
  // Reset state variables
  window.state.selectedMcqOption = null;
  window.state.filledBlankWord = null;
  window.state.isStepSolved = false;
  window.resetLessonWorkspaceOutput();
  
  // Header text updates
  document.getElementById("lesson-module-title").textContent = lesson.module_title || "Python Studio";
  document.getElementById("lesson-title-label").textContent = lesson.title;
  document.getElementById("lesson-progress-text").textContent = `Page ${pageIndex + 1} of ${lesson.pages.length}`;
  window.updateLessonWorkspaceHeader(lesson, page, pageIndex);
  
  // Render Step dots
  const dotsContainer = document.getElementById("lesson-step-dots");
  dotsContainer.innerHTML = lesson.pages.map((p, idx) => {
    let colorClass = "bg-slate-200";
    if (idx === pageIndex) {
      colorClass = "bg-indigo-500 w-4"; // Highlight active
    } else if (idx < pageIndex) {
      colorClass = "bg-emerald-500"; // Completed steps
    }
    return `<span class="h-1.5 rounded-full transition-all duration-300 ${colorClass} ${idx === pageIndex ? 'flex-1' : 'w-1.5'}"></span>`;
  }).join("");
  
  // Populate instruction body
  const bodyHost = document.getElementById("lesson-instruction-copy");
  const editorPlaceholder = document.getElementById("lesson-editor-placeholder");
  if (editorPlaceholder) editorPlaceholder.classList.add("hidden");
  
  let contentHtml = `<h3 class="text-sm font-bold text-slate-800">${window.escapeHtml(page.title)}</h3>`;
  
  if (page.page_type === "theory") {
    contentHtml += `
      <div class="text-xs text-slate-600 leading-relaxed space-y-3 prose">
        ${window.markdownToHtml(page.content)}
      </div>`;
    // Set code editor value and show placeholder overlay
    if (page.code) {
      window.setLessonEditorValue(page.code);
    }
    window.state.isStepSolved = true; // Theory steps are always instantly completed
    
  } else if (page.page_type === "code_example") {
    contentHtml += `
      <div class="text-xs text-slate-600 leading-relaxed space-y-3 prose">
        ${window.markdownToHtml(page.content)}
      </div>
      <div class="p-3 bg-amber-50 border border-amber-100 text-[10px] text-amber-700 leading-relaxed">
        👉 <strong>Interactive Code:</strong> Edit the Python program in the editor below and click <strong>Run</strong> to test its output.
      </div>`;
    
    // Load code into editor, hide overlay
    window.setLessonEditorValue(page.code || "");
    if (editorPlaceholder) editorPlaceholder.classList.add("hidden");
    window.state.isStepSolved = true;
    
  } else if (page.page_type === "mcq") {
    contentHtml += `
      <div class="text-xs text-slate-600 leading-relaxed prose mb-4">
        ${window.markdownToHtml(page.content || "")}
      </div>
      <div class="space-y-2 select-none">
        <p class="text-xs font-bold text-slate-700">${window.escapeHtml(page.question)}</p>
        <div class="space-y-2 pt-1" id="mcq-options-container">
          ${page.options.map(opt => `
            <button class="w-full text-left p-3 border border-slate-200 hover:border-indigo-300 hover:bg-slate-50 transition-all font-medium text-xs flex items-center justify-between select-none mcq-opt-btn" onclick="selectMcqOption(this, '${window.escapeHtml(opt)}')">
              <span>${window.escapeHtml(opt)}</span>
              <span class="w-4 h-4 border border-slate-300 rounded-full flex items-center justify-center shrink-0 opt-check-circle"></span>
            </button>
          `).join("")}
        </div>
      </div>
      <div id="quiz-feedback-box" class="hidden p-4 border text-xs"></div>`;
    
    // Hide code placeholder, load code if any
    if (page.code) {
      window.setLessonEditorValue(page.code);
    }
    window.state.isStepSolved = false;
    
  } else if (page.page_type === "fill_in_the_blank") {
    // Render text with blank
    const blankRegex = /\[blank\]/g;
    const promptWithBlank = page.prompt_text.replace(blankRegex, `<span id="blank-placeholder" class="inline-block px-3 py-0.5 border-b-2 border-indigo-500 font-mono font-bold text-indigo-600 bg-indigo-50/50 text-center min-w-[50px] select-none">___</span>`);
    
    contentHtml += `
      <div class="text-xs text-slate-600 leading-relaxed prose mb-4">
        ${window.markdownToHtml(page.content || "")}
      </div>
      <div class="space-y-4 select-none">
        <div class="p-4 bg-slate-50 border border-slate-150 font-mono text-xs leading-relaxed text-slate-800">
          ${promptWithBlank}
        </div>
        <div class="space-y-2">
          <p class="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">Select option to fill blank</p>
          <div class="flex flex-wrap gap-2" id="blank-options-container">
            ${page.options.map(opt => `
              <button class="px-3.5 py-1.5 border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/30 bg-white font-mono text-xs font-semibold select-none blank-opt-btn shadow-sm" onclick="fillBlank(this, '${window.escapeHtml(opt)}')">
                ${window.escapeHtml(opt)}
              </button>
            `).join("")}
          </div>
        </div>
      </div>
      <div id="quiz-feedback-box" class="hidden p-4 border text-xs"></div>`;
    
    if (page.code) {
      window.setLessonEditorValue(page.code);
    }
    window.state.isStepSolved = false;
  }
  
  if (bodyHost) bodyHost.innerHTML = contentHtml;
  
  // Configure navigation buttons
  document.getElementById("lesson-nav-prev").disabled = (pageIndex === 0);
  
  const checkBtn = document.getElementById("lesson-nav-check");
  const nextBtn = document.getElementById("lesson-nav-next");
  
  if (page.page_type === "mcq" || page.page_type === "fill_in_the_blank") {
    checkBtn.classList.remove("hidden");
    checkBtn.disabled = true; // Wait for select
    nextBtn.classList.add("hidden");
  } else {
    checkBtn.classList.add("hidden");
    nextBtn.classList.remove("hidden");
    nextBtn.textContent = (pageIndex === lesson.pages.length - 1) ? "Finish Lesson" : "Continue";
    nextBtn.disabled = false;
  }

  window.setLessonWorkspaceVisibility(page);
};

// Select MCQ Option
window.selectMcqOption = function(btnElement, value) {
  if (window.state.isStepSolved) return; // Disallow edits once solved
  
  document.querySelectorAll(".mcq-opt-btn").forEach(btn => {
    btn.classList.remove("border-indigo-500", "bg-indigo-50/20");
    btn.querySelector(".opt-check-circle").innerHTML = "";
    btn.querySelector(".opt-check-circle").className = "w-4 h-4 border border-slate-300 rounded-full flex items-center justify-center shrink-0 opt-check-circle";
  });
  
  btnElement.classList.add("border-indigo-500", "bg-indigo-50/20");
  btnElement.querySelector(".opt-check-circle").className = "w-4 h-4 bg-indigo-500 border border-indigo-500 rounded-full flex items-center justify-center shrink-0 text-white font-bold text-[8px] opt-check-circle";
  btnElement.querySelector(".opt-check-circle").innerHTML = "✓";
  
  window.state.selectedMcqOption = value;
  
  document.getElementById("lesson-nav-check").disabled = false;
};

// Fill Blank
window.fillBlank = function(btnElement, value) {
  if (window.state.isStepSolved) return;
  
  document.querySelectorAll(".blank-opt-btn").forEach(btn => {
    btn.classList.remove("border-indigo-500", "bg-indigo-50");
  });
  
  btnElement.classList.add("border-indigo-500", "bg-indigo-50");
  
  const placeholder = document.getElementById("blank-placeholder");
  if (placeholder) {
    placeholder.textContent = value;
    placeholder.classList.add("bg-indigo-100/50");
  }
  
  window.state.filledBlankWord = value;
  document.getElementById("lesson-nav-check").disabled = false;
};

// Check Quiz Answer
window.checkLessonAnswer = function() {
  const lesson = window.state.activeLesson;
  if (!lesson) return;
  
  const page = lesson.pages[window.state.activePageIndex];
  if (!page) return;
  
  let isCorrect = false;
  const feedbackBox = document.getElementById("quiz-feedback-box");
  feedbackBox.classList.remove("hidden", "bg-emerald-50", "border-emerald-200", "text-emerald-800", "bg-rose-50", "border-rose-200", "text-rose-800");
  
  if (page.page_type === "mcq") {
    isCorrect = (window.state.selectedMcqOption === page.answer);
    
    // Highlight options in UI
    document.querySelectorAll(".mcq-opt-btn").forEach(btn => {
      const optVal = btn.querySelector("span").textContent.trim();
      if (optVal === page.answer) {
        btn.classList.add("border-emerald-500", "bg-emerald-50/30");
      } else if (optVal === window.state.selectedMcqOption && !isCorrect) {
        btn.classList.add("border-rose-500", "bg-rose-50/30");
      }
    });
    
  } else if (page.page_type === "fill_in_the_blank") {
    // Blank check
    isCorrect = page.answers.some(ans => ans.toLowerCase() === (window.state.filledBlankWord || "").toLowerCase());
    
    const placeholder = document.getElementById("blank-placeholder");
    if (placeholder) {
      placeholder.className = `inline-block px-3 py-0.5 border-b-2 font-mono font-bold text-center min-w-[50px] select-none ${isCorrect ? 'border-emerald-500 text-emerald-600 bg-emerald-50' : 'border-rose-500 text-rose-600 bg-rose-50'}`;
    }
  }
  
  if (isCorrect) {
    feedbackBox.classList.add("bg-emerald-50", "border-emerald-200", "text-emerald-800");
    feedbackBox.innerHTML = `
      <div class="flex items-start gap-2.5">
        <span class="text-base">🎉</span>
        <div class="space-y-1">
          <p class="font-bold">Correct!</p>
          ${page.explanation ? `<p class="opacity-90 leading-relaxed">${window.escapeHtml(page.explanation)}</p>` : ""}
        </div>
      </div>`;
    
    window.state.isStepSolved = true;
    
    // Transition check to next button
    document.getElementById("lesson-nav-check").classList.add("hidden");
    const nextBtn = document.getElementById("lesson-nav-next");
    nextBtn.classList.remove("hidden");
    nextBtn.disabled = false;
    nextBtn.textContent = (window.state.activePageIndex === lesson.pages.length - 1) ? "Finish Lesson" : "Continue";
    
  } else {
    feedbackBox.classList.add("bg-rose-50", "border-rose-200", "text-rose-800");
    feedbackBox.innerHTML = `
      <div class="flex items-start gap-2.5">
        <span class="text-base font-bold">❌</span>
        <div class="space-y-1">
          <p class="font-bold">Incorrect answer</p>
          <p class="opacity-90 leading-relaxed">Review the concept and try again!</p>
        </div>
      </div>`;
  }
};

// Go to Next Page Step
window.goToNextPage = function() {
  const lesson = window.state.activeLesson;
  if (!lesson) return;
  
  if (window.state.activePageIndex < lesson.pages.length - 1) {
    window.state.activePageIndex++;
    window.renderLessonPage();
  } else {
    // Lesson Finished!
    window.state.completedLessons.add(lesson.lesson_id);
    
    // Save final progress
    window.callBackend("saveProgress", lesson.lesson_id, lesson.pages.length, JSON.stringify(Array.from(window.state.completedLessons)));
    
    // Update UI elements
    window.renderSyllabusList();
    if (window.renderDashboardRoadmap) window.renderDashboardRoadmap();
    if (window.updateDashboardStats) window.updateDashboardStats();
    
    // Show premium Completion screen in instruction panel
    const bodyHost = document.getElementById("lesson-instruction-copy");
    if (bodyHost) bodyHost.innerHTML = `
      <div class="flex flex-col items-center justify-center h-full text-center space-y-5 my-10 select-none animate-fadeIn">
        <span class="text-5xl">🏆</span>
        <div class="space-y-1.5">
          <h2 class="text-lg font-bold text-slate-800">Lesson Complete!</h2>
          <p class="text-xs text-slate-500 max-w-xs leading-relaxed">Congratulations, you've completed <strong>${window.escapeHtml(lesson.title)}</strong> and reinforced your understanding!</p>
        </div>
        <div class="p-3 border border-slate-150 bg-slate-50/50 text-[10px] text-slate-500 font-mono tracking-wide rounded-lg">
          +10 XP · Streak Restored
        </div>
        <button onclick="toggleSyllabusSidebar(true)" class="py-2.5 px-6 btn-tactile-primary text-xs font-semibold">
          Select Next Lesson
        </button>
      </div>`;
      
    // Set breadcrumb
    window.ui.activePathBreadcrumb.textContent = `Lesson Complete: ${lesson.title}`;
    
    // Configure buttons
    document.getElementById("lesson-nav-prev").disabled = false;
    document.getElementById("lesson-nav-next").classList.add("hidden");
    document.getElementById("lesson-nav-check").classList.add("hidden");
    window.setLessonWorkspaceVisibility(null);
  }
};

// Go to Previous Page Step
window.goToPrevPage = function() {
  if (window.state.activePageIndex > 0) {
    window.state.activePageIndex--;
    window.renderLessonPage();
  }
};

// Reset Lesson Editor Code
window.resetLessonCode = function() {
  const lesson = window.state.activeLesson;
  if (!lesson) return;
  const page = lesson.pages[window.state.activePageIndex];
  if (page && page.code) {
    window.setLessonEditorValue(page.code);
    window.resetLessonEditorInteraction(page);
    window.resetLessonWorkspaceOutput();
  }
};

// Run Lesson Code
window.runLessonCode = function() {
  if (!window.state.lessonEditor) return;
  const code = window.state.lessonEditor.getValue();
  
  // Set execution source routing flag
  window.state.runRequestSource = "lesson";
  
  const consolePane = document.getElementById("lesson-console-pane");
  const outputShell = document.getElementById("lesson-inline-output-shell");
  if (consolePane) {
    consolePane.innerHTML = `<div class="lesson-sol-console-empty">Running process script...</div>`;
  }
  if (outputShell) outputShell.classList.add("show");
  
  // Call backend compiler
  window.callBackend("runCode", code);
};

// Switch Right Panel Tabs (Console Output vs AI Tutor Hint)
window.switchLessonTab = function(tab) {
  const consoleTabBtn = document.getElementById("lesson-tab-console-btn");
  const tutorTabBtn = document.getElementById("lesson-tab-tutor-btn");
  const consolePane = document.getElementById("lesson-console-pane");
  const tutorPane = document.getElementById("lesson-tutor-pane");
  if (!consoleTabBtn || !tutorTabBtn || !consolePane || !tutorPane) return;

  window.state.lessonWorkspaceActiveTab = tab === "tutor" ? "tutor" : "console";

  const showConsole = window.state.lessonWorkspaceActiveTab === "console";
  consoleTabBtn.classList.toggle("lesson-sol-output-tab--active", showConsole);
  tutorTabBtn.classList.toggle("lesson-sol-output-tab--active", !showConsole);
  consolePane.classList.toggle("hidden", !showConsole);
  tutorPane.classList.toggle("hidden", showConsole);
};

// Send Lesson Tutor Message
window.sendLessonTutorMessage = function() {
  const inputEl = document.getElementById("lesson-tutor-input");
  if (!inputEl) return;
  
  const text = inputEl.value.trim();
  if (!text) return;
  
  // Append user message
  window.appendLessonTutorMessage("user", text);
  inputEl.value = "";
  inputEl.disabled = true;
  
  // Construct context-sensitized query
  const lesson = window.state.activeLesson;
  const page = lesson ? lesson.pages[window.state.activePageIndex] : null;
  const codeVal = window.state.lessonEditor ? window.state.lessonEditor.getValue() : "";
  
  let contextPrompt = "";
  if (lesson && page) {
    contextPrompt = `[CONTEXT: The user is doing lesson "${lesson.title}", step: "${page.title}" (page type: "${page.page_type}").
Instruction Content: "${page.content || page.prompt_text}"
Current code in the editor is:
\`\`\`python
${codeVal}
\`\`\`
]

Question: ${text}`;
  } else {
    contextPrompt = text;
  }
  
  // Route target response source
  window.state.tutorRequestSource = "lesson";
  
  // Construct messages stack
  const history = [
    { role: "user", content: contextPrompt }
  ];
  
  window.callBackend("askAiTutor", JSON.stringify(history));
};

// Append Tutor Message in Lesson Tutor Pane
window.appendLessonTutorMessage = function(role, text) {
  const container = document.getElementById("lesson-tutor-messages");
  if (!container) return;
  
  const bubble = document.createElement("div");
  if (role === "user") {
    bubble.className = "lesson-sol-tutor-bubble lesson-sol-tutor-bubble--user";
    bubble.innerHTML = `<span class="lesson-sol-tutor-bubble-label">You</span><div>${window.escapeHtml(text)}</div>`;
  } else {
    bubble.className = "lesson-sol-tutor-bubble lesson-sol-tutor-bubble--assistant";
    bubble.innerHTML = `<span class="lesson-sol-tutor-bubble-label">AI Tutor</span><div class="prose">${window.markdownToHtml(text)}</div>`;
  }
  
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
};

// Preserve old AI Custom Lesson Generator features in the new workspace
window.showAiLessonGenerator = function() {
  window.toggleSyllabusSidebar(false);
  
  const bodyHost = document.getElementById("lesson-instruction-copy");
  if (bodyHost) bodyHost.innerHTML = `
    <div class="space-y-6 mt-6">
      <header class="space-y-2 text-center select-none">
        <span class="text-4xl block mb-2">✨</span>
        <h1 class="text-lg font-bold tracking-tight text-slate-900">AI Lesson Generator</h1>
        <p class="text-xs text-slate-500 leading-relaxed max-w-xs mx-auto">Generate a custom lesson module tailored to any concept using our advanced Gemini curriculum engine.</p>
      </header>
      
      <div class="p-4 border border-slate-200 space-y-4 shadow-sm rounded-xl">
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider font-mono">Concept / Topic</label>
          <input type="text" id="ai-lesson-topic-input" placeholder="e.g. List Comprehensions, Decorators..." class="w-full p-2.5 border border-slate-200 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <button id="ai-lesson-generate-btn" class="w-full py-2.5 px-4 btn-tactile-primary text-xs font-semibold" onclick="generateCustomLessonUI()">
          Generate Lesson Module
        </button>
        <div id="ai-lesson-progress" class="hidden h-1.5 bg-slate-100 overflow-hidden mt-2 rounded-full">
          <div class="h-full bg-indigo-500 w-1/3 animate-pulse rounded-full"></div>
        </div>
      </div>
    </div>`;
  
  // Set UI state details
  window.ui.activePathBreadcrumb.textContent = `Lesson Generator`;
  document.getElementById("lesson-module-title").textContent = "AI Studio Engine";
  document.getElementById("lesson-title-label").textContent = "Lesson Generator";
  document.getElementById("lesson-progress-text").textContent = "Page 1 of 1";
  document.getElementById("lesson-step-dots").innerHTML = `<span class="h-1.5 w-4 rounded-full bg-indigo-500"></span>`;
  
  // Configure navigation buttons
  document.getElementById("lesson-nav-prev").disabled = true;
  document.getElementById("lesson-nav-next").classList.add("hidden");
  document.getElementById("lesson-nav-check").classList.add("hidden");
  
  // Hide editor overlay
  document.getElementById("lesson-editor-placeholder").classList.add("hidden");
  window.state.lessonWorkspaceExpanded = false;
  window.setLessonWorkspaceVisibility(null);
};

window.generateCustomLessonUI = function() {
  const topic = document.getElementById("ai-lesson-topic-input").value.trim();
  if (!topic) return;
  const btn = document.getElementById("ai-lesson-generate-btn");
  btn.disabled = true;
  btn.textContent = "Synthesizing Curriculum...";
  document.getElementById("ai-lesson-progress").classList.remove("hidden");
  window.callBackend("generateCustomLesson", topic);
};
