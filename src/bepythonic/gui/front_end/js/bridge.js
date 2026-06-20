// Qt QWebChannel bridge integration
window.callBackend = function(methodName, ...args) {
  if (!window.state.backend || typeof window.state.backend[methodName] !== "function") {
    window.appendTerminalOutput("Warn", `Backend is offline in browser preview mode: ${methodName}`);
    return;
  }
  window.state.backend[methodName](...args);
};

window.appendTerminalOutput = function(kind, message) {
  const container = window.ui.terminalContent;
  const row = document.createElement("div");
  row.className = "py-0.5 border-b border-slate-900/10";
  const stamp = new Date().toLocaleTimeString();
  
  let colorClass = "text-emerald-400"; // Default: stdout or success
  if (kind.toLowerCase() === "error") colorClass = "text-rose-400 font-bold";
  if (kind.toLowerCase() === "warn") colorClass = "text-amber-500 font-bold";
  if (kind.toLowerCase() === "ast check") colorClass = "text-indigo-400 font-bold";
  
  row.innerHTML = `
    <span class="opacity-30 select-none">[${stamp}]</span> 
    <span class="${colorClass}">${kind}:</span> 
    <span class="select-text text-slate-300">${window.escapeHtml(message)}</span>`;
    
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
};

window.appendLessonTerminalOutput = function(kind, message) {
  const container = document.getElementById("lesson-console-pane");
  const outputShell = document.getElementById("lesson-inline-output-shell");
  if (!container) return;
  if (outputShell) outputShell.classList.add("show");
  const emptyState = container.querySelector(".lesson-sol-console-empty");
  if (emptyState) emptyState.remove();
  const row = document.createElement("div");
  row.className = "lesson-sol-console-row";
  const stamp = new Date().toLocaleTimeString();
  const normalizedKind = (kind || "").toLowerCase();

  let kindClass = "lesson-sol-console-kind lesson-sol-console-kind--stdout";
  if (normalizedKind === "error") kindClass = "lesson-sol-console-kind lesson-sol-console-kind--error";
  if (normalizedKind === "warn") kindClass = "lesson-sol-console-kind lesson-sol-console-kind--warn";
  if (normalizedKind === "system") kindClass = "lesson-sol-console-kind lesson-sol-console-kind--system";
  if (normalizedKind === "ast check") kindClass = "lesson-sol-console-kind lesson-sol-console-kind--ast";

  row.innerHTML = `
    <span class="lesson-sol-console-stamp">[${stamp}]</span>
    <span class="${kindClass}">${window.escapeHtml(kind)}:</span>
    <span class="lesson-sol-console-message">${window.escapeHtml(message)}</span>`;
    
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
};

