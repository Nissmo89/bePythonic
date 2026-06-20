// Application boots and event coordinators
window.switchMainTab = function(route) {
  window.state.currentPage = route;
  document.getElementById("page-view-home").classList.toggle("hidden", route !== "home");
  document.getElementById("page-view-lessons").classList.toggle("hidden", route !== "lessons");
  document.getElementById("page-view-playground").classList.toggle("hidden", route !== "playground");
  document.getElementById("page-view-tutor").classList.toggle("hidden", route !== "tutor");
  document.getElementById("page-view-explore").classList.toggle("hidden", route !== "explore");
  document.getElementById("page-view-settings").classList.toggle("hidden", route !== "settings");

  let pathText = "Overview";
  if (route === "home") pathText = "Profile & Stats Overview";
  if (route === "lessons") {
    let activeL = null;
    if (window.COURSE_CURRICULUM) {
      window.COURSE_CURRICULUM.forEach(c => {
        if (c.lessons) {
          const f = c.lessons.find(l => (l.lesson_id === window.state.currentLessonId || l.id === window.state.currentLessonId));
          if (f) activeL = f;
        }
      });
    }
    pathText = activeL ? `Lesson: ${activeL.title}` : "Structured Curriculum";
  }
  if (route === "playground") pathText = "Playground Editor";
  if (route === "tutor") pathText = "AI Chat Tutor";
  if (route === "explore") pathText = "Community Explore";
  if (route === "settings") pathText = "Platform Settings";
  window.ui.activePathBreadcrumb.textContent = pathText;

  document.querySelectorAll(".nav-tab").forEach(btn => {
    const isActive = btn.dataset.tab === route;
    btn.classList.toggle("active", isActive);
    if (isActive) {
      btn.classList.add("bg-indigo-50/15", "text-indigo-600");
      btn.classList.remove("text-slate-500", "hover:text-slate-900");
    } else {
      btn.classList.remove("bg-indigo-50/15", "text-indigo-600");
      btn.classList.add("text-slate-500", "hover:text-slate-900");
    }
  });
};

window.runCode = function() {
  window.appendTerminalOutput("System", "Transmitting Python script to local environment safe sandbox...");
  window.callBackend("runCode", window.getCodeValue());
};

window.runAstCheck = function() {
  window.appendTerminalOutput("System", "Submitting syntax parse structure to local AST validator...");
  window.callBackend("syntaxCheck", window.getCodeValue());
};

window.bindInteractiveUiEvents = function() {
  window.ui.enterStudioBtn.addEventListener("click", () => {
    if (window.gsap) {
      window.gsap.to(window.ui.welcomeScreen, {
        opacity: 0,
        duration: 0.35,
        onComplete: () => {
          window.ui.welcomeScreen.style.display = "none";
          window.ui.appShell.style.opacity = "1";
          window.switchMainTab("home");
        }
      });
    } else {
      window.ui.welcomeScreen.style.display = "none";
      window.ui.appShell.style.opacity = "1";
      window.switchMainTab("home");
    }
  });

  document.querySelectorAll(".nav-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      if (btn.dataset.tab) window.switchMainTab(btn.dataset.tab);
    });
  });

  window.ui.topRunBtn.addEventListener("click", window.runCode);
  window.ui.terminalActionCheck.addEventListener("click", window.runAstCheck);

  window.addEventListener("keydown", (e) => {
    if (e.key === "F5") {
      e.preventDefault();
      window.runCode();
    }
  });

  window.ui.clearTerminalBtn.addEventListener("click", () => {
    window.ui.terminalContent.innerHTML = "<div class='opacity-40 select-none'>Sandbox Console execution logs cleared.</div>";
  });

  window.ui.sendChatBtn.addEventListener("click", window.sendTutorChatMessage);
  window.ui.chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      window.sendTutorChatMessage();
    }
  });

  window.ui.dashSendChatBtn.addEventListener("click", window.sendDashboardChatMessage);
  window.ui.dashChatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      window.sendDashboardChatMessage();
    }
  });

  document.getElementById("workspace-action-open").addEventListener("click", () => {
    window.callBackend("openPythonFile");
  });
};

window.boot = function() {
  window.initUiReferences();
  window.initMonacoEditor();
  window.renderSyllabusList();
  window.renderDashboardRoadmap();
  window.bindInteractiveUiEvents();
  window.initQtBridgeConnection();
  
  window.appendTutorMessage("assistant", "Welcome to the conversational tutor chat! I'm here to clarify complicated error messages, quiz your comprehension of variables or arrays, and offer hints for lesson exercises. Ask me any question below!");

  setTimeout(() => {
    window.initActivityChart();
  }, 300);
  
  if (window.gsap) {
    window.gsap.to(window.ui.welcomeScreen, { opacity: 1, duration: 0.35 });
  }
};

document.addEventListener("DOMContentLoaded", () => {
  window.boot();
});
