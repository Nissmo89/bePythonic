// AI Tutor Chat Operations
window.parseMarkdown = function(md) {
  if (!md) return "";
  let html = window.escapeHtml(md);
  
  // Custom python code blocks with sandbox insertion
  html = html.replace(/```python([\s\S]*?)```/g, (match, code) => {
    return `
      <div class="code-block-wrapper my-3 overflow-hidden border border-slate-200 bg-slate-950 font-mono text-xs text-slate-300" style="border-radius: 0px;">
        <div class="px-3 py-2 bg-slate-900 border-b border-slate-800 flex justify-between items-center text-[10px] text-slate-400 select-none">
          <span>python</span>
          <button onclick="copyCodeToSandbox(this)" class="text-indigo-400 hover:text-white transition-colors font-bold" data-code="${encodeURIComponent(code.trim())}">Insert to Editor</button>
        </div>
        <pre class="p-3 overflow-auto max-h-[250px] text-left select-text" style="border-radius: 0px;"><code>${code.trim()}</code></pre>
      </div>`;
  });
  
  // Custom general code blocks
  html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
    return `<pre class="my-3 p-3 overflow-auto border border-slate-800 bg-slate-900 text-left font-mono text-xs text-slate-300 select-text" style="border-radius: 0px;">${code.trim()}</pre>`;
  });
  
  // Inline code ticks
  html = html.replace(/`([^`\n]+)`/g, '<code class="px-1.5 py-0.5 border border-slate-200 text-indigo-600 font-mono text-xs" style="background-color: #f1f5f9; border-radius: 0px;">$1</code>');
  
  // Double newlines to paragraph tags
  html = html.replace(/\n\n/g, '</p><p class="mt-2 text-xs leading-relaxed select-text">');
  
  return `<p class="text-xs leading-relaxed select-text">${html}</p>`;
};

window.copyCodeToSandbox = function(btn) {
  const code = decodeURIComponent(btn.dataset.code);
  window.setCodeValue(code);
  window.appendTerminalOutput("System", "Injected Python code directly from AI Tutor into coding playground.");
};

window.appendTutorMessage = function(role, text) {
  window.state.chatHistory.push({ role, text });
  const isUser = role === "user";
  
  const mainContainer = document.getElementById("chat-messages-container");
  if (mainContainer) {
    const mainBubble = document.createElement("div");
    mainBubble.className = `chat-bubble ${isUser ? "user ml-auto shadow-sm" : "ai mr-auto"}`;
    mainBubble.innerHTML = `
      <div class="mb-1 flex items-center justify-between select-none">
        <span class="text-[10px] font-bold ${isUser ? "text-indigo-200" : "text-indigo-600"}">${isUser ? "You" : "AI Tutor"}</span>
      </div>
      ${isUser ? `<p class="text-xs leading-relaxed select-text">${window.escapeHtml(text)}</p>` : window.parseMarkdown(text)}`;
      
    mainContainer.appendChild(mainBubble);
    mainContainer.scrollTop = mainContainer.scrollHeight;
    
    if (window.gsap) {
      window.gsap.fromTo(mainBubble, { opacity: 0, y: 8, scale: 0.98 }, { opacity: 1, y: 0, scale: 1, duration: 0.15 });
    }
  }

  const dashContainer = document.getElementById("dashboard-chat-messages-container");
  if (dashContainer) {
    const dashBubble = document.createElement("div");
    dashBubble.className = `p-2.5 text-xs shadow-sm border ${isUser ? "bg-indigo-50 border-indigo-100 text-slate-800 ml-5" : "bg-slate-50 border-slate-200 text-slate-700 mr-5"}`;
    dashBubble.style.borderRadius = "0px";
    dashBubble.innerHTML = `
      <div class="flex items-center gap-1 select-none mb-0.5">
        <span class="text-[8px] font-bold uppercase tracking-wider ${isUser ? "text-indigo-600" : "text-indigo-500"}">${isUser ? "You" : "AI Tutor"}</span>
      </div>
      <div class="leading-relaxed select-text text-[11px]">${isUser ? window.escapeHtml(text) : window.parseMarkdown(text)}</div>`;
      
    dashContainer.appendChild(dashBubble);
    dashContainer.scrollTop = dashContainer.scrollHeight;
    
    if (window.gsap) {
      window.gsap.fromTo(dashBubble, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.15 });
    }
  }
};

window.quickTutorQuery = function(queryText) {
  document.getElementById("chat-input").value = "";
  window.appendTutorMessage("user", queryText);
  
  const combined = `${queryText}\n\n[Active Playground Code]\n\`\`\`python\n${window.getCodeValue()}\n\`\`\``;
  const payload = [
    ...window.state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })),
    { role: "user", text: combined }
  ];
  
  window.ui.chatInput.disabled = true;
  window.ui.sendChatBtn.disabled = true;
  window.ui.dashChatInput.disabled = true;
  window.ui.dashSendChatBtn.disabled = true;
  
  window.callBackend("askAiTutor", JSON.stringify(payload));
};

window.sendTutorChatMessage = function() {
  const val = window.ui.chatInput.value.trim();
  if (!val) return;
  window.ui.chatInput.value = "";
  window.appendTutorMessage("user", val);
  
  const combined = `${val}\n\n[Active Playground Code]\n\`\`\`python\n${window.getCodeValue()}\n\`\`\``;
  const payload = [
    ...window.state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })),
    { role: "user", text: combined }
  ];
  
  window.ui.chatInput.disabled = true;
  window.ui.sendChatBtn.disabled = true;
  window.ui.dashChatInput.disabled = true;
  window.ui.dashSendChatBtn.disabled = true;
  
  window.callBackend("askAiTutor", JSON.stringify(payload));
};

window.sendDashboardChatMessage = function() {
  const val = window.ui.dashChatInput.value.trim();
  if (!val) return;
  window.ui.dashChatInput.value = "";
  window.appendTutorMessage("user", val);
  
  const combined = `${val}\n\n[Active Playground Code]\n\`\`\`python\n${window.getCodeValue()}\n\`\`\``;
  const payload = [
    ...window.state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })),
    { role: "user", text: combined }
  ];
  
  window.ui.chatInput.disabled = true;
  window.ui.sendChatBtn.disabled = true;
  window.ui.dashChatInput.disabled = true;
  window.ui.dashSendChatBtn.disabled = true;
  
  window.callBackend("askAiTutor", JSON.stringify(payload));
};
