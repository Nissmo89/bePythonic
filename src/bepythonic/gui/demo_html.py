"""Kinetic UI dashboard/editor pages rendered inside QWebEngineView."""

EDITOR_HTML = r"""
<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>bePythonic - Kinetic Studio</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/material-darker.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/monokai.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/cobalt.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/base16-dark.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vue-calendar-heatmap@0.8.4/dist/vue-calendar-heatmap.css">

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/split.js/1.6.5/split.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vue@2.7.16/dist/vue.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vue-calendar-heatmap@0.8.4/dist/vue-calendar-heatmap.browser.js"></script>
  <script src="qrc:///qtwebchannel/qwebchannel.js"></script>

  <style>
    :root {
      color-scheme: dark;
      --background: #0b1326;
      --surface-lowest: #060e20;
      --surface-low: #131b2e;
      --surface: #171f33;
      --surface-high: #222a3d;
      --surface-highest: #2d3449;
      --on-surface: #dae2fd;
      --on-surface-variant: #c5c9ac;
      --outline: #8f9378;
      --outline-variant: #454932;
      --lime: #cdf200;
      --lime-dim: #b4d400;
      --yellow: #ffe24c;
      --yellow-dim: #e2c62d;
      --danger: #ffb4ab;
      --glow: 0 0 24px rgba(205, 242, 0, 0.15);
      --radius-xs: 4px;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --space-1: 8px;
      --space-2: 16px;
      --space-3: 24px;
      --space-4: 32px;
    }

    * {
      box-sizing: border-box;
    }

    html,
    body {
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: radial-gradient(circle at top right, rgba(205, 242, 0, 0.08), transparent 34%),
        radial-gradient(circle at bottom left, rgba(255, 226, 76, 0.08), transparent 36%),
        var(--background);
      color: var(--on-surface);
      font-family: "Geist", sans-serif;
    }

    button,
    input,
    select,
    textarea {
      font-family: inherit;
    }

    .material-symbols-outlined {
      font-family: "Material Symbols Outlined";
      font-weight: normal;
      font-style: normal;
      font-size: 22px;
      line-height: 1;
      display: inline-block;
      white-space: nowrap;
      direction: ltr;
      -webkit-font-feature-settings: "liga";
      -webkit-font-smoothing: antialiased;
    }

    #app {
      height: 100%;
      display: flex;
    }

    .side-nav {
      width: 252px;
      background: var(--surface-low);
      border-right: 1px solid var(--outline-variant);
      padding: 28px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex-shrink: 0;
      overflow: hidden;
    }

    .brand {
      padding: 0 12px 14px;
      border-bottom: 1px solid rgba(143, 147, 120, 0.22);
      margin-bottom: 8px;
    }

    .brand h1 {
      margin: 0;
      font-size: 30px;
      line-height: 1.15;
      letter-spacing: -0.02em;
      font-weight: 700;
      color: var(--lime-dim);
    }

    .brand p {
      margin: 8px 0 0;
      color: var(--on-surface-variant);
      font-size: 12px;
      letter-spacing: 0.06em;
      font-family: "JetBrains Mono", monospace;
      text-transform: uppercase;
    }

    .nav-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      overflow-y: auto;
      padding-right: 2px;
      flex: 1;
    }

    .nav-item {
      border: 1px solid transparent;
      background: transparent;
      color: var(--on-surface-variant);
      border-radius: var(--radius-md);
      padding: 11px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: left;
    }

    .nav-item:hover {
      background: var(--surface-highest);
      color: var(--lime);
    }

    .nav-item.active {
      border-color: rgba(205, 242, 0, 0.48);
      background: rgba(205, 242, 0, 0.09);
      color: var(--lime);
      box-shadow: var(--glow);
      transform: translateX(2px);
    }

    .nav-footer {
      border-top: 1px solid rgba(143, 147, 120, 0.22);
      padding-top: 12px;
      display: grid;
      gap: 8px;
    }

    .main-shell {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
    }

    .topbar {
      height: 68px;
      border-bottom: 1px solid var(--outline-variant);
      background: rgba(19, 27, 46, 0.9);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      gap: 16px;
      flex-shrink: 0;
    }

    .topbar-title {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }

    .topbar-title .kicker {
      color: var(--yellow-dim);
      font-size: 12px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      font-family: "JetBrains Mono", monospace;
    }

    .topbar-title .title {
      margin: 0;
      font-size: 22px;
      line-height: 1.2;
      letter-spacing: -0.01em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .topbar-search {
      width: 320px;
      background: var(--surface);
      border: 1px solid var(--outline-variant);
      border-radius: 999px;
      color: var(--on-surface);
      padding: 9px 14px;
      font-size: 14px;
      outline: none;
      transition: all 0.2s ease;
    }

    .topbar-search:focus {
      border-color: rgba(205, 242, 0, 0.58);
      box-shadow: var(--glow);
    }

    .icon-btn {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 1px solid var(--outline-variant);
      background: var(--surface);
      color: var(--on-surface-variant);
      display: grid;
      place-items: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .icon-btn:hover {
      border-color: rgba(205, 242, 0, 0.58);
      color: var(--lime);
    }

    .chip {
      border: 1px solid var(--outline-variant);
      background: var(--surface-high);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 12px;
      color: var(--on-surface-variant);
      font-family: "JetBrains Mono", monospace;
    }

    .chip.connected {
      color: var(--lime);
      border-color: rgba(205, 242, 0, 0.58);
      box-shadow: var(--glow);
    }

    .chip.warn {
      color: var(--yellow);
      border-color: rgba(255, 226, 76, 0.45);
    }

    #page-container {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .page {
      position: absolute;
      inset: 0;
      overflow-y: auto;
      padding: 24px;
      scrollbar-width: thin;
      scrollbar-color: var(--outline-variant) transparent;
    }

    .page.hidden {
      display: none;
    }

    .page::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }

    .page::-webkit-scrollbar-thumb {
      background: var(--outline-variant);
      border-radius: 999px;
    }

    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      gap: var(--space-3);
      max-width: 1260px;
      margin: 0 auto;
    }

    .hero {
      grid-column: span 8;
      background: linear-gradient(160deg, rgba(19, 27, 46, 0.94), rgba(34, 42, 61, 0.9));
      border: 1px solid var(--outline-variant);
      border-top: 2px solid var(--lime-dim);
      border-radius: var(--radius-lg);
      padding: 24px;
      position: relative;
      overflow: hidden;
    }

    .hero::after {
      content: "";
      position: absolute;
      right: -70px;
      top: -70px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(205, 242, 0, 0.28), transparent 68%);
      pointer-events: none;
    }

    .panel {
      background: var(--surface-low);
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-lg);
      padding: 20px;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }

    .panel:hover {
      border-color: rgba(205, 242, 0, 0.4);
      transform: translateY(-2px);
    }

    .streak {
      grid-column: span 4;
    }

    .activity {
      grid-column: span 12;
    }

    .quick-card {
      grid-column: span 4;
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .meter {
      width: 100%;
      height: 8px;
      border-radius: 999px;
      background: var(--surface-highest);
      overflow: hidden;
      border: 1px solid rgba(143, 147, 120, 0.25);
    }

    .meter-fill {
      height: 100%;
      width: 0;
      background: linear-gradient(90deg, var(--yellow), var(--lime));
    }

    .activity-grid {
      display: grid;
      grid-template-columns: repeat(15, minmax(0, 1fr));
      gap: 6px;
    }

    .calendar-heatmap-shell {
      position: relative;
      border-radius: calc(var(--radius-lg) + 2px);
      padding: 1px;
      background: linear-gradient(
        125deg,
        rgba(205, 242, 0, 0.46) 0%,
        rgba(255, 226, 76, 0.22) 32%,
        rgba(143, 147, 120, 0.26) 68%,
        rgba(69, 73, 50, 0.72) 100%
      );
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.3), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
      overflow: hidden;
    }

    .calendar-heatmap-shell::before {
      content: "";
      position: absolute;
      left: -120px;
      top: -88px;
      width: 320px;
      height: 210px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(205, 242, 0, 0.22) 0%, rgba(205, 242, 0, 0) 72%);
      pointer-events: none;
      z-index: 0;
    }

    .calendar-heatmap-shell::after {
      content: "";
      position: absolute;
      right: -110px;
      bottom: -86px;
      width: 280px;
      height: 180px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 226, 76, 0.18) 0%, rgba(255, 226, 76, 0) 74%);
      pointer-events: none;
      z-index: 0;
    }

    .calendar-heatmap-host {
      position: relative;
      border: 1px solid rgba(143, 147, 120, 0.24);
      border-radius: calc(var(--radius-lg) + 1px);
      background:
        linear-gradient(180deg, rgba(8, 15, 31, 0.97) 0%, rgba(13, 21, 40, 0.95) 44%, rgba(18, 29, 52, 0.9) 100%),
        repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.02) 0px, rgba(255, 255, 255, 0.02) 1px, transparent 1px, transparent 42px);
      padding: 18px 16px 12px;
      overflow-x: auto;
      min-height: 188px;
      scrollbar-width: thin;
      scrollbar-color: var(--outline-variant) transparent;
      z-index: 1;
    }

    .calendar-heatmap-host::-webkit-scrollbar {
      height: 8px;
    }

    .calendar-heatmap-host::-webkit-scrollbar-thumb {
      background: var(--outline-variant);
      border-radius: 999px;
    }

    .calendar-heatmap-host .vch__container,
    .calendar-heatmap-host .vch__wrapper {
      min-width: 780px;
    }

    .calendar-heatmap-host svg {
      display: block;
      overflow: visible;
    }

    .calendar-heatmap-host text {
      fill: rgba(218, 226, 253, 0.78) !important;
      font-family: "JetBrains Mono", monospace;
      font-size: 11px;
      letter-spacing: 0.01em;
    }

    .calendar-heatmap-host rect {
      stroke: rgba(143, 147, 120, 0.3);
      stroke-width: 0.8px;
      rx: 2.5;
      ry: 2.5;
      transition: transform 0.15s ease, filter 0.2s ease, stroke 0.2s ease;
      transform-box: fill-box;
      transform-origin: center;
    }

    .calendar-heatmap-host rect:hover {
      transform: translateY(-1px) scale(1.06);
      stroke: rgba(205, 242, 0, 0.55);
      filter: drop-shadow(0 0 6px rgba(205, 242, 0, 0.24));
    }

    .calendar-heatmap-host .vch__legend {
      margin-top: 10px;
      color: var(--on-surface-variant);
      font-family: "JetBrains Mono", monospace;
      font-size: 11px;
    }

    .calendar-heatmap-legend-band {
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      padding: 10px 14px 12px;
      border-top: 1px solid rgba(143, 147, 120, 0.24);
      background: linear-gradient(180deg, rgba(19, 27, 46, 0.86), rgba(12, 19, 34, 0.9));
      font-family: "JetBrains Mono", monospace;
      font-size: 11px;
      color: var(--on-surface-variant);
    }

    .calendar-heatmap-ramp {
      display: inline-flex;
      gap: 6px;
      align-items: center;
    }

    .calendar-heatmap-ramp i {
      width: 12px;
      height: 12px;
      border-radius: 3px;
      border: 1px solid rgba(143, 147, 120, 0.26);
      box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
    }

    .calendar-heatmap-fallback {
      min-height: 120px;
    }

    .heat {
      aspect-ratio: 1;
      border-radius: 4px;
      border: 1px solid rgba(143, 147, 120, 0.12);
      opacity: 0.86;
      transition: opacity 0.2s ease;
    }

    .heat:hover {
      opacity: 1;
    }

    .editor-wrap {
      max-width: 1320px;
      margin: 0 auto;
      display: grid;
      gap: 16px;
    }

    .editor-toolbar {
      background: var(--surface-low);
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-lg);
      padding: 12px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .btn {
      border: 1px solid var(--outline-variant);
      background: var(--surface-high);
      color: var(--on-surface-variant);
      border-radius: var(--radius-sm);
      padding: 8px 10px;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn:hover {
      color: var(--lime);
      border-color: rgba(205, 242, 0, 0.52);
    }

    .btn.primary {
      background: var(--lime-dim);
      border-color: var(--lime-dim);
      color: #1d2400;
      box-shadow: var(--glow);
    }

    .btn.primary:hover {
      background: var(--lime);
      border-color: var(--lime);
      color: #151a00;
    }

    .btn.warn {
      color: var(--yellow);
      border-color: rgba(255, 226, 76, 0.46);
    }

    .btn:disabled {
      cursor: wait;
      opacity: 0.7;
    }

    .workspace {
      display: flex;
      min-height: 660px;
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-lg);
      overflow: hidden;
      background: var(--surface-low);
    }

    .workspace-left,
    .workspace-right {
      min-width: 0;
      padding: 14px;
    }

    .workspace-left {
      width: 70%;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 10px;
      background: #000;
    }

    .workspace-right {
      width: 30%;
      border-left: 1px solid var(--outline-variant);
      background: var(--surface);
      display: grid;
      grid-template-rows: auto auto auto 1fr auto;
      gap: 10px;
    }

    .gutter.gutter-horizontal {
      width: 8px;
      background: linear-gradient(180deg, var(--surface-highest), var(--surface));
      border-left: 1px solid var(--outline-variant);
      border-right: 1px solid var(--outline-variant);
      cursor: col-resize;
      position: relative;
    }

    .gutter.gutter-horizontal::after {
      content: "";
      position: absolute;
      left: 50%;
      top: 14px;
      bottom: 14px;
      width: 2px;
      transform: translateX(-50%);
      border-radius: 999px;
      background: rgba(143, 147, 120, 0.5);
    }

    .editor-head {
      background: rgba(23, 31, 51, 0.8);
      border: 1px solid rgba(143, 147, 120, 0.35);
      border-radius: var(--radius-sm);
      padding: 8px 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-family: "JetBrains Mono", monospace;
      font-size: 12px;
      color: var(--on-surface-variant);
    }

    .cm-wrap {
      border: 1px solid rgba(143, 147, 120, 0.35);
      border-radius: var(--radius-sm);
      overflow: hidden;
      min-height: 380px;
      background: #000;
    }

    .CodeMirror {
      height: 100%;
      min-height: 380px;
      font-family: "JetBrains Mono", monospace;
      font-size: 14px;
      line-height: 1.55;
    }

    #fallback-editor {
      display: none;
      width: 100%;
      min-height: 380px;
      background: #000;
      border: 0;
      color: #dae2fd;
      padding: 14px;
      resize: vertical;
      outline: none;
      font-family: "JetBrains Mono", monospace;
      font-size: 14px;
      line-height: 1.55;
    }

    .stats {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .console {
      border: 1px solid rgba(143, 147, 120, 0.35);
      border-radius: var(--radius-sm);
      background: #0c1223;
      min-height: 150px;
      overflow: hidden;
      display: grid;
      grid-template-rows: auto 1fr;
    }

    .console-head {
      border-bottom: 1px solid rgba(143, 147, 120, 0.28);
      padding: 8px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--on-surface-variant);
      font-family: "JetBrains Mono", monospace;
    }

    .console-log {
      margin: 0;
      list-style: none;
      padding: 10px;
      display: grid;
      gap: 6px;
      overflow-y: auto;
      max-height: 200px;
    }

    .log-item {
      border: 1px solid rgba(143, 147, 120, 0.32);
      border-radius: var(--radius-sm);
      padding: 6px 8px;
      font-family: "JetBrains Mono", monospace;
      font-size: 12px;
      color: var(--on-surface-variant);
      background: rgba(6, 14, 32, 0.85);
    }

    .log-item.success {
      border-left: 3px solid var(--lime-dim);
      color: #d9ef96;
    }

    .log-item.warn {
      border-left: 3px solid var(--yellow);
      color: #ffe990;
    }

    .log-item.error {
      border-left: 3px solid var(--danger);
      color: #ffd3cc;
    }

    .ai-card {
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-sm);
      background: rgba(19, 27, 46, 0.9);
      padding: 10px;
      display: grid;
      gap: 8px;
    }

    .ai-label {
      margin: 0;
      color: var(--yellow-dim);
      text-transform: uppercase;
      font-size: 12px;
      font-family: "JetBrains Mono", monospace;
      letter-spacing: 0.06em;
    }

    .ai-topic-input,
    .text-notes,
    .theme-select {
      width: 100%;
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-sm);
      background: var(--surface-high);
      color: var(--on-surface);
      padding: 8px 10px;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .ai-topic-input:focus,
    .text-notes:focus,
    .theme-select:focus {
      border-color: rgba(205, 242, 0, 0.58);
      box-shadow: var(--glow);
    }

    .topic-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .topic-chip {
      border: 1px solid rgba(255, 226, 76, 0.35);
      border-radius: 999px;
      background: rgba(226, 198, 45, 0.12);
      color: #ffe990;
      padding: 4px 10px;
      font-size: 12px;
      cursor: pointer;
      font-family: "JetBrains Mono", monospace;
      transition: all 0.2s ease;
    }

    .topic-chip:hover {
      border-color: rgba(255, 226, 76, 0.6);
      background: rgba(226, 198, 45, 0.18);
    }

    .assistant-feed {
      margin: 0;
      list-style: none;
      padding: 0;
      display: grid;
      gap: 8px;
      overflow-y: auto;
      max-height: 220px;
    }

    .assistant-msg {
      border: 1px solid rgba(143, 147, 120, 0.32);
      border-radius: var(--radius-sm);
      background: rgba(6, 14, 32, 0.7);
      padding: 8px;
      font-size: 13px;
      line-height: 1.45;
      color: var(--on-surface-variant);
    }

    .assistant-msg.system {
      border-left: 3px solid rgba(143, 147, 120, 0.55);
    }

    .assistant-msg.success {
      border-left: 3px solid var(--lime-dim);
      color: #d9ef96;
    }

    .assistant-msg.error {
      border-left: 3px solid var(--danger);
      color: #ffd3cc;
    }

    .text-notes {
      min-height: 110px;
      resize: vertical;
      font-size: 13px;
      line-height: 1.5;
    }

    .kpi {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-size: 14px;
    }

    .kpi strong {
      color: var(--lime);
      font-family: "JetBrains Mono", monospace;
    }

    .section-title {
      max-width: 1260px;
      margin: 0 auto 20px;
    }

    .section-title h2 {
      margin: 0;
      font-size: 42px;
      line-height: 1.1;
      letter-spacing: -0.02em;
    }

    .section-title p {
      margin: 8px 0 0;
      color: var(--on-surface-variant);
      font-size: 17px;
      line-height: 1.5;
    }

    @media (max-width: 1240px) {
      .workspace {
        flex-direction: column;
      }

      .workspace-left,
      .workspace-right {
        width: 100%;
      }

      .workspace-right {
        border-left: 0;
        border-top: 1px solid var(--outline-variant);
      }

      .gutter {
        display: none;
      }

      .hero,
      .streak,
      .quick-card,
      .activity {
        grid-column: span 12;
      }
    }

    @media (max-width: 980px) {
      .side-nav {
        display: none;
      }

      .topbar-search {
        width: 200px;
      }

      .section-title h2 {
        font-size: 30px;
      }
    }

    @media (max-width: 760px) {
      .topbar {
        padding: 0 12px;
      }

      .topbar-search {
        display: none;
      }

      .page {
        padding: 14px;
      }
    }
  </style>
</head>
<body>
  <div id="app">
    <nav class="side-nav">
      <div class="brand">
        <h1>bePythonic</h1>
        <p>Kinetic Logic Studio</p>
      </div>

      <div class="nav-list">
        <button class="nav-item active" data-page="dashboard" type="button">
          <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
          <span>Dashboard</span>
        </button>
        <button class="nav-item" data-page="editor" type="button">
          <span class="material-symbols-outlined">code</span>
          <span>Editor</span>
        </button>
        <button class="nav-item" type="button">
          <span class="material-symbols-outlined">menu_book</span>
          <span>Library</span>
        </button>
        <button class="nav-item" type="button">
          <span class="material-symbols-outlined">group</span>
          <span>Community</span>
        </button>
        <button class="nav-item" type="button">
          <span class="material-symbols-outlined">settings</span>
          <span>Settings</span>
        </button>
      </div>

      <div class="nav-footer">
        <button class="btn primary" id="nav-start-coding" type="button">
          <span class="material-symbols-outlined">bolt</span>
          Open Editor
        </button>
        <div class="chip" id="bridge-chip">Bridge: connecting...</div>
      </div>
    </nav>

    <section class="main-shell">
      <header class="topbar">
        <div class="topbar-title">
          <span class="kicker" id="topbar-kicker">Kinetic Logic</span>
          <h2 class="title" id="topbar-title">Dashboard</h2>
        </div>

        <div class="topbar-right">
          <input class="topbar-search" type="search" placeholder="Search lessons, snippets, bugs..." />
          <button class="icon-btn" type="button" aria-label="Notifications">
            <span class="material-symbols-outlined">notifications</span>
          </button>
          <button class="icon-btn" type="button" aria-label="Profile">
            <span class="material-symbols-outlined">account_circle</span>
          </button>
        </div>
      </header>

      <main id="page-container">
        <section class="page" id="page-dashboard">
          <div class="section-title">
            <h2>Welcome back, Coder.</h2>
            <p>Electric momentum, structured progress, and focused Python practice.</p>
          </div>

          <div class="dashboard-grid">
            <article class="hero">
              <div class="kpi">
                <span>Current Track</span>
                <strong>Module 4 / 10</strong>
              </div>
              <h3 style="margin: 0; font-size: 32px; line-height: 1.2;">Python Patterns</h3>
              <p style="margin: 10px 0 22px; color: var(--on-surface-variant); font-size: 16px; max-width: 620px;">
                Master structural and behavioral patterns in Python with guided broken-code drills.
              </p>
              <div class="kpi" style="margin-bottom: 8px;">
                <span style="font-family: 'JetBrains Mono', monospace; color: var(--on-surface-variant);">Progress</span>
                <strong id="progress-label">40%</strong>
              </div>
              <div class="meter">
                <div class="meter-fill" id="progress-fill"></div>
              </div>
              <div style="margin-top: 24px; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                <span style="color: var(--on-surface-variant); font-size: 14px;">~ 35 mins left in this module</span>
                <button class="btn primary" data-page="editor" type="button">
                  <span class="material-symbols-outlined">play_arrow</span>
                  Continue In Editor
                </button>
              </div>
            </article>

            <article class="panel streak">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <p class="ai-label" style="margin: 0; color: var(--on-surface-variant);">Learning Streak</p>
                <span class="material-symbols-outlined" style="color: var(--yellow);">local_fire_department</span>
              </div>
              <div style="margin-top: 16px; display: flex; align-items: baseline; gap: 8px;">
                <span style="font-size: 58px; font-weight: 700; line-height: 1; color: var(--lime);">12</span>
                <span style="color: var(--on-surface-variant);">days</span>
              </div>
              <p style="margin: 10px 0 0; color: var(--on-surface-variant); font-size: 14px;">Top 15% consistency this week.</p>
            </article>

            <article class="panel activity">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h4 style="margin: 0; font-size: 20px;">Activity Heatmap</h4>
                <span class="chip">Last 12 Months</span>
              </div>
              <div class="calendar-heatmap-shell">
                <div class="calendar-heatmap-host" id="calendar-heatmap-host">
                  <div id="calendar-heatmap-app"></div>
                  <div class="activity-grid calendar-heatmap-fallback" id="activity-grid-fallback" style="display: none;"></div>
                </div>
                <div class="calendar-heatmap-legend-band">
                  <span>Low Focus</span>
                  <span class="calendar-heatmap-ramp" aria-hidden="true">
                    <i style="background: #0c1428;"></i>
                    <i style="background: #1a2b49;"></i>
                    <i style="background: #2f4e72;"></i>
                    <i style="background: #95b72a;"></i>
                    <i style="background: #cdf200;"></i>
                    <i style="background: #ffe24c;"></i>
                  </span>
                  <span>High Focus</span>
                </div>
              </div>
            </article>

            <article class="panel quick-card">
              <span class="material-symbols-outlined" style="color: var(--lime);">code_blocks</span>
              <div>
                <h5 style="margin: 0; font-size: 18px;">Daily Challenge</h5>
                <p style="margin: 4px 0 0; color: var(--on-surface-variant);">Solve one algorithm today.</p>
              </div>
            </article>
            <article class="panel quick-card">
              <span class="material-symbols-outlined" style="color: var(--yellow);">quiz</span>
              <div>
                <h5 style="margin: 0; font-size: 18px;">Quick Quiz</h5>
                <p style="margin: 4px 0 0; color: var(--on-surface-variant);">Reinforce syntax memory.</p>
              </div>
            </article>
            <article class="panel quick-card">
              <span class="material-symbols-outlined" style="color: #d9e3f7;">smart_toy</span>
              <div>
                <h5 style="margin: 0; font-size: 18px;">AI Tutor</h5>
                <p style="margin: 4px 0 0; color: var(--on-surface-variant);">Ask for nudges, not full answers.</p>
              </div>
            </article>
          </div>
        </section>

        <section class="page hidden" id="page-editor">
          <div class="editor-wrap">
            <div class="editor-toolbar">
              <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px;">
                <span class="chip" id="file-chip">main.py</span>
                <span class="chip" id="dirty-chip">Saved</span>
                <span class="chip" id="engine-chip">Editor: loading...</span>
              </div>

              <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px;">
                <button class="btn" id="open-btn" type="button"><span class="material-symbols-outlined">folder_open</span>Open</button>
                <button class="btn" id="save-btn" type="button"><span class="material-symbols-outlined">save</span>Save</button>
                <button class="btn" id="syntax-btn" type="button"><span class="material-symbols-outlined">rule</span>Syntax</button>
                <button class="btn" id="copy-btn" type="button"><span class="material-symbols-outlined">content_copy</span>Copy</button>
                <button class="btn warn" id="clear-btn" type="button"><span class="material-symbols-outlined">ink_eraser</span>Clear</button>
              </div>
            </div>

            <section class="workspace" id="workspace-split">
              <section class="workspace-left" id="workspace-left">
                <div class="editor-head">
                  <span>Code Editor</span>
                  <span id="cursor-chip">Ln 1, Col 1</span>
                </div>

                <div class="cm-wrap">
                  <textarea id="editor-source"></textarea>
                  <textarea id="fallback-editor" spellcheck="false"></textarea>
                </div>

                <div class="stats">
                  <span class="chip" id="line-chip">Lines: 0</span>
                  <span class="chip" id="char-chip">Chars: 0</span>
                  <span class="chip" id="sel-chip">Selection: 0</span>
                  <select class="theme-select" id="theme-select" style="max-width: 170px; padding: 5px 8px;">
                    <option value="dracula">Theme: Dracula</option>
                    <option value="material-darker">Theme: Material Darker</option>
                    <option value="monokai">Theme: Monokai</option>
                    <option value="cobalt">Theme: Cobalt</option>
                    <option value="base16-dark">Theme: Base16 Dark</option>
                  </select>
                  <button class="btn" id="wrap-btn" type="button">Wrap: Off</button>
                  <button class="btn" id="font-down" type="button">A-</button>
                  <button class="btn" id="font-up" type="button">A+</button>
                </div>

                <section class="console">
                  <div class="console-head">
                    <span>OUTPUT CONSOLE</span>
                    <button class="btn" id="clear-console" type="button">Clear</button>
                  </div>
                  <ul class="console-log" id="console-log"></ul>
                </section>
              </section>

              <aside class="workspace-right" id="workspace-right">
                <section class="ai-card">
                  <p class="ai-label">AI Generator</p>
                  <input class="ai-topic-input" id="ai-topic" placeholder="Topic, e.g. loops, lists, functions" type="text" />
                  <button class="btn primary" id="ai-generate" type="button">
                    <span class="material-symbols-outlined">auto_awesome</span>
                    Generate Broken Exercise
                  </button>
                  <div class="topic-chips">
                    <button class="topic-chip" data-topic="loops" type="button">loops</button>
                    <button class="topic-chip" data-topic="lists" type="button">lists</button>
                    <button class="topic-chip" data-topic="functions" type="button">functions</button>
                    <button class="topic-chip" data-topic="recursion" type="button">recursion</button>
                    <button class="topic-chip" data-topic="decorators" type="button">decorators</button>
                  </div>
                </section>

                <section class="ai-card">
                  <p class="ai-label">AI Feed</p>
                  <ul class="assistant-feed" id="assistant-feed"></ul>
                </section>

                <section class="ai-card">
                  <p class="ai-label">Notes</p>
                  <textarea class="text-notes" id="notes" placeholder="Capture hypotheses, TODOs, and debugging breadcrumbs."></textarea>
                </section>

                <div class="chip" id="syntax-chip">Syntax: not checked</div>
              </aside>
            </section>
          </div>
        </section>
      </main>
    </section>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/search/searchcursor.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/matchbrackets.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closebrackets.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/comment/comment.min.js"></script>

  <script>
    const STARTER_CODE = [
      "# Kinetic Logic exercise starter",
      "def normalize_scores(values):",
      "    cleaned = [value for value in values if value >= 0]",
      "    total = sum(cleaned)",
      "    if total == 0:",
      "        return []",
      "    return [round(value / total, 3) for value in cleaned]",
      "",
      "if __name__ == '__main__':",
      "    scores = [10, 20, 5, 15]",
      "    print(normalize_scores(scores))",
      "",
    ].join("\n");

    const HEATMAP_COLOR_RANGE = [
      "#0c1428",
      "#1a2b49",
      "#2f4e72",
      "#95b72a",
      "#cdf200",
      "#ffe24c",
    ];
    const HEATMAP_FALLBACK_LEVELS = [
      0.22, 0.71, 0.42, 0.9, 0.37, 0.16, 0.66, 0.58, 0.31, 0.45,
      0.83, 0.12, 0.56, 0.74, 0.27, 0.39, 0.61, 0.95, 0.48, 0.2,
      0.54, 0.8, 0.67, 0.28, 0.88, 0.35, 0.52, 0.13, 0.77, 0.63,
    ];

    const PAGE_META = {
      dashboard: {
        title: "Dashboard",
        kicker: "Kinetic Logic",
      },
      editor: {
        title: "Editor Studio",
        kicker: "CodeMirror + AI Bridge",
      },
    };

    const pageDashboard = document.getElementById("page-dashboard");
    const pageEditor = document.getElementById("page-editor");
    const topbarTitle = document.getElementById("topbar-title");
    const topbarKicker = document.getElementById("topbar-kicker");

    const bridgeChip = document.getElementById("bridge-chip");
    const fileChip = document.getElementById("file-chip");
    const dirtyChip = document.getElementById("dirty-chip");
    const engineChip = document.getElementById("engine-chip");
    const lineChip = document.getElementById("line-chip");
    const charChip = document.getElementById("char-chip");
    const selChip = document.getElementById("sel-chip");
    const cursorChip = document.getElementById("cursor-chip");
    const syntaxChip = document.getElementById("syntax-chip");
    const consoleLog = document.getElementById("console-log");
    const assistantFeed = document.getElementById("assistant-feed");
    const themeSelect = document.getElementById("theme-select");
    const fallbackEditor = document.getElementById("fallback-editor");

    let backend = null;
    let codeMirror = null;
    let calendarHeatmapVm = null;
    let fallbackMode = false;
    let wrapEnabled = false;
    let currentFontSize = 14;

    function parsePayload(rawPayload) {
      if (typeof rawPayload === "string") {
        try {
          return JSON.parse(rawPayload);
        } catch (_error) {
          return {};
        }
      }
      if (rawPayload && typeof rawPayload === "object") {
        return rawPayload;
      }
      return {};
    }

    function addConsole(kind, message) {
      const item = document.createElement("li");
      item.className = `log-item ${kind}`;
      const stamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      item.textContent = `[${stamp}] ${message}`;
      consoleLog.prepend(item);
      while (consoleLog.children.length > 50) {
        consoleLog.removeChild(consoleLog.lastChild);
      }
    }

    function addAssistant(kind, message) {
      const item = document.createElement("li");
      item.className = `assistant-msg ${kind}`;
      item.textContent = message;
      assistantFeed.prepend(item);
      while (assistantFeed.children.length > 18) {
        assistantFeed.removeChild(assistantFeed.lastChild);
      }
    }

    function setBridgeStatus(connected) {
      bridgeChip.classList.toggle("connected", connected);
      bridgeChip.textContent = connected ? "Bridge: Qt connected" : "Bridge: preview mode";
    }

    function setDirtyState(isDirty) {
      dirtyChip.textContent = isDirty ? "Unsaved" : "Saved";
      dirtyChip.classList.toggle("warn", isDirty);
    }

    function getCodeValue() {
      if (codeMirror) {
        return codeMirror.getValue();
      }
      return fallbackEditor.value;
    }

    function setCodeValue(nextCode) {
      const safeCode = typeof nextCode === "string" ? nextCode : "";
      if (codeMirror) {
        codeMirror.setValue(safeCode);
      } else {
        fallbackEditor.value = safeCode;
      }
      updateEditorStats();
      setDirtyState(false);
    }

    function updateEditorStats() {
      const text = getCodeValue();
      const lines = text ? text.split("\n").length : 0;
      lineChip.textContent = `Lines: ${lines}`;
      charChip.textContent = `Chars: ${text.length}`;

      let selected = 0;
      if (codeMirror) {
        selected = codeMirror.getSelection().length;
        const cursor = codeMirror.getCursor();
        cursorChip.textContent = `Ln ${cursor.line + 1}, Col ${cursor.ch + 1}`;
      } else {
        const start = fallbackEditor.selectionStart || 0;
        const end = fallbackEditor.selectionEnd || 0;
        selected = Math.max(0, end - start);
      }

      selChip.textContent = `Selection: ${selected}`;
    }

    function openFindPrompt() {
      const query = window.prompt("Find text:");
      if (!query) {
        return;
      }

      if (!codeMirror) {
        addConsole("warn", "Find is limited in fallback mode.");
        return;
      }

      const cursor = codeMirror.getSearchCursor(query, codeMirror.getCursor());
      if (cursor.findNext()) {
        codeMirror.setSelection(cursor.from(), cursor.to());
        codeMirror.scrollIntoView({ from: cursor.from(), to: cursor.to() }, 110);
        addConsole("success", `Found: ${query}`);
        return;
      }

      addConsole("warn", `No match for: ${query}`);
    }

    function callBackend(methodName, ...args) {
      if (!backend || typeof backend[methodName] !== "function") {
        addConsole("warn", `Qt backend unavailable: ${methodName}`);
        addAssistant("system", "Qt backend unavailable. Running in preview mode.");
        return false;
      }

      backend[methodName](...args);
      return true;
    }

    function handleBridgeEvent(eventName, rawPayload) {
      const payload = parsePayload(rawPayload);

      switch (eventName) {
        case "bridge:ready":
          addConsole("success", "Qt web bridge ready.");
          addAssistant("system", "Bridge connected. AI and file actions are active.");
          break;

        case "editor:setCode":
          if (typeof payload.code === "string") {
            setCodeValue(payload.code);
          }
          navigate("editor", false);
          addConsole("success", "Editor updated from AI result.");
          break;

        case "ai:loading": {
          const loading = Boolean(payload.loading);
          const button = document.getElementById("ai-generate");
          button.disabled = loading;
          button.innerHTML = loading
            ? "<span class='material-symbols-outlined'>hourglass_empty</span>Generating..."
            : "<span class='material-symbols-outlined'>auto_awesome</span>Generate Broken Exercise";
          if (loading) {
            const topic = typeof payload.topic === "string" ? payload.topic : "(topic)";
            addAssistant("system", `Generating practice code for: ${topic}`);
          }
          break;
        }

        case "ai:message": {
          const message = typeof payload.message === "string" ? payload.message : "AI task finished.";
          addAssistant("success", message);
          addConsole("success", message);
          break;
        }

        case "ai:error": {
          const message = typeof payload.message === "string" ? payload.message : "AI generation failed.";
          addAssistant("error", message);
          addConsole("error", message);
          break;
        }

        case "syntax:result": {
          const ok = Boolean(payload.ok);
          const message = typeof payload.message === "string" ? payload.message : "Syntax result received.";
          syntaxChip.textContent = ok ? "Syntax: clean" : "Syntax: issues";
          syntaxChip.classList.toggle("warn", !ok);
          addConsole(ok ? "success" : "error", message);
          addAssistant(ok ? "success" : "error", message);
          break;
        }

        case "file:opened": {
          const name = typeof payload.name === "string" ? payload.name : "main.py";
          const code = typeof payload.code === "string" ? payload.code : "";
          fileChip.textContent = name;
          setCodeValue(code);
          addConsole("success", `Opened ${name}`);
          addAssistant("system", `Loaded file: ${name}`);
          break;
        }

        case "file:saved": {
          const name = typeof payload.name === "string" ? payload.name : "exercise.py";
          fileChip.textContent = name;
          setDirtyState(false);
          addConsole("success", `Saved ${name}`);
          addAssistant("success", `Saved file: ${name}`);
          break;
        }

        case "file:error": {
          const message = typeof payload.message === "string" ? payload.message : "File operation failed.";
          addConsole("error", message);
          addAssistant("error", message);
          break;
        }

        default:
          addConsole("warn", `Unhandled bridge event: ${eventName}`);
          break;
      }
    }

    function initQtBridge() {
      if (!window.QWebChannel || !window.qt || !qt.webChannelTransport) {
        setBridgeStatus(false);
        addConsole("warn", "QWebChannel unavailable. Preview mode active.");
        addAssistant("system", "Preview mode: AI/open/save actions require desktop runtime.");
        return;
      }

      new QWebChannel(qt.webChannelTransport, (channel) => {
        backend = channel.objects.backend;
        if (!backend) {
          setBridgeStatus(false);
          addConsole("error", "Qt bridge object not found.");
          return;
        }

        if (backend.bridgeEvent) {
          backend.bridgeEvent.connect(handleBridgeEvent);
        }

        setBridgeStatus(true);
        backend.ready();
      });
    }

    function formatDate(dateValue) {
      const date = new Date(dateValue);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
    }

    function buildCalendarHeatmapValues(days = 365) {
      const values = [];
      const today = new Date();

      for (let i = days - 1; i >= 0; i -= 1) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);

        const wave = Math.sin(i / 10) + Math.cos(i / 19);
        const trend = Math.max(0, Math.round((wave + 2) * 1.8));
        const boost = i % 7 === 0 ? 3 : i % 9 === 0 ? 2 : 0;
        const drop = i % 11 === 0 ? 2 : 0;
        const count = Math.max(0, Math.min(12, trend + boost - drop));

        values.push({ date: formatDate(date), count });
      }

      return values;
    }

    function initHeatmapFallback() {
      const grid = document.getElementById("activity-grid-fallback");
      if (!grid) {
        return;
      }

      grid.innerHTML = "";
      grid.style.display = "grid";

      HEATMAP_FALLBACK_LEVELS.forEach((level) => {
        const cell = document.createElement("div");
        cell.className = "heat";

        let color = "rgba(143, 147, 120, 0.24)";
        if (level > 0.8) {
          color = "rgba(205, 242, 0, 0.95)";
        } else if (level > 0.55) {
          color = "rgba(205, 242, 0, 0.68)";
        } else if (level > 0.35) {
          color = "rgba(255, 226, 76, 0.58)";
        }

        cell.style.background = color;
        cell.title = `Activity ${Math.round(level * 100)}%`;
        grid.appendChild(cell);
      });
    }

    function initCalendarHeatmap() {
      const mount = document.getElementById("calendar-heatmap-app");
      if (!mount) {
        return;
      }

      const values = buildCalendarHeatmapValues(365);
      const endDate = formatDate(new Date());

      const hasRegisteredHeatmap = Boolean(
        window.Vue &&
        window.Vue.options &&
        window.Vue.options.components &&
        (
          window.Vue.options.components["calendar-heatmap"] ||
          window.Vue.options.components.CalendarHeatmap
        )
      );

      if (!window.Vue || (!window.VueCalendarHeatmap && !hasRegisteredHeatmap)) {
        addConsole("warn", "Calendar heatmap library unavailable, using fallback tiles.");
        initHeatmapFallback();
        return;
      }

      if (window.VueCalendarHeatmap) {
        try {
          if (window.VueCalendarHeatmap.CalendarHeatmap) {
            window.Vue.component("calendar-heatmap", window.VueCalendarHeatmap.CalendarHeatmap);
          } else if (window.VueCalendarHeatmap.install) {
            window.Vue.use(window.VueCalendarHeatmap);
          }
        } catch (_error) {
          // Ignore duplicate component/plugin registration errors.
        }
      }

      mount.innerHTML = `
        <calendar-heatmap
          :values="values"
          :end-date="endDate"
          :max="maxCount"
          :tooltip="false"
          :color-range="colorRange"
          :range-color="rangeColor"
          tooltip-unit="sessions"
          no-data-text="No activity recorded"
        />
      `;

      try {
        calendarHeatmapVm = new Vue({
          el: "#calendar-heatmap-app",
          data: {
            values,
            endDate,
            maxCount: 12,
            colorRange: HEATMAP_COLOR_RANGE.slice(1),
            rangeColor: HEATMAP_COLOR_RANGE,
          },
        });
        addConsole("success", "Calendar heatmap loaded.");
      } catch (_error) {
        addConsole("warn", "Calendar heatmap mount failed, using fallback tiles.");
        mount.innerHTML = "";
        initHeatmapFallback();
      }
    }

    function initProgressAnimation() {
      if (!window.gsap) {
        const fill = document.getElementById("progress-fill");
        fill.style.width = "40%";
        return;
      }

      gsap.to("#progress-fill", {
        width: "40%",
        duration: 1.1,
        ease: "power2.out",
      });

      gsap.from(".panel, .hero", {
        y: 18,
        opacity: 0,
        duration: 0.65,
        ease: "power3.out",
        stagger: 0.06,
      });
    }

    function initSplitPane() {
      if (!window.Split || window.innerWidth < 1240) {
        return;
      }

      Split(["#workspace-left", "#workspace-right"], {
        sizes: [70, 30],
        minSize: [500, 320],
        gutterSize: 8,
      });
    }

    function initRouting() {
      const initial = window.location.hash.replace("#", "");
      navigate(initial === "editor" ? "editor" : "dashboard", false);

      window.addEventListener("hashchange", () => {
        const hash = window.location.hash.replace("#", "");
        navigate(hash === "editor" ? "editor" : "dashboard", false);
      });

      document.querySelectorAll("[data-page]").forEach((button) => {
        button.addEventListener("click", () => {
          navigate(button.dataset.page || "dashboard", true);
        });
      });

      document.getElementById("nav-start-coding").addEventListener("click", () => {
        navigate("editor", true);
      });
    }

    function navigate(pageName, updateHash = true) {
      const target = pageName === "editor" ? "editor" : "dashboard";

      pageDashboard.classList.toggle("hidden", target !== "dashboard");
      pageEditor.classList.toggle("hidden", target !== "editor");

      document.querySelectorAll("[data-page]").forEach((button) => {
        button.classList.toggle("active", button.dataset.page === target);
      });

      topbarTitle.textContent = PAGE_META[target].title;
      topbarKicker.textContent = PAGE_META[target].kicker;

      if (updateHash) {
        window.location.hash = target;
      }

      if (target === "editor" && codeMirror) {
        window.setTimeout(() => codeMirror.refresh(), 20);
      }
    }

    function initCodeEditor() {
      const source = document.getElementById("editor-source");
      source.value = STARTER_CODE;

      if (!window.CodeMirror) {
        fallbackMode = true;
        fallbackEditor.style.display = "block";
        fallbackEditor.value = STARTER_CODE;
        source.style.display = "none";
        engineChip.textContent = "Editor: fallback textarea";
        addConsole("warn", "CodeMirror unavailable. Fallback textarea enabled.");

        fallbackEditor.addEventListener("input", () => {
          updateEditorStats();
          setDirtyState(true);
        });
        fallbackEditor.addEventListener("select", updateEditorStats);
        updateEditorStats();
        return;
      }

      codeMirror = CodeMirror.fromTextArea(source, {
        mode: "python",
        theme: "dracula",
        lineNumbers: true,
        lineWrapping: false,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        extraKeys: {
          "Ctrl-F": openFindPrompt,
          "Cmd-F": openFindPrompt,
          "Ctrl-S": () => callBackend("savePythonFile", getCodeValue()),
          "Cmd-S": () => callBackend("savePythonFile", getCodeValue()),
          "Ctrl-/": "toggleComment",
          "Cmd-/": "toggleComment",
        },
      });

      codeMirror.on("change", () => {
        updateEditorStats();
        setDirtyState(true);
      });
      codeMirror.on("cursorActivity", updateEditorStats);

      engineChip.textContent = "Editor: CodeMirror ready";
      updateEditorStats();
      setDirtyState(false);
      addConsole("success", "CodeMirror booted with Python mode.");
      addAssistant("system", "CodeMirror ready. You can now generate AI exercises.");
    }

    function bindEditorControls() {
      document.getElementById("open-btn").addEventListener("click", () => {
        callBackend("openPythonFile");
      });

      document.getElementById("save-btn").addEventListener("click", () => {
        callBackend("savePythonFile", getCodeValue());
      });

      document.getElementById("syntax-btn").addEventListener("click", () => {
        callBackend("syntaxCheck", getCodeValue());
      });

      document.getElementById("copy-btn").addEventListener("click", async () => {
        const text = getCodeValue();
        try {
          await navigator.clipboard.writeText(text);
          addConsole("success", "Code copied to clipboard.");
        } catch (_error) {
          addConsole("error", "Clipboard copy failed.");
        }
      });

      document.getElementById("clear-btn").addEventListener("click", () => {
        setCodeValue("");
        addConsole("warn", "Editor cleared.");
      });

      document.getElementById("clear-console").addEventListener("click", () => {
        consoleLog.innerHTML = "";
        addConsole("success", "Console cleared.");
      });

      document.getElementById("wrap-btn").addEventListener("click", () => {
        wrapEnabled = !wrapEnabled;
        const button = document.getElementById("wrap-btn");
        button.textContent = wrapEnabled ? "Wrap: On" : "Wrap: Off";
        if (codeMirror) {
          codeMirror.setOption("lineWrapping", wrapEnabled);
          codeMirror.refresh();
        } else {
          fallbackEditor.style.whiteSpace = wrapEnabled ? "pre-wrap" : "pre";
        }
      });

      document.getElementById("font-up").addEventListener("click", () => {
        currentFontSize = Math.min(22, currentFontSize + 1);
        const cmEl = document.querySelector(".CodeMirror");
        if (cmEl && codeMirror) {
          cmEl.style.fontSize = `${currentFontSize}px`;
          codeMirror.refresh();
        } else {
          fallbackEditor.style.fontSize = `${currentFontSize}px`;
        }
      });

      document.getElementById("font-down").addEventListener("click", () => {
        currentFontSize = Math.max(11, currentFontSize - 1);
        const cmEl = document.querySelector(".CodeMirror");
        if (cmEl && codeMirror) {
          cmEl.style.fontSize = `${currentFontSize}px`;
          codeMirror.refresh();
        } else {
          fallbackEditor.style.fontSize = `${currentFontSize}px`;
        }
      });

      themeSelect.addEventListener("change", (event) => {
        const theme = event.target.value;
        if (codeMirror) {
          codeMirror.setOption("theme", theme);
          addConsole("success", `Theme switched to ${theme}.`);
        }
      });

      document.querySelectorAll(".topic-chip").forEach((button) => {
        button.addEventListener("click", () => {
          const topic = button.dataset.topic || "";
          const input = document.getElementById("ai-topic");
          input.value = topic;
          triggerAiGeneration();
        });
      });

      document.getElementById("ai-generate").addEventListener("click", triggerAiGeneration);
    }

    function triggerAiGeneration() {
      const input = document.getElementById("ai-topic");
      const topic = input.value.trim();

      if (!topic) {
        addAssistant("error", "Enter a topic before generating code.");
        return;
      }

      const sent = callBackend("generateBrokenCode", topic);
      if (!sent) {
        addAssistant("error", "Backend unavailable. Cannot call AI generation.");
      }
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
        lines: text ? text.split("\n").length : 0,
        chars: text.length,
        fallback: fallbackMode,
      };
    };

    initCalendarHeatmap();
    initRouting();
    initCodeEditor();
    bindEditorControls();
    initSplitPane();
    initProgressAnimation();
    initQtBridge();
  </script>
</body>
</html>
"""