window.handleBridgeEvent = function(eventName, rawPayload) {
  let payload = {};
  try {
    payload = JSON.parse(rawPayload);
  } catch(e) {}

  switch(eventName) {
    case "bridge:ready":
      window.ui.bridgeStatus.textContent = "Connected";
      window.ui.bridgeDot.style.backgroundColor = "#32d74b"; // Lime Green
      window.appendTerminalOutput("System", "Native Python API bridge active.");
      // Load course catalog on startup
      window.callBackend("getCourseCatalog");
      break;
      
    case "catalog:loaded":
      if (payload.ok && payload.catalog) {
        window.COURSE_CURRICULUM = payload.catalog.modules;
        window.renderSyllabusList();
        // Request progress load
        window.callBackend("loadProgress");
      } else {
        window.appendTerminalOutput("Error", `Failed to load catalog: ${payload.message || "Unknown error"}`);
      }
      break;
      
    case "lesson:loaded":
      if (payload.ok && payload.lesson) {
        window.loadLessonContent(payload.lesson);
      } else {
        window.appendTerminalOutput("Error", `Failed to load lesson: ${payload.message || "Unknown error"}`);
      }
      break;
      
    case "progress:loaded":
      if (payload.ok) {
        window.state.completedLessons = new Set(payload.completed_lessons || []);
        window.state.currentLessonId = payload.current_lesson || null;
        window.state.currentLessonPageIndex = payload.current_page || 0;
        
        if (window.renderDashboardRoadmap) window.renderDashboardRoadmap();
        if (window.updateDashboardStats) window.updateDashboardStats();
        
        // Auto-select lesson on load to resume progress
        if (window.state.currentLessonId) {
          window.selectLesson(window.state.currentLessonId, true);
        }
      }
      break;
      
    case "progress:saved":
      if (window.updateDashboardStats) window.updateDashboardStats();
      break;
      
    case "lesson:loading":
      window.appendTerminalOutput("System", "AI is synthesizing a new curriculum module...");
      break;
      
    case "lesson:success":
      try {
        const newConcept = JSON.parse(payload.lesson);
        // Make custom concept match backend structure format
        const formattedModule = {
          module_id: "custom_" + Date.now(),
          title: "Custom generated: " + newConcept.conceptTitle,
          lessons: newConcept.lessons.map(l => ({
            lesson_id: l.id,
            title: l.title,
            module_id: "custom",
            module_title: "Custom Curriculum"
          }))
        };
        window.COURSE_CURRICULUM.push(formattedModule);
        window.renderSyllabusList();
        
        // Save pages locally in memory for custom loading
        window.state.customLessons = window.state.customLessons || {};
        newConcept.lessons.forEach(l => {
          window.state.customLessons[l.id] = {
            lesson_id: l.id,
            title: l.title,
            module_title: "Custom Curriculum",
            estimated_minutes: l.minutes || 5,
            topics: [newConcept.conceptTitle],
            pages: [
              {
                page_id: "p1",
                title: "Concept Introduction",
                page_type: "theory",
                content: l.summary + "\n\n" + l.blocks.map(b => `### ${b.heading}\n${b.body}`).join("\n\n")
              },
              {
                page_id: "p2",
                title: "Practice Exercise",
                page_type: "code_example",
                content: "Run and repair the custom program below.",
                code: l.starter
              }
            ]
          };
        });
        
        window.selectLesson(newConcept.lessons[0].id);
        window.appendTerminalOutput("System", `Successfully generated custom lesson: ${newConcept.conceptTitle}`);
      } catch(e) {
        window.appendTerminalOutput("Error", "Failed to parse generated lesson JSON.");
      }
      break;
      
    case "lesson:error":
      const btn = document.getElementById("ai-lesson-generate-btn");
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Generate Lesson Module";
      }
      const progressDiv = document.getElementById("ai-lesson-progress");
      if (progressDiv) progressDiv.classList.add("hidden");
      window.appendTerminalOutput("Error", payload.message || "Failed to generate lesson.");
      break;

    case "tutor:response":
      window.ui.chatInput.disabled = false;
      window.ui.sendChatBtn.disabled = false;
      window.ui.dashChatInput.disabled = false;
      window.ui.dashSendChatBtn.disabled = false;
      
      const lessonTutorInput = document.getElementById("lesson-tutor-input");
      if (lessonTutorInput) lessonTutorInput.disabled = false;
      
      if (payload.text) {
        if (window.state.tutorRequestSource === "lesson") {
          window.appendLessonTutorMessage("assistant", payload.text);
        } else {
          window.appendTutorMessage("assistant", payload.text);
        }
      }
      break;

    case "tutor:error":
      window.ui.chatInput.disabled = false;
      window.ui.sendChatBtn.disabled = false;
      window.ui.dashChatInput.disabled = false;
      window.ui.dashSendChatBtn.disabled = false;
      
      const lessonTutorInputErr = document.getElementById("lesson-tutor-input");
      if (lessonTutorInputErr) lessonTutorInputErr.disabled = false;
      
      if (window.state.tutorRequestSource === "lesson") {
        window.appendLessonTerminalOutput("Error", payload.message || "Tutor response failed.");
        window.appendLessonTutorMessage("assistant", "I encountered an error analyzing that query.");
      } else {
        window.appendTerminalOutput("Error", payload.message || "Tutor response failed.");
        window.appendTutorMessage("assistant", "I encountered an error analyzing that query.");
      }
      break;

    case "run:result":
      if (window.state.runRequestSource === "lesson") {
        if (payload.ok) {
          window.appendLessonTerminalOutput("Stdout", payload.stdout || "Process executed successfully.");
        } else {
          if (payload.stdout) {
            window.appendLessonTerminalOutput("Stdout", payload.stdout);
          }
          window.appendLessonTerminalOutput("Error", payload.stderr || "Process closed with failures.");
        }
      } else {
        if (payload.ok) {
          window.appendTerminalOutput("Stdout", payload.stdout || "Process executed successfully.");
        } else {
          if (payload.stdout) {
            window.appendTerminalOutput("Stdout", payload.stdout);
          }
          window.appendTerminalOutput("Error", payload.stderr || "Process closed with failures.");
        }
      }
      break;

    case "syntax:result":
      if (payload.ok) {
        window.ui.syntaxStatus.textContent = "No Syntax Errors";
        window.ui.syntaxStatus.className = "text-emerald-600 font-bold";
        window.appendTerminalOutput("AST Check", payload.message);
      } else {
        window.ui.syntaxStatus.textContent = "Syntax Error";
        window.ui.syntaxStatus.className = "text-rose-600 font-bold";
        window.appendTerminalOutput("AST Error", payload.message);
      }
      break;

    case "file:opened":
      window.setCodeValue(payload.code || "");
      window.switchMainTab("playground");
      window.appendTerminalOutput("System", `Loaded open Python file: ${payload.name}`);
      break;
      
    case "file:saved":
      window.setDirty(false);
      window.appendTerminalOutput("System", `Saved file: ${payload.name}`);
      break;
      
    case "file:error":
      window.appendTerminalOutput("Error", `IO error: ${payload.message}`);
      break;
  }
};

