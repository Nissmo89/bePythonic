// Application state and selectors definitions
window.state = {
  backend: null,
  monaco: null,
  monacoEditor: null,
  monacoConfigured: false,
  monacoLoadPromise: null,
  lessonEditor: null,
  lessonEditorUnlocked: false,
  pendingLessonCode: null,
  lessonMonacoThemeReady: false,
  fallbackEditor: null,
  fallbackEditorBound: false,
  hasBooted: false,
  isDirty: false,
  currentPage: "home",
  currentLessonId: null,
  lessonWorkspaceExpanded: false,
  lessonWorkspaceKeyBound: false,
  lessonWorkspaceInitialized: false,
  lessonWorkspaceSplit: 50,
  lessonWorkspaceActiveTab: "console",
  runRequestSource: null,
  tutorRequestSource: null,
  chatHistory: [],
  qwebChannelPromise: null,
};

// Main UI mappings resolved at boot
window.ui = {};

window.initUiReferences = function() {
  window.ui = {
    appShell: document.getElementById("app-shell"),
    welcomeScreen: document.getElementById("welcome-screen"),
    enterStudioBtn: document.getElementById("enter-studio-btn"),
    bridgeStatus: document.getElementById("bridge-status"),
    bridgeDot: document.getElementById("bridge-dot"),
    
    chatInput: document.getElementById("chat-input"),
    sendChatBtn: document.getElementById("send-chat-btn"),
    dashChatInput: document.getElementById("dashboard-chat-input"),
    dashSendChatBtn: document.getElementById("dashboard-send-chat-btn"),
    
    editorHost: document.getElementById("editor-host"),
    sourceCode: document.getElementById("source-code"),
    terminalContent: document.getElementById("terminal-content"),
    
    cursorPos: document.getElementById("editor-cursor-pos"),
    dirtyLabel: document.getElementById("dirty-label"),
    dirtyDot: document.getElementById("dirty-status-dot"),
    syntaxStatus: document.getElementById("syntax-status-label"),
    activePathBreadcrumb: document.getElementById("active-path-breadcrumb"),
    
    topRunBtn: document.getElementById("top-run-btn"),
    terminalActionCheck: document.getElementById("terminal-action-check"),
    clearTerminalBtn: document.getElementById("clear-terminal-btn")
  };
};

// Default course curriculum fallback
window.COURSE_CURRICULUM = [
  {
    conceptId: "variables-data",
    conceptTitle: "01. Variables & Types",
    summary: "Master value assignments, integers, floating structures, and mathematical traps.",
    lessons: [
      {
        id: "var-intro",
        title: "Variables (Intro)",
        level: "Beginner",
        minutes: 5,
        summary: "Understand how variables store values sequentially in memory.",
        objectives: [
          "Identify correct variable assignment directions",
          "Recognize how string literals are evaluated"
        ],
        blocks: [
          {
            heading: "Variables Concept",
            body: "A variable is like a named box. You define them using <code>=</code> in Python. Keep in mind: the variable name MUST reside on the left, and its value on the right!"
          }
        ],
        starter: "# Variables Assignment\n\"Ava\" = name  # Bug: variable name must be on the left!\nprint(f\"Hello {name}!\")\n"
      }
    ]
  },
  {
    conceptId: "control-flow",
    conceptTitle: "02. Control Flow",
    summary: "Direct sequential operations using branch conditions and loops.",
    lessons: [
      {
        id: "cf-conditionals",
        title: "Conditional Statements",
        level: "Beginner",
        minutes: 12,
        summary: "Implement logical branching structures with if/elif/else.",
        objectives: [
          "Master 4-space indentation scoping rules",
          "Trace conditional operators"
        ],
        blocks: [
          {
            heading: "Logical branching",
            body: "Conditions evaluate true or false states. Remember that Python strictly mandates 4 spaces of indentation inside branching blocks!"
          }
        ],
        starter: "# Conditional logic branching practice\nscore = 70\nif score > 70:  # Bug: Change > to >= to pass at 70!\n    print(\"Result: Pass\")\nelse:\n    print(\"Result: Fail\")\n"
      }
    ]
  }
];

window.escapeHtml = function(text) {
  if (text === undefined || text === null) return "";
  return text.toString()
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
};
