// Dashboard stats and Chart.js initialization
window.initActivityChart = function() {
  if (typeof Chart === "undefined") {
    setTimeout(window.initActivityChart, 50);
    return;
  }
  const canvas = document.getElementById("activity-chart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  
  // Custom Sea Blue to transparent gradient
  const gradient = ctx.createLinearGradient(0, 0, 0, 160);
  gradient.addColorStop(0, "rgba(11, 132, 230, 0.16)");
  gradient.addColorStop(1, "rgba(11, 132, 230, 0.0)");

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Hours Spent',
        data: [1.2, 0.8, 1.6, 2.4, 1.4, 3.1, 2.7],
        borderColor: '#0b84e6', // Sea Blue
        borderWidth: 2,
        backgroundColor: gradient,
        fill: true,
        tension: 0.38,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#0b84e6',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: '#0b84e6',
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
          cornerRadius: 6, // Smooth corners
          displayColors: false
        }
      },
      scales: {
        x: { 
          grid: { display: false }, 
          ticks: { font: { family: 'IBM Plex Mono', size: 8 }, color: '#94a3b8' } 
        },
        y: { 
          grid: { color: '#f1f5f9' }, 
          ticks: { font: { family: 'IBM Plex Mono', size: 8 }, color: '#94a3b8', stepSize: 1 } 
        }
      }
    }
  });
};

window.renderDashboardRoadmap = function() {
  const container = document.getElementById("dashboard-roadmap-container");
  if (!container) return;
  
  let html = `
    <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-2 mb-4 select-none">
      <span>🗺️</span> Python Course Learning Tree
    </h3>
    <div class="space-y-5">`;
    
  if (!window.COURSE_CURRICULUM || window.COURSE_CURRICULUM.length === 0) {
    html += `<div class="text-xs text-slate-400 p-4">Loading syllabus data...</div>`;
  } else {
    window.COURSE_CURRICULUM.forEach(concept => {
      const title = concept.title || concept.conceptTitle || "Curriculum Module";
      const summary = concept.description || concept.summary || "Master Python core concepts step-by-step.";
      const lessons = concept.lessons || [];
      
      html += `
        <div class="relative border-l border-indigo-100 pl-6 ml-3">
          <span class="absolute -left-1.5 top-1.5 w-3 h-3 border border-indigo-500 bg-white shadow-sm rounded-full"></span>
          <div class="space-y-2">
            <div>
              <h4 class="text-xs font-bold text-slate-800 font-mono uppercase tracking-tight">${window.escapeHtml(title)}</h4>
              <p class="text-[10px] text-slate-400 leading-normal mt-0.5">${window.escapeHtml(summary)}</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
              ${lessons.map(lesson => {
                const lessonId = lesson.lesson_id || lesson.id;
                const minutes = lesson.minutes || 8;
                const level = lesson.level || "Beginner";
                const isCompleted = window.state.completedLessons && window.state.completedLessons.has(lessonId);
                return `
                  <button onclick="selectLesson('${window.escapeHtml(lessonId)}')" class="p-2.5 border border-slate-200 bg-white/70 hover:border-indigo-300 hover:bg-indigo-50/15 text-left transition-all shadow-sm flex flex-col justify-between rounded-lg">
                    <div class="flex items-center justify-between w-full gap-1">
                      <span class="text-[7px] font-mono text-indigo-500 font-bold uppercase block">${window.escapeHtml(level)} · ${minutes} min</span>
                      ${isCompleted ? '<span class="text-emerald-500 text-[9px] font-bold">✓</span>' : ''}
                    </div>
                    <span class="text-xs font-bold text-slate-800 block truncate w-full mt-0.5">${window.escapeHtml(lesson.title)}</span>
                  </button>
                `;
              }).join("")}
            </div>
          </div>
        </div>`;
    });
  }
  
  html += "</div>";
  container.innerHTML = html;
};