window.ensureQtWebChannel = function() {
  if (window.QWebChannel) {
    return Promise.resolve(true);
  }

  const isQtWebEngine =
    Boolean(window.qt && window.qt.webChannelTransport) ||
    navigator.userAgent.includes("QtWebEngine");

  if (!isQtWebEngine) {
    return Promise.resolve(false);
  }

  if (window.state.qwebChannelPromise) {
    return window.state.qwebChannelPromise;
  }

  window.state.qwebChannelPromise = new Promise((resolve) => {
    const existing = document.querySelector('script[data-qwebchannel-loader="true"]');
    if (existing) {
      existing.addEventListener("load", () => resolve(Boolean(window.QWebChannel)), { once: true });
      existing.addEventListener("error", () => resolve(false), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.src = "qrc:///qtwebchannel/qwebchannel.js";
    script.dataset.qwebchannelLoader = "true";
    script.onload = () => resolve(Boolean(window.QWebChannel));
    script.onerror = () => resolve(false);
    document.head.appendChild(script);
  });

  return window.state.qwebChannelPromise;
};

window.initQtBridgeConnection = async function() {
  const hasQWebChannel = await window.ensureQtWebChannel();

  if (!hasQWebChannel || !window.qt || !window.qt.webChannelTransport) {
    window.ui.bridgeStatus.textContent = "Preview Mode";
    window.ui.bridgeDot.style.backgroundColor = "#f5c518"; // Thunder Yellow
    window.appendTerminalOutput("Warn", "Connected in browser preview sandbox.");
    
    // Initialize dummy catalog for browser preview
    window.COURSE_CURRICULUM = [
      {
        module_id: "getting_started",
        title: "Getting Started",
        lessons: [
          { lesson_id: "what_is_python", title: "What is Python?", module_title: "Getting Started" },
          { lesson_id: "first_program", title: "Your First Program", module_title: "Getting Started" }
        ]
      }
    ];
    window.renderSyllabusList();
    return;
  }
  
  new QWebChannel(window.qt.webChannelTransport, (channel) => {
    window.state.backend = channel.objects.backend || null;
    if (!window.state.backend) {
      window.ui.bridgeStatus.textContent = "Bridge Offline";
      window.ui.bridgeDot.style.backgroundColor = "#ef4444";
      return;
    }
    
    if (window.state.backend.bridgeEvent) {
      window.state.backend.bridgeEvent.connect(window.handleBridgeEvent);
    }
    
    window.ui.bridgeStatus.textContent = "Connected";
    window.ui.bridgeDot.style.backgroundColor = "#32d74b"; // Lime Green
    
    if (typeof window.state.backend.ready === "function") {
      window.state.backend.ready();
    }
  });
};
