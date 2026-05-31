# ruff: noqa: E501
"""Dashboard/lessons page rendered inside QWebEngineView for a premium Python Learning Platform with dedicated Profile & Stats page and AI Lesson Generator."""

EDITOR_HTML = r"""
<!doctype html>
<html class="h-full" lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>bePythonic Learning Platform</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Space Grotesk"', '"Segoe UI"', 'sans-serif'],
            mono: ['"IBM Plex Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
          },
          colors: {
            learning: {
              primary: "#4f46e5",
              secondary: "#6366f1",
              bg: "#f8fafc",
              border: "#e2e8f0",
              text: "#0f172a",
              muted: "#475569",
              success: "#10b981",
              warning: "#f59e0b",
              error: "#ef4444"
            }
          }
        }
      }
    };
  </script>

  <link rel="stylesheet" data-name="vs/editor/editor.main" href="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs/editor/editor.main.min.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs/loader.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="qrc:///qtwebchannel/qwebchannel.js"></script>

  <style>
    :root {
      --bg-color: #f8fafc;
      --bar-bg: rgba(255, 255, 255, 0.75);
      --editor-bg: #ffffff;
      --border-color: rgba(226, 232, 240, 0.8);
      --text-color: #0f172a;
      --muted-color: #475569;
    }

    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(148, 163, 184, 0.3);
      border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(148, 163, 184, 0.5);
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }

    body {
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: "Space Grotesk", sans-serif;
      background-color: var(--bg-color);
      color: var(--text-color);
      background-image: 
        radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.03) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.03) 0px, transparent 50%);
    }

    /* True Glassmorphism overlay panels */
    .glass-nav {
      background: var(--bar-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
    }

    .glass-card {
      background: rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(226, 232, 240, 0.8);
      box-shadow: 0 4px 30px rgba(15, 23, 42, 0.02);
    }

    /* Tactile controls */
    .btn-tactile-primary {
      background: #4f46e5;
      color: #ffffff;
      border: 1px solid rgba(79, 70, 229, 0.4);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 1px 2px rgba(15, 23, 42, 0.05);
      transition: all 0.15s ease-in-out;
    }
    .btn-tactile-primary:hover {
      background: #4338ca;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 2px 4px rgba(15, 23, 42, 0.08);
      transform: translateY(-0.5px);
    }
    .btn-tactile-primary:active {
      background: #3730a3;
      transform: translateY(0.5px);
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15);
    }

    .btn-tactile-secondary {
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(6px);
      color: #0f172a;
      border: 1px solid #e2e8f0;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
      transition: all 0.15s ease-in-out;
    }
    .btn-tactile-secondary:hover {
      background: rgba(248, 250, 252, 0.98);
      border-color: #cbd5e1;
      transform: translateY(-0.5px);
    }
    .btn-tactile-secondary:active {
      transform: translateY(0.5px);
      background: #f1f5f9;
    }

    .nav-tab {
      transition: all 0.15s ease-in-out;
    }
    .nav-tab.active {
      background-color: rgba(79, 70, 229, 0.07);
      color: #4f46e5;
      border: 1px solid rgba(79, 70, 229, 0.12);
    }

    /* Premium AI Chat Bubble design */
    .chat-bubble {
      max-width: 80%;
      border-radius: 12px;
      padding: 10px 14px;
      line-height: 1.5;
    }
    .chat-bubble.user {
      background-color: #4f46e5;
      color: #ffffff;
      border-bottom-right-radius: 2px;
      align-self: flex-end;
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.15);
    }
    .chat-bubble.ai {
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      color: var(--text-color);
      border-bottom-left-radius: 2px;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
      align-self: flex-start;
    }

    #editor-host {
      width: 100%;
      height: 100%;
      overflow: hidden;
      border: 1px solid var(--border-color);
      border-radius: 8px;
    }
  </style>
</head>
<body class="h-full bg-slate-50 text-slate-900 antialiased overflow-hidden select-none">

  <!-- Welcome Page -->
  <section id="welcome-screen" class="welcome-screen">
    <div class="max-w-md w-full mx-4 p-8 rounded-2xl border border-slate-200 bg-white/80 backdrop-blur-xl shadow-xl text-center">
      <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center rounded-2xl bg-indigo-50 border border-indigo-100 text-indigo-600">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.62 48.62 0 0112 20.904a48.62 48.62 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 018.75 5.841c-.893.233-1.782.507-2.658.814m-15.482 0a50.58 50.58 0 003.528 7.643m11.954-7.643a50.58 50.58 0 013.528 7.643m-14.73 1.579a48.514 48.514 0 004.91 5.922m7.41-5.922a48.514 48.514 0 014.91 5.922M12 10.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"></path>
        </svg>
      </div>
      <h1 class="text-2xl font-bold tracking-tight text-slate-900 mb-1">bePythonic</h1>
      <p class="text-xs font-semibold tracking-widest text-indigo-600 uppercase mb-4">Python Learning Companion</p>
      <p class="text-slate-500 mb-8 text-xs leading-relaxed max-w-sm mx-auto">
        Step into an interactive, beautifully structured local course sandbox with Gemini-powered debugging tutors.
      </p>
      
      <button id="enter-studio-btn" class="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-semibold text-white transition-all transform hover:scale-[1.01] active:scale-[0.99] shadow-md">
        Start Learning Python
      </button>
      <div class="text-[10px] text-slate-400 font-mono mt-4">Local host offline learning platform</div>
    </div>
  </section>

  <!-- Complete Workspace Shell with Top Bar Navigation -->
  <div id="app-shell" class="h-full flex flex-col opacity-0 overflow-hidden" style="background-color: var(--bg-color);">
    
    <!-- Unified Top Navigation Bar (Sleek Glassmorphism Style) -->
    <nav class="h-14 glass-nav flex items-center justify-between px-6 shrink-0 select-none z-40">
      
      <!-- Left side: Platform identity and bridge status -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-xl">🎓</span>
          <span class="text-base font-bold bg-gradient-to-r from-indigo-600 to-indigo-400 bg-clip-text text-transparent">bePythonic</span>
        </div>
        <div class="h-4 w-px bg-slate-200"></div>
        <div class="flex items-center gap-1.5 bg-white/60 border border-slate-100 rounded-lg px-2.5 py-1">
          <span class="w-1.5 h-1.5 rounded-full" id="bridge-dot" style="background-color: #ef4444;"></span>
          <span class="text-[9px] font-mono font-bold text-slate-500 uppercase tracking-wider" id="bridge-status">Connecting...</span>
        </div>
      </div>

      <!-- Center: Navigation Tabs (Expanded UX) -->
      <div class="flex items-center gap-1.5 select-none bg-slate-100/50 p-1 rounded-xl border border-slate-200/50">
        <button class="nav-tab active flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold" data-tab="home">
          <span>👤</span>
          <span>Profile & Stats</span>
        </button>
        <button class="nav-tab flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900" data-tab="lessons">
          <span>📚</span>
          <span>Curriculum</span>
        </button>
        <button class="nav-tab flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900" data-tab="playground">
          <span>💻</span>
          <span>Playground</span>
        </button>
        <button class="nav-tab flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900" data-tab="tutor">
          <span>💬</span>
          <span>AI Tutor Chat</span>
        </button>
        <button class="nav-tab flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900" data-tab="explore">
          <span>🌐</span>
          <span>Explore</span>
        </button>
        <button class="nav-tab flex items-center gap-1.5 px-4.5 py-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-slate-900" data-tab="settings">
          <span>⚙️</span>
          <span>Settings</span>
        </button>
      </div>

      <!-- Right side: Streak -->
      <div class="flex items-center gap-4">
        <div class="bg-amber-50 border border-amber-100 text-amber-700 font-bold text-[10px] px-3 py-1 rounded-xl flex items-center gap-1 select-none">
          <span>🔥</span>
          <span><span id="topbar-streak-counter">3</span> Day Streak</span>
        </div>
        <div class="text-[10px] font-mono text-slate-400" id="active-path-breadcrumb">Profile & Stats Overview</div>
      </div>
    </nav>

    <!-- Workspace Subpages Views -->
    <div class="flex-1 min-h-0 relative z-30">

      <!-- View A: Profile & Stats Page -->
      <div class="absolute inset-0 overflow-y-auto p-6 space-y-6" id="page-view-home">
        <div class="max-w-6xl mx-auto space-y-6">
          
          <header class="p-6 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="text-[10px] font-mono font-bold text-indigo-600 uppercase tracking-wider">Student Portfolio Ledger</div>
              <h2 class="text-2xl font-bold tracking-tight text-slate-900">Coder Profile & Statistics</h2>
              <p class="text-xs text-slate-500 leading-relaxed max-w-lg">
                Track your active learning milestones, coding frequencies, resolved compiler errors, and unlocked achievements in one centralized workspace.
              </p>
            </div>
            <button class="py-2 px-4 rounded-xl btn-tactile-primary text-xs font-semibold shrink-0" onclick="switchMainTab('lessons')">
              Open Python Syllabus
            </button>
          </header>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="p-4 rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur flex flex-col gap-1 shadow-sm">
              <div class="text-[9px] font-mono uppercase tracking-wider text-slate-400">LESSONS COMPLETED</div>
              <div class="text-lg font-bold text-slate-800"><span id="stats-lessons">2</span> / 7</div>
            </div>
            <div class="p-4 rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur flex flex-col gap-1 shadow-sm">
              <div class="text-[9px] font-mono uppercase tracking-wider text-slate-400">ACTIVE STREAK</div>
              <div class="text-lg font-bold text-slate-800">3 Days 🔥</div>
            </div>
            <div class="p-4 rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur flex flex-col gap-1 shadow-sm">
              <div class="text-[9px] font-mono uppercase tracking-wider text-slate-400">DRILLS RESOLVED</div>
              <div class="text-lg font-bold text-slate-800">12 Bugfixes</div>
            </div>
            <div class="p-4 rounded-xl border border-slate-200/60 bg-white/60 backdrop-blur flex flex-col gap-1 shadow-sm">
              <div class="text-[9px] font-mono uppercase tracking-wider text-slate-400">AI TUTOR CHATS</div>
              <div class="text-lg font-bold text-slate-800">24 Queries</div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div class="lg:col-span-2 space-y-6">
              
              <!-- Weekly Analytics Graph (Interactive Chart.js line graph) -->
              <div class="p-6 rounded-2xl glass-card space-y-4">
                <div class="flex items-center justify-between">
                  <div class="space-y-0.5">
                    <span class="text-[9px] font-mono font-bold text-indigo-600 uppercase tracking-wider">Learning Performance</span>
                    <h3 class="text-sm font-bold text-slate-800">Weekly Coding Activity Analytics</h3>
                  </div>
                  <div class="flex items-center gap-2 select-none">
                    <span class="px-2 py-0.5 rounded bg-indigo-50 border border-indigo-100 text-indigo-600 text-[10px] font-bold">Accuracy: 89%</span>
                    <span class="px-2 py-0.5 rounded bg-emerald-50 border border-emerald-100 text-emerald-600 text-[10px] font-bold">+2.4 hrs today</span>
                  </div>
                </div>
                
                <div class="relative w-full border border-slate-100 bg-slate-50/40 rounded-xl p-3 h-48">
                  <canvas id="activity-chart"></canvas>
                </div>
              </div>

              <!-- Structured Visual Learning Tree Roadmap -->
              <div class="p-6 rounded-2xl glass-card space-y-4" id="dashboard-roadmap-container">
                <!-- Dynamically populated timeline -->
              </div>
              
            </div>

            <div class="space-y-6">
              
              <!-- Unlocked Achievements Badges Ledger -->
              <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/60 backdrop-blur shadow-sm space-y-4">
                <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider select-none">Unlocked Achievements</h3>
                <div class="grid grid-cols-2 gap-3 select-none">
                  <div class="p-3 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col gap-1 items-center text-center">
                    <span class="text-3xl">🎓</span>
                    <span class="text-xs font-bold text-slate-800 block truncate w-full">First Variable</span>
                    <span class="text-[8px] text-slate-400 font-medium">Declared memory blocks</span>
                  </div>
                  <div class="p-3 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col gap-1 items-center text-center">
                    <span class="text-3xl">🛡️</span>
                    <span class="text-xs font-bold text-slate-800 block truncate w-full">AST Guardian</span>
                    <span class="text-[8px] text-slate-400 font-medium">Passed strict parse syntax</span>
                  </div>
                  <div class="p-3 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col gap-1 items-center text-center">
                    <span class="text-3xl">💬</span>
                    <span class="text-xs font-bold text-slate-800 block truncate w-full">Companion</span>
                    <span class="text-[8px] text-slate-400 font-medium">Consulted AI 5 times</span>
                  </div>
                  <div class="p-3 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col gap-1 items-center text-center opacity-40">
                    <span class="text-3xl">🔥</span>
                    <span class="text-xs font-bold text-slate-800 block truncate w-full">Loop Master</span>
                    <span class="text-[8px] text-slate-400 font-medium">Break infinite evaluations</span>
                  </div>
                </div>
              </div>

              <!-- Active Platform / Sandbox Statistics Ledger -->
              <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/60 backdrop-blur shadow-sm space-y-4">
                <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider select-none">Compiler & Sandbox Statistics</h3>
                <div class="space-y-3 font-mono text-[10px] text-slate-500">
                  <div class="flex justify-between border-b pb-1.5">
                    <span>Syntax check validator</span>
                    <span class="text-indigo-600 font-semibold">Active</span>
                  </div>
                  <div class="flex justify-between border-b pb-1.5">
                    <span>Weekly solved rate</span>
                    <span class="text-indigo-600 font-semibold">7 drills/wk</span>
                  </div>
                  <div class="flex justify-between border-b pb-1.5">
                    <span>Subprocess environment</span>
                    <span class="text-emerald-500 font-semibold">Healthy</span>
                  </div>
                  <div class="flex justify-between border-b pb-1.5">
                    <span>Sandbox execution limits</span>
                    <span class="text-emerald-500 font-semibold">5s Enforced</span>
                  </div>
                </div>
              </div>

              <!-- Real AI Tutor Chat Widget on Dashboard -->
              <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/60 backdrop-blur shadow-sm space-y-3 flex flex-col h-80">
                <div class="flex items-center justify-between shrink-0 select-none">
                  <div class="flex items-center gap-1.5">
                    <span class="text-indigo-600">💬</span>
                    <span class="text-sm font-bold text-slate-800">Tutor Dialogue Preview</span>
                  </div>
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                </div>
                
                <div class="flex-1 overflow-y-auto space-y-2.5 p-1 select-text" id="dashboard-chat-messages-container">
                </div>
                
                <div class="flex gap-2 shrink-0 pt-1.5 border-t">
                  <label class="sr-only" for="dashboard-chat-input">Tutor Message Quick</label>
                  <input type="text" id="dashboard-chat-input" placeholder="Type quick query..." class="flex-1 p-2 rounded-lg border border-slate-200 text-xs bg-slate-50 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                  <button id="dashboard-send-chat-btn" class="px-3 rounded-lg btn-tactile-primary text-xs font-semibold">Send</button>
                </div>
              </div>

            </div>

          </div>

        </div>
      </div>

      <!-- View B: Interactive Course Modules (Curriculum + AI Engine) -->
      <div class="absolute inset-0 flex min-h-0 hidden" id="page-view-lessons">
        
        <!-- Left Column Sidebar: Course outline selection grouped by Accordions -->
        <aside class="w-64 border-r bg-white/70 backdrop-blur-md flex flex-col shrink-0 overflow-hidden" style="border-color: var(--border-color);">
          <div class="p-3 border-b flex items-center justify-between bg-slate-50/50" style="border-color: var(--border-color);">
            <span class="text-[10px] font-mono font-bold text-slate-500 tracking-wider">CURRICULUM</span>
            <span class="px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-600 text-[10px] font-bold" id="lessons-count-badge">0</span>
          </div>
          <div class="flex-1 overflow-y-auto p-3 space-y-4" id="lessons-list-sidebar">
            <!-- Dynamically populated concept blocks and lessons -->
          </div>
          <!-- AI Generator CTA in sidebar -->
          <div class="p-3 border-t bg-slate-50" style="border-color: var(--border-color);">
            <button class="w-full py-2 px-4 rounded-xl btn-tactile-secondary text-xs font-semibold flex items-center justify-center gap-1.5 text-indigo-600" onclick="showAiLessonGenerator()">
              <span>✨</span> Generate Lesson
            </button>
          </div>
        </aside>

        <!-- Right Main Column: Unified lesson reading panel -->
        <div class="flex-1 flex flex-col bg-white min-h-0 overflow-y-auto">
          <div class="max-w-3xl mx-auto p-8 w-full select-text" id="lessons-detail-container">
            <div class="flex flex-col items-center justify-center h-full text-center space-y-4 mt-20 opacity-60">
              <span class="text-4xl">📚</span>
              <p class="text-sm font-medium">Select a course module from the left sidebar catalog to begin reading.</p>
            </div>
          </div>
        </div>

      </div>

      <!-- View C: Dedicated Spacing Playground Editor (Separate Workspace) -->
      <div class="absolute inset-0 flex min-h-0 hidden" id="page-view-playground">
        
        <div class="w-72 border-r bg-white/70 backdrop-blur-md flex flex-col shrink-0 overflow-hidden" style="border-color: var(--border-color);">
          <div class="p-3 border-b bg-slate-50/50" style="border-color: var(--border-color);">
            <span class="text-[10px] font-mono font-bold text-slate-500 tracking-wider">ACTIVE DRILL TASK</span>
          </div>
          <div class="p-4 space-y-4 flex-1 overflow-y-auto select-text">
            <h3 class="text-sm font-bold text-slate-800" id="playground-instructions-title">Custom Sandbox Playground</h3>
            <div id="playground-instructions-body" class="space-y-3">
              <p class="text-xs text-slate-500 leading-relaxed font-medium">
                You are in the free coding sandbox. You can open external python scripts, write random functions, check syntax, and execute processes.
              </p>
              <div class="p-3.5 rounded-xl border border-slate-100 bg-slate-50/50 text-[11px] leading-relaxed text-slate-600">
                🚀 To practice a specific curriculum topic, head to the <strong>Curriculum</strong> tab, select a module, and click <strong>🚀 Practice in Playground</strong> to inject its broken code here.
              </div>
            </div>
          </div>
        </div>

        <div class="flex-1 flex flex-col bg-slate-50 min-h-0">
          <div class="h-10 flex items-center justify-between border-b px-4 shrink-0 bg-white" style="border-color: var(--border-color);">
            <div class="flex items-center gap-1.5 font-mono text-[11px] text-slate-700 select-none">
              <svg class="w-3.5 h-3.5 text-indigo-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" /></svg>
              <span class="font-semibold">practice_playground.py</span>
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-500" id="dirty-status-dot"></span>
            </div>
            
            <div class="flex items-center gap-2 select-none">
              <button class="py-1 px-2.5 rounded btn-tactile-secondary text-[11px] font-semibold" id="workspace-action-open" title="Open .py File">
                Open File
              </button>
              <button class="py-1 px-3 rounded btn-tactile-primary text-[11px] font-semibold" id="top-run-btn">
                Run Challenge (F5)
              </button>
            </div>
          </div>

          <div class="flex-1 p-4 flex flex-col min-h-0 relative">
            <div class="flex-1 min-h-0">
              <div id="editor-host"></div>
              <textarea id="source-code" spellcheck="false"></textarea>
            </div>

            <div class="h-48 mt-3 flex flex-col rounded-xl border border-slate-200 bg-white overflow-hidden shrink-0 shadow-sm">
              <div class="h-8 border-b px-3 flex items-center justify-between select-none shrink-0 bg-slate-50">
                <span class="text-[9px] font-mono font-bold text-slate-500">SANDBOX OUTPUT CONSOLE</span>
                
                <div class="flex items-center gap-2">
                  <button class="opacity-70 hover:opacity-100 p-0.5 rounded text-indigo-600" id="terminal-action-check" title="Run AST Syntax Check">
                    <span class="text-[10px] font-bold font-mono">AST CHECK</span>
                  </button>
                  <button class="opacity-70 hover:opacity-100 p-0.5 rounded text-slate-400 hover:text-slate-600" id="clear-terminal-btn" title="Clear logs">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </div>
              </div>
              <div class="flex-1 overflow-auto p-3 font-mono text-[11px] bg-slate-950 text-slate-200" id="terminal-content">
                <div class="opacity-40 select-none">Execution stdout / stderr appear here...</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- View D: Full page AI Tutor Chat Companion -->
      <div class="absolute inset-0 flex min-h-0 hidden bg-white" id="page-view-tutor">
        <aside class="w-64 border-r bg-white/70 backdrop-blur-md flex flex-col shrink-0 overflow-hidden" style="border-color: var(--border-color);">
          <div class="p-3 border-b bg-slate-50/50" style="border-color: var(--border-color);">
            <span class="text-[10px] font-mono font-bold text-slate-500 tracking-wider">TUTOR PROMPTS</span>
          </div>
          <div class="p-3 space-y-2.5 flex-1 overflow-y-auto">
            <button class="w-full text-left p-3 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex flex-col gap-1 shadow-sm" onclick="quickTutorQuery('Explain indentation in Python and why it is mandatory.')">
              <span class="text-[11px] font-bold text-indigo-600 font-sans">🔑 Indentation Syntax</span>
              <span class="text-[9px] text-slate-400 leading-normal font-sans font-medium">Learn block indent rules</span>
            </button>
            <button class="w-full text-left p-3 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex flex-col gap-1 shadow-sm" onclick="quickTutorQuery('What does NameError mean and how do I solve it?')">
              <span class="text-[11px] font-bold text-indigo-600 font-sans">⚠️ Trace NameError</span>
              <span class="text-[9px] text-slate-400 leading-normal font-sans font-medium">Spot local scoping issues</span>
            </button>
            <button class="w-full text-left p-3 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex flex-col gap-1 shadow-sm" onclick="quickTutorQuery('Explain variables and integers like I am five.')">
              <span class="text-[11px] font-bold text-indigo-600 font-sans">🧠 Simplified Variables</span>
              <span class="text-[9px] text-slate-400 leading-normal font-sans font-medium">Trace values containers</span>
            </button>
            <button class="w-full text-left p-3 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex flex-col gap-1 shadow-sm" onclick="quickTutorQuery('Give me a 5-question multiple choice quiz on Python basic loops!')">
              <span class="text-[11px] font-bold text-indigo-600 font-sans">📝 Loops sequence quiz</span>
              <span class="text-[9px] text-slate-400 leading-normal font-sans font-medium">Test logic progression</span>
            </button>
          </div>
        </aside>

        <div class="flex-1 flex flex-col min-h-0 bg-slate-50/40">
          <div class="flex-1 overflow-y-auto p-6 space-y-4 flex flex-col min-h-0" id="chat-messages-container"></div>
          <div class="p-2.5 border-t flex flex-wrap gap-1.5 bg-white/70 backdrop-blur-md shrink-0" style="border-color: var(--border-color);">
            <button class="py-1 px-2.5 rounded-lg btn-tactile-secondary text-[10px] font-semibold" onclick="quickTutorQuery('Give me a simple code hint based on my current coding editor session.')">💡 Hint on Code</button>
            <button class="py-1 px-2.5 rounded-lg btn-tactile-secondary text-[10px] font-semibold" onclick="quickTutorQuery('Explain what is wrong with the code currently loaded in my editor.')">🔍 Analyze Bug</button>
          </div>
          <div class="p-3 border-t flex gap-2 bg-white shrink-0" style="border-color: var(--border-color);">
            <label class="sr-only" for="chat-input">Tutor Message</label>
            <input type="text" id="chat-input" placeholder="Ask your Python tutor anything... (e.g. explain lists, quiz me)" class="flex-1 p-2.5 rounded-xl text-xs border border-slate-200 bg-slate-50 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
            <button id="send-chat-btn" class="px-4.5 rounded-xl btn-tactile-primary text-xs font-semibold">Send Message</button>
          </div>
        </div>
      </div>

      <!-- View E: Explore / Community (Mock) -->
      <div class="absolute inset-0 overflow-y-auto p-6 space-y-6 hidden bg-slate-50" id="page-view-explore">
        <div class="max-w-6xl mx-auto space-y-6">
          <header class="p-6 rounded-2xl glass-card text-center space-y-2">
            <h2 class="text-2xl font-bold tracking-tight text-slate-900">Community Explore</h2>
            <p class="text-sm text-slate-500">Discover user-created lessons, custom AI challenges, and popular topics.</p>
          </header>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Mock items -->
            <div class="p-5 rounded-2xl glass-card flex flex-col gap-3">
              <span class="text-xs font-bold text-indigo-600 font-mono">TRENDING</span>
              <h3 class="text-sm font-bold text-slate-800">Advanced List Comprehensions</h3>
              <p class="text-xs text-slate-500 flex-1">Explore concise syntax for creating lists in a single line. Generated by AI Tutor.</p>
              <button class="w-full py-1.5 rounded-lg btn-tactile-secondary text-[10px] font-semibold">Preview Concept</button>
            </div>
            <div class="p-5 rounded-2xl glass-card flex flex-col gap-3">
              <span class="text-xs font-bold text-emerald-600 font-mono">NEW</span>
              <h3 class="text-sm font-bold text-slate-800">Understanding 'kwargs'</h3>
              <p class="text-xs text-slate-500 flex-1">A deep dive into dictionary unpacking in function arguments.</p>
              <button class="w-full py-1.5 rounded-lg btn-tactile-secondary text-[10px] font-semibold">Preview Concept</button>
            </div>
          </div>
        </div>
      </div>

      <!-- View F: Settings (Mock) -->
      <div class="absolute inset-0 overflow-y-auto p-6 space-y-6 hidden bg-slate-50" id="page-view-settings">
        <div class="max-w-3xl mx-auto space-y-6">
          <header class="p-6 rounded-2xl glass-card">
            <h2 class="text-2xl font-bold tracking-tight text-slate-900">Platform Settings</h2>
            <p class="text-sm text-slate-500 mt-1">Configure Gemini API models, appearance, and editor preferences.</p>
          </header>
          
          <div class="p-6 rounded-2xl glass-card space-y-4">
            <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider font-mono border-b pb-2">AI Configuration</h3>
            <div class="space-y-4">
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold text-slate-700">Preferred Model</label>
                <select class="p-2 rounded-lg border border-slate-200 text-xs bg-slate-50">
                  <option>gemini-3.5-flash (Default)</option>
                  <option>gemini-2.5-pro</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Bottom Status Bar -->
    <footer class="h-6 light-status-bar flex items-center justify-between px-4 text-[10px] font-mono select-none shrink-0 border-t" style="color: var(--muted-color); border-color: var(--border-color); background-color: var(--bar-bg);">
      <div class="flex items-center gap-4">
        <span>Language: Python 3</span>
        <span>|</span>
        <span id="editor-cursor-pos">Ln 1, Col 1</span>
        <span>|</span>
        <span id="dirty-label" class="text-indigo-600 font-bold">Clean</span>
        <span>|</span>
        <span id="syntax-status-label" class="text-emerald-600 font-bold">No Syntax Errors</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="opacity-80">Platform Host: bepythonic.local</span>
      </div>
    </footer>

  </div>

  <script>
    const state = {
      backend: null,
      monaco: null,
      monacoEditor: null,
      fallbackEditor: null,
      isDirty: false,
      currentPage: "home",
      currentLessonId: null,
      chatHistory: []
    };

    const ui = {
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

    // Master curriculum content
    let COURSE_CURRICULUM = [
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

    function boot() {
      initMonacoEditor();
      renderLessonsSidebarList();
      renderDashboardRoadmap();
      bindInteractiveUiEvents();
      initQtBridgeConnection();
      
      appendTutorMessage("assistant", "Welcome to the conversational tutor chat! I'm here to clarify complicated error messages, quiz your comprehension of variables or arrays, and offer hints for lesson exercises. Ask me any question below!");

      setTimeout(() => {
        initActivityChart();
      }, 300);
      
      if (window.gsap) {
        gsap.to(ui.welcomeScreen, { opacity: 1, duration: 0.35 });
      }
    }

    // Real Chart.js rendering
    function initActivityChart() {
      const canvas = document.getElementById("activity-chart");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      const gradient = ctx.createLinearGradient(0, 0, 0, 160);
      gradient.addColorStop(0, "rgba(79, 70, 229, 0.16)");
      gradient.addColorStop(1, "rgba(79, 70, 229, 0.0)");

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            label: 'Hours Spent',
            data: [1.2, 0.8, 1.6, 2.4, 1.4, 3.1, 2.7],
            borderColor: '#4f46e5',
            borderWidth: 2,
            backgroundColor: gradient,
            fill: true,
            tension: 0.38,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#4f46e5',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#4f46e5',
            pointHoverBorderColor: '#ffffff',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleFont: { family: 'Space Grotesk', size: 10, weight: 'bold' },
              bodyFont: { family: 'IBM Plex Mono', size: 9 },
              padding: 8,
              cornerRadius: 8,
              displayColors: false
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: 'IBM Plex Mono', size: 8 }, color: '#94a3b8' } },
            y: { grid: { color: '#f1f5f9' }, ticks: { font: { family: 'IBM Plex Mono', size: 8 }, color: '#94a3b8', stepSize: 1 } }
          }
        }
      });
    }

    function initMonacoEditor() {
      const MONACO_BASE_PATH = "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs";
      const enableFallback = () => {
        ui.editorHost.style.display = "none";
        ui.sourceCode.classList.add("fallback-active");
        state.fallbackEditor = ui.sourceCode;
        ui.sourceCode.addEventListener("input", () => { setDirty(true); updateEditorStats(); });
        updateEditorStats();
      };
      if (!window.require) { enableFallback(); return; }
      window.MonacoEnvironment = {
        getWorkerUrl: function (workerId, label) {
          const source = [`self.MonacoEnvironment = { baseUrl: '${MONACO_BASE_PATH}/' };`, `importScripts('${MONACO_BASE_PATH}/base/worker/workerMain.js');`].join("\n");
          return `data:text/javascript;charset=utf-8,${encodeURIComponent(source)}`;
        }
      };
      window.require.config({ paths: { vs: MONACO_BASE_PATH } });
      window.require(["vs/editor/editor.main"], () => {
        if (!window.monaco || !window.monaco.editor) { enableFallback(); return; }
        state.monaco = window.monaco;
        ui.editorHost.style.display = "block";
        ui.sourceCode.classList.remove("fallback-active");
        state.monacoEditor = state.monaco.editor.create(ui.editorHost, {
          value: ui.sourceCode.value, language: "python", theme: "vs", automaticLayout: true, minimap: { enabled: false },
          fontFamily: "IBM Plex Mono", fontSize: 13, tabSize: 4, insertSpaces: true, autoClosingBrackets: "always", matchBrackets: "always", scrollBeyondLastLine: false, padding: { top: 12, bottom: 12 }
        });
        state.monacoEditor.onDidChangeModelContent(() => { setDirty(true); updateEditorStats(); });
        state.monacoEditor.onDidChangeCursorPosition(() => { updateEditorStats(); });
        updateEditorStats();
      }, () => { enableFallback(); });
    }

    function getCodeValue() { return state.monacoEditor ? state.monacoEditor.getValue() : ui.sourceCode.value; }
    function setCodeValue(nextCode) { state.monacoEditor ? state.monacoEditor.setValue(nextCode) : ui.sourceCode.value = nextCode; setDirty(false); updateEditorStats(); }
    
    function updateEditorStats() {
      let cursorStr = "Ln 1, Col 1";
      if (state.monacoEditor) {
        const pos = state.monacoEditor.getPosition();
        if (pos) cursorStr = `Ln ${pos.lineNumber}, Col ${pos.column}`;
      }
      ui.cursorPos.textContent = cursorStr;
    }

    function setDirty(dirty) {
      state.isDirty = Boolean(dirty);
      if (state.isDirty) { ui.dirtyLabel.textContent = "Unsaved"; ui.dirtyLabel.className = "text-amber-500 font-bold"; ui.dirtyDot.style.backgroundColor = "#f59e0b"; } 
      else { ui.dirtyLabel.textContent = "Clean"; ui.dirtyLabel.className = "text-indigo-600 font-bold"; ui.dirtyDot.style.backgroundColor = "#4f46e5"; }
    }

    function renderLessonsSidebarList() {
      let count = 0;
      COURSE_CURRICULUM.forEach(c => count += c.lessons.length);
      document.getElementById("lessons-count-badge").textContent = String(count);
      const container = document.getElementById("lessons-list-sidebar");
      let html = "";
      COURSE_CURRICULUM.forEach(concept => {
        html += `
          <div class="space-y-1.5">
            <div class="px-2.5 py-1 rounded-lg bg-slate-50 flex items-center justify-between border border-slate-200/60 select-none">
              <span class="text-[9px] font-mono font-bold text-slate-500 uppercase tracking-wide">${escapeHtml(concept.conceptTitle)}</span>
              <span class="text-[8px] font-mono bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded font-bold">${concept.lessons.length} topics</span>
            </div>
            <div class="space-y-1 pl-1">
              ${concept.lessons.map(lesson => `
                <button class="w-full text-left p-2.5 rounded-lg border border-slate-200/50 bg-white hover:border-indigo-300 hover:bg-indigo-50/10 transition-all flex flex-col gap-0.5 lesson-card-btn shadow-sm" data-id="${escapeHtml(lesson.id)}">
                  <span class="text-[7px] font-mono text-indigo-500 font-bold uppercase tracking-wider">${escapeHtml(lesson.level)} · ${lesson.minutes} min</span>
                  <span class="text-xs font-semibold text-slate-800 block truncate">${escapeHtml(lesson.title)}</span>
                </button>
              `).join("")}
            </div>
          </div>`;
      });
      container.innerHTML = html;
      container.querySelectorAll(".lesson-card-btn").forEach(btn => {
        btn.addEventListener("click", () => { selectLesson(btn.dataset.id); });
      });
    }

    function renderDashboardRoadmap() {
      const container = document.getElementById("dashboard-roadmap-container");
      if (!container) return;
      let html = `<h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-2 mb-4"><span>🗺️</span> Python Course Learning Tree</h3><div class="space-y-5">`;
      COURSE_CURRICULUM.forEach(concept => {
        html += `
          <div class="relative border-l border-indigo-100 pl-6 ml-3">
            <span class="absolute -left-1 top-1 w-2.5 h-2.5 rounded-full border border-indigo-500 bg-white shadow-sm"></span>
            <div class="space-y-2">
              <div>
                <h4 class="text-xs font-bold text-slate-800 font-mono uppercase tracking-tight">${escapeHtml(concept.conceptTitle)}</h4>
                <p class="text-[10px] text-slate-400 leading-normal mt-0.5">${escapeHtml(concept.summary)}</p>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                ${concept.lessons.map(lesson => `
                  <button onclick="selectLesson('${escapeHtml(lesson.id)}')" class="p-2.5 rounded-xl border border-slate-200 bg-white/70 hover:border-indigo-300 hover:bg-indigo-50/15 text-left transition-all shadow-sm">
                    <span class="text-[7px] font-mono text-indigo-500 font-bold uppercase block">${escapeHtml(lesson.level)} · ${lesson.minutes} min</span>
                    <span class="text-xs font-bold text-slate-800 block truncate">${escapeHtml(lesson.title)}</span>
                  </button>
                `).join("")}
              </div>
            </div>
          </div>`;
      });
      html += "</div>";
      container.innerHTML = html;
    }

    // AI Lesson Generator
    window.showAiLessonGenerator = function() {
      document.getElementById("lessons-detail-container").innerHTML = `
        <div class="space-y-6 max-w-2xl mx-auto mt-10">
          <header class="space-y-2 text-center">
            <span class="text-4xl block mb-2">✨</span>
            <h1 class="text-2xl font-bold tracking-tight text-slate-900">AI Curriculum Generator</h1>
            <p class="text-sm text-slate-500 leading-relaxed max-w-md mx-auto">Generate a custom lesson module tailored to any concept using our advanced Gemini curriculum engine.</p>
          </header>
          
          <div class="p-6 rounded-2xl glass-card space-y-4">
            <div class="space-y-2">
              <label class="text-xs font-bold text-slate-800 uppercase tracking-wider font-mono">Concept / Topic</label>
              <input type="text" id="ai-lesson-topic-input" placeholder="e.g. List Comprehensions, Decorators..." class="w-full p-3 rounded-xl border border-slate-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <button id="ai-lesson-generate-btn" class="w-full py-3 px-4 rounded-xl btn-tactile-primary text-sm font-semibold" onclick="generateCustomLessonUI()">
              Generate Lesson Module
            </button>
            <div id="ai-lesson-progress" class="hidden h-1.5 rounded-full bg-slate-100 overflow-hidden mt-2">
              <div class="h-full bg-indigo-500 w-1/3 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      `;
      ui.activePathBreadcrumb.textContent = `Lesson Generator`;
    }

    window.generateCustomLessonUI = function() {
      const topic = document.getElementById("ai-lesson-topic-input").value.trim();
      if (!topic) return;
      document.getElementById("ai-lesson-generate-btn").disabled = true;
      document.getElementById("ai-lesson-generate-btn").textContent = "Synthesizing Curriculum...";
      document.getElementById("ai-lesson-progress").classList.remove("hidden");
      callBackend("generateCustomLesson", topic);
    }

    function selectLesson(id) {
      let lesson = null;
      COURSE_CURRICULUM.forEach(c => {
        const found = c.lessons.find(l => l.id === id);
        if (found) lesson = found;
      });
      if (!lesson) return;
      state.currentLessonId = lesson.id;
      switchMainTab("lessons");
      
      const objectivesHtml = lesson.objectives.map(obj => `<li class="flex items-start gap-2 text-xs text-slate-600 leading-relaxed"><svg class="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg><span>${escapeHtml(obj)}</span></li>`).join("");
      const blocksHtml = lesson.blocks.map(block => `<div class="space-y-1"><h4 class="text-xs font-bold text-indigo-900 tracking-wide uppercase font-mono">${escapeHtml(block.heading)}</h4><p class="text-xs text-slate-600 leading-relaxed">${escapeHtml(block.body)}</p></div>`).join("");

      document.getElementById("lessons-detail-container").innerHTML = `
        <div class="space-y-6 max-w-2xl mx-auto">
          <div class="text-[10px] font-mono uppercase tracking-wider text-indigo-600 font-bold select-none">${escapeHtml(lesson.level)} · ${lesson.minutes} minutes topic</div>
          <header class="space-y-1">
            <h1 class="text-2xl font-bold tracking-tight text-slate-900">${escapeHtml(lesson.title)}</h1>
            <p class="text-sm text-slate-500 leading-relaxed">${escapeHtml(lesson.summary)}</p>
          </header>
          <div class="border-b border-slate-100 my-4"></div>
          <article class="space-y-6">${blocksHtml}</article>
          <div class="rounded-xl border border-slate-200/80 bg-slate-950 shadow-sm overflow-hidden my-6">
            <div class="px-4 py-2 bg-slate-900 border-b border-slate-800 flex items-center justify-between select-none">
              <div class="flex items-center gap-1.5 text-[10px] font-mono text-slate-400"><span class="w-2 h-2 rounded-full bg-indigo-500"></span><span>minimized_lesson_snippet.py</span></div>
              <span class="text-[9px] font-mono text-indigo-400 font-bold uppercase tracking-wider">Inline preview</span>
            </div>
            <pre class="p-4 font-mono text-[11px] leading-relaxed text-slate-300 overflow-x-auto select-text"><code>${escapeHtml(lesson.starter)}</code></pre>
          </div>
          <div class="p-5 rounded-2xl border border-slate-200/60 bg-slate-50/50 space-y-3">
            <h3 class="text-[10px] font-mono font-bold text-slate-500 tracking-wider uppercase select-none">Course Objectives</h3>
            <ul class="space-y-2.5">${objectivesHtml}</ul>
          </div>
          <div class="p-6 rounded-2xl glass-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-indigo-200 bg-gradient-to-r from-indigo-50/20 to-white">
            <div class="space-y-0.5"><h4 class="text-xs font-bold text-indigo-900 font-sans">Ready to test your comprehension?</h4><p class="text-[11px] text-slate-500 leading-normal">Load this buggy starter program into your separate workspace and correct its logic errors.</p></div>
            <button onclick="launchPlaygroundWithCode('${encodeURIComponent(lesson.starter)}', '${escapeHtml(lesson.title)}')" class="py-2 px-4 rounded-xl btn-tactile-primary text-xs font-semibold shrink-0">🚀 Practice in Playground</button>
          </div>
        </div>`;
      ui.activePathBreadcrumb.textContent = `Lesson: ${lesson.title}`;
    }

    window.launchPlaygroundWithCode = function(encodedStarter, lessonTitle) {
      const code = decodeURIComponent(encodedStarter);
      setCodeValue(code);
      document.getElementById("playground-instructions-title").textContent = lessonTitle;
      document.getElementById("playground-instructions-body").innerHTML = `
        <p class="text-[10px] font-mono text-indigo-600 font-bold uppercase tracking-wider">ACTIVE PRACTICE CHALLENGE</p>
        <p class="text-xs text-slate-600 leading-relaxed font-medium">Correct the logic or syntax errors described in the <strong>Curriculum</strong> tab reading materials.</p>
        <div class="p-3.5 rounded-xl border border-slate-100 bg-slate-50/60 text-[11px] leading-relaxed text-slate-600">💡 <strong>Tips:</strong> If you get stuck, run <strong>AST CHECK</strong> or use the suggestion buttons in the <strong>AI Tutor Chat</strong> tab.</div>`;
      switchMainTab("playground");
      appendTerminalOutput("System", `Loaded code challenge variables into sandbox editor playground.`);
    };

    function switchMainTab(route) {
      state.currentPage = route;
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
        COURSE_CURRICULUM.forEach(c => { const f = c.lessons.find(l => l.id === state.currentLessonId); if (f) activeL = f; });
        pathText = activeL ? `Lesson: ${activeL.title}` : "Structured Curriculum";
      }
      if (route === "playground") pathText = "Playground Editor";
      if (route === "tutor") pathText = "AI Chat Tutor";
      if (route === "explore") pathText = "Community Explore";
      if (route === "settings") pathText = "Platform Settings";
      ui.activePathBreadcrumb.textContent = pathText;

      document.querySelectorAll(".nav-tab").forEach(btn => {
        const isActive = btn.dataset.tab === route;
        btn.classList.toggle("active", isActive);
        if (isActive) { btn.classList.add("bg-indigo-50/15", "text-indigo-600"); btn.classList.remove("text-slate-500", "hover:text-slate-900"); } 
        else { btn.classList.remove("bg-indigo-50/15", "text-indigo-600"); btn.classList.add("text-slate-500", "hover:text-slate-900"); }
      });
    }

    function callBackend(methodName, ...args) {
      if (!state.backend || typeof state.backend[methodName] !== "function") {
        appendTerminalOutput("Warn", `Backend is offline in browser preview mode: ${methodName}`);
        return;
      }
      state.backend[methodName](...args);
    }

    function appendTerminalOutput(kind, message) {
      const container = ui.terminalContent;
      const row = document.createElement("div");
      row.className = "py-0.5 border-b border-slate-900/10";
      const stamp = new Date().toLocaleTimeString();
      let colorClass = "text-emerald-400";
      if (kind.toLowerCase() === "error") colorClass = "text-rose-400 font-bold";
      if (kind.toLowerCase() === "warn") colorClass = "text-amber-500 font-bold";
      if (kind.toLowerCase() === "ast check") colorClass = "text-indigo-400 font-bold";
      row.innerHTML = `<span class="opacity-30 select-none">[${stamp}]</span> <span class="${colorClass}">${kind}:</span> <span class="select-text text-slate-300">${escapeHtml(message)}</span>`;
      container.appendChild(row);
      container.scrollTop = container.scrollHeight;
    }

    function escapeHtml(text) { return text.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

    function parseMarkdown(md) {
      if (!md) return "";
      let html = escapeHtml(md);
      html = html.replace(/```python([\s\S]*?)```/g, (match, code) => {
        return `<div class="code-block-wrapper my-3 rounded-xl overflow-hidden border border-slate-200 bg-slate-950 font-mono text-xs text-slate-300">
          <div class="px-3 py-2 bg-slate-900 border-b border-slate-800 flex justify-between items-center text-[10px] text-slate-400 select-none"><span>python</span><button onclick="copyCodeToSandbox(this)" class="text-indigo-400 hover:text-white transition-colors font-bold" data-code="${encodeURIComponent(code.trim())}">Insert to Editor</button></div>
          <pre class="p-3 overflow-auto max-h-[250px] text-left select-text"><code>${code.trim()}</code></pre></div>`;
      });
      html = html.replace(/```([\s\S]*?)```/g, (match, code) => { return `<pre class="my-3 p-3 overflow-auto rounded-lg border border-slate-800 bg-slate-905 text-left font-mono text-xs text-slate-300 select-text">${code.trim()}</pre>`; });
      html = html.replace(/`([^`\n]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-100 border border-slate-200 text-indigo-600 font-mono text-xs">$1</code>');
      html = html.replace(/\n\n/g, '</p><p class="mt-2 text-xs leading-relaxed select-text">');
      return `<p class="text-xs leading-relaxed select-text">${html}</p>`;
    }

    window.copyCodeToSandbox = function(btn) {
      const code = decodeURIComponent(btn.dataset.code);
      setCodeValue(code);
      appendTerminalOutput("System", "Injected Python code directly from AI Tutor into coding playground.");
    };

    function appendTutorMessage(role, text) {
      state.chatHistory.push({ role, text });
      const isUser = role === "user";
      
      const mainContainer = document.getElementById("chat-messages-container");
      if (mainContainer) {
        const mainBubble = document.createElement("div");
        mainBubble.className = `chat-bubble ${isUser ? "user ml-auto shadow-sm" : "ai mr-auto"}`;
        mainBubble.innerHTML = `<div class="mb-1 flex items-center justify-between select-none"><span class="text-[10px] font-bold ${isUser ? "text-indigo-200" : "text-indigo-600"}">${isUser ? "You" : "AI Tutor"}</span></div>${isUser ? `<p class="text-xs leading-relaxed select-text">${escapeHtml(text)}</p>` : parseMarkdown(text)}`;
        mainContainer.appendChild(mainBubble);
        mainContainer.scrollTop = mainContainer.scrollHeight;
        if (window.gsap) gsap.fromTo(mainBubble, { opacity: 0, y: 8, scale: 0.98 }, { opacity: 1, y: 0, scale: 1, duration: 0.15 });
      }

      const dashContainer = document.getElementById("dashboard-chat-messages-container");
      if (dashContainer) {
        const dashBubble = document.createElement("div");
        dashBubble.className = `p-2.5 rounded-xl text-xs shadow-sm border ${isUser ? "bg-indigo-50 border-indigo-100 text-slate-800 ml-5" : "bg-slate-50 border-slate-200 text-slate-700 mr-5"}`;
        dashBubble.innerHTML = `<div class="flex items-center gap-1 select-none mb-0.5"><span class="text-[8px] font-bold uppercase tracking-wider ${isUser ? "text-indigo-600" : "text-indigo-500"}">${isUser ? "You" : "AI Tutor"}</span></div><div class="leading-relaxed select-text text-[11px]">${isUser ? escapeHtml(text) : parseMarkdown(text)}</div>`;
        dashContainer.appendChild(dashBubble);
        dashContainer.scrollTop = dashContainer.scrollHeight;
        if (window.gsap) gsap.fromTo(dashBubble, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.15 });
      }
    }

    function quickTutorQuery(queryText) {
      document.getElementById("chat-input").value = "";
      appendTutorMessage("user", queryText);
      const combined = `${queryText}\n\n[Active Playground Code]\n\`\`\`python\n${getCodeValue()}\n\`\`\``;
      const payload = [...state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })), { role: "user", text: combined }];
      ui.chatInput.disabled = true; ui.sendChatBtn.disabled = true; ui.dashChatInput.disabled = true; ui.dashSendChatBtn.disabled = true;
      callBackend("askAiTutor", JSON.stringify(payload));
    }

    function sendTutorChatMessage() {
      const val = ui.chatInput.value.trim();
      if (!val) return;
      ui.chatInput.value = "";
      appendTutorMessage("user", val);
      const combined = `${val}\n\n[Active Playground Code]\n\`\`\`python\n${getCodeValue()}\n\`\`\``;
      const payload = [...state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })), { role: "user", text: combined }];
      ui.chatInput.disabled = true; ui.sendChatBtn.disabled = true; ui.dashChatInput.disabled = true; ui.dashSendChatBtn.disabled = true;
      callBackend("askAiTutor", JSON.stringify(payload));
    }

    function sendDashboardChatMessage() {
      const val = ui.dashChatInput.value.trim();
      if (!val) return;
      ui.dashChatInput.value = "";
      appendTutorMessage("user", val);
      const combined = `${val}\n\n[Active Playground Code]\n\`\`\`python\n${getCodeValue()}\n\`\`\``;
      const payload = [...state.chatHistory.slice(0, -1).map(m => ({ role: m.role, text: m.text })), { role: "user", text: combined }];
      ui.chatInput.disabled = true; ui.sendChatBtn.disabled = true; ui.dashChatInput.disabled = true; ui.dashSendChatBtn.disabled = true;
      callBackend("askAiTutor", JSON.stringify(payload));
    }

    function runCode() {
      appendTerminalOutput("System", "Transmitting Python script to local environment safe sandbox...");
      callBackend("runCode", getCodeValue());
    }

    function runAstCheck() {
      appendTerminalOutput("System", "Submitting syntax parse structure to local AST validator...");
      callBackend("syntaxCheck", getCodeValue());
    }

    function bindInteractiveUiEvents() {
      ui.enterStudioBtn.addEventListener("click", () => {
        if (window.gsap) gsap.to(ui.welcomeScreen, { opacity: 0, duration: 0.35, onComplete: () => { ui.welcomeScreen.style.display = "none"; ui.appShell.style.opacity = "1"; switchMainTab("home"); } });
        else { ui.welcomeScreen.style.display = "none"; ui.appShell.style.opacity = "1"; switchMainTab("home"); }
      });
      document.querySelectorAll(".nav-tab").forEach(btn => { btn.addEventListener("click", () => { if (btn.dataset.tab) switchMainTab(btn.dataset.tab); }); });
      ui.topRunBtn.addEventListener("click", runCode);
      ui.terminalActionCheck.addEventListener("click", runAstCheck);
      window.addEventListener("keydown", (e) => { if (e.key === "F5") { e.preventDefault(); runCode(); } });
      ui.clearTerminalBtn.addEventListener("click", () => { ui.terminalContent.innerHTML = "<div class='opacity-40 select-none'>Sandbox Console execution logs cleared.</div>"; });
      ui.sendChatBtn.addEventListener("click", sendTutorChatMessage);
      ui.chatInput.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); sendTutorChatMessage(); } });
      ui.dashSendChatBtn.addEventListener("click", sendDashboardChatMessage);
      ui.dashChatInput.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); sendDashboardChatMessage(); } });
      document.getElementById("workspace-action-open").addEventListener("click", () => { callBackend("openPythonFile"); });
    }

    function handleBridgeEvent(eventName, rawPayload) {
      let payload = {};
      try { payload = JSON.parse(rawPayload); } catch(e) {}

      switch(eventName) {
        case "bridge:ready":
          ui.bridgeStatus.textContent = "Connected"; ui.bridgeDot.style.backgroundColor = "#10b981";
          appendTerminalOutput("System", "Native Python API bridge active."); break;
          
        case "lesson:loading":
          appendTerminalOutput("System", "AI is synthesizing a new curriculum module...");
          break;
          
        case "lesson:success":
          try {
            const newConcept = JSON.parse(payload.lesson);
            COURSE_CURRICULUM.push(newConcept);
            renderLessonsSidebarList();
            renderDashboardRoadmap();
            selectLesson(newConcept.lessons[0].id);
            appendTerminalOutput("System", `Successfully generated and loaded custom lesson: ${newConcept.conceptTitle}`);
          } catch(e) {
            appendTerminalOutput("Error", "Failed to parse generated lesson JSON.");
          }
          break;
          
        case "lesson:error":
          const btn = document.getElementById("ai-lesson-generate-btn");
          if (btn) { btn.disabled = false; btn.textContent = "Generate Lesson Module"; }
          document.getElementById("ai-lesson-progress").classList.add("hidden");
          appendTerminalOutput("Error", payload.message || "Failed to generate lesson.");
          break;

        case "tutor:response":
          ui.chatInput.disabled = false; ui.sendChatBtn.disabled = false; ui.dashChatInput.disabled = false; ui.dashSendChatBtn.disabled = false;
          if (payload.text) appendTutorMessage("assistant", payload.text); break;

        case "tutor:error":
          ui.chatInput.disabled = false; ui.sendChatBtn.disabled = false; ui.dashChatInput.disabled = false; ui.dashSendChatBtn.disabled = false;
          appendTerminalOutput("Error", payload.message || "Tutor response failed.");
          appendTutorMessage("assistant", "I encountered an error analyzing that query."); break;

        case "run:result":
          if (payload.ok) appendTerminalOutput("Stdout", payload.stdout || "Process executed successfully.");
          else { if (payload.stdout) appendTerminalOutput("Stdout", payload.stdout); appendTerminalOutput("Error", payload.stderr || "Process closed with failures."); }
          break;

        case "syntax:result":
          if (payload.ok) { ui.syntaxStatus.textContent = "No Syntax Errors"; ui.syntaxStatus.className = "text-emerald-600 font-bold"; appendTerminalOutput("AST Check", payload.message); }
          else { ui.syntaxStatus.textContent = "Syntax Error"; ui.syntaxStatus.className = "text-rose-600 font-bold"; appendTerminalOutput("AST Error", payload.message); }
          break;

        case "file:opened": setCodeValue(payload.code || ""); switchMainTab("playground"); appendTerminalOutput("System", `Loaded open Python file: ${payload.name}`); break;
        case "file:saved": setDirty(false); appendTerminalOutput("System", `Saved file: ${payload.name}`); break;
        case "file:error": appendTerminalOutput("Error", `IO error: ${payload.message}`); break;
      }
    }

    function initQtBridgeConnection() {
      if (!window.QWebChannel || !window.qt || !qt.webChannelTransport) {
        ui.bridgeStatus.textContent = "Preview Mode"; ui.bridgeDot.style.backgroundColor = "#f59e0b";
        appendTerminalOutput("Warn", "Connected in browser preview sandbox."); return;
      }
      new QWebChannel(qt.webChannelTransport, (channel) => {
        state.backend = channel.objects.backend || null;
        if (!state.backend) { ui.bridgeStatus.textContent = "Bridge Offline"; ui.bridgeDot.style.backgroundColor = "#ef4444"; return; }
        if (state.backend.bridgeEvent) state.backend.bridgeEvent.connect(handleBridgeEvent);
        ui.bridgeStatus.textContent = "Connected"; ui.bridgeDot.style.backgroundColor = "#10b981";
        if (typeof state.backend.ready === "function") state.backend.ready();
      });
    }

    window.selectLesson = selectLesson;
    boot();
  </script>
</body>
</html>
"""
