from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Watchtower Admin</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117;--surface:#161b22;--surface2:#1c2128;
  --border:#30363d;--text:#e6edf3;--dim:#848d97;
  --accent:#58a6ff;--green:#3fb950;--red:#f85149;
  --amber:#d29922;--purple:#bc8cff;
}
body{background:var(--bg);color:var(--text);font:13px/1.5 'SF Mono',ui-monospace,monospace;min-height:100vh}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:10px 16px;display:flex;align-items:center;gap:12px}
header h1{font-size:14px;font-weight:600;color:var(--text)}
header .badge{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:2px 8px;font-size:11px;color:var(--dim)}
nav{background:var(--surface);border-bottom:1px solid var(--border);display:flex;gap:0;overflow-x:auto}
nav button{background:none;border:none;color:var(--dim);cursor:pointer;padding:10px 16px;font:inherit;font-size:12px;border-bottom:2px solid transparent;white-space:nowrap}
nav button:hover{color:var(--text)}
nav button.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-content{display:none;padding:16px}
.tab-content.active{display:block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:12px}
.card h3{font-size:11px;text-transform:uppercase;color:var(--dim);margin-bottom:10px;letter-spacing:.04em}
.row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--border)}
.row:last-child{border-bottom:none}
.row .k{color:var(--dim);font-size:12px}
.row .v{font-size:12px;text-align:right;max-width:60%}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:4px}
.ok{color:var(--green)}.warn{color:var(--amber)}.err{color:var(--red)}.info{color:var(--accent)}
.dot-ok{background:var(--green)}.dot-warn{background:var(--amber)}.dot-err{background:var(--red)}.dot-off{background:var(--dim)}
table{width:100%;border-collapse:collapse;font-size:12px}
th{color:var(--dim);text-align:left;padding:6px 8px;border-bottom:1px solid var(--border);font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
td{padding:6px 8px;border-bottom:1px solid var(--border);vertical-align:top}
tr:last-child td{border-bottom:none}
.tag{display:inline-block;border-radius:3px;padding:1px 6px;font-size:11px;margin:1px}
.tag-ok{background:rgba(63,185,80,.15);color:var(--green);border:1px solid rgba(63,185,80,.3)}
.tag-warn{background:rgba(210,153,34,.15);color:var(--amber);border:1px solid rgba(210,153,34,.3)}
.tag-err{background:rgba(248,81,73,.15);color:var(--red);border:1px solid rgba(248,81,73,.3)}
.tag-info{background:rgba(88,166,255,.15);color:var(--accent);border:1px solid rgba(88,166,255,.3)}
.tag-off{background:rgba(132,141,151,.1);color:var(--dim);border:1px solid rgba(132,141,151,.2)}
pre{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:10px;font:12px/1.4 inherit;overflow-x:auto;white-space:pre-wrap;word-break:break-all}
.toolbar{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.btn{background:var(--surface2);border:1px solid var(--border);color:var(--text);cursor:pointer;padding:5px 12px;border-radius:4px;font:inherit;font-size:12px}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn-primary{background:rgba(88,166,255,.15);border-color:var(--accent);color:var(--accent)}
.section-title{font-size:11px;text-transform:uppercase;color:var(--dim);margin:16px 0 8px;letter-spacing:.04em}
.empty{color:var(--dim);font-size:12px;padding:20px;text-align:center}
.refresh-ts{color:var(--dim);font-size:11px;margin-left:auto}
.chip-list{display:flex;flex-wrap:wrap;gap:4px}
.chip{background:var(--surface2);border:1px solid var(--border);border-radius:3px;padding:1px 6px;font-size:11px;color:var(--dim)}
input,textarea,select{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:5px 8px;border-radius:4px;font:inherit;font-size:12px;width:100%}
input:focus,textarea:focus,select:focus{outline:none;border-color:var(--accent)}
label{font-size:11px;color:var(--dim);display:block;margin-bottom:3px}
.form-row{margin-bottom:10px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center}
.modal-overlay.open{display:flex}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;min-width:480px;max-width:600px;max-height:80vh;overflow-y:auto}
.modal h2{font-size:13px;margin-bottom:16px;color:var(--text)}
.modal-footer{display:flex;justify-content:flex-end;gap:8px;margin-top:16px;border-top:1px solid var(--border);padding-top:12px}
</style>
</head>
<body>
<header>
  <h1>Watchtower Admin</h1>
  <span class="badge" id="hdr-env">local</span>
  <span class="badge" id="hdr-ver">v0.1.0</span>
  <span style="margin-left:auto;font-size:11px;color:var(--dim)" id="hdr-ts"></span>
</header>
<nav id="nav">
  <button class="active" onclick="switchTab('status')">Status</button>
  <button onclick="switchTab('sources')">Sources</button>
  <button onclick="switchTab('filters')">Filters</button>
  <button onclick="switchTab('routing')">Routing</button>
  <button onclick="switchTab('queue')">Review Queue</button>
  <button onclick="switchTab('telegram')">Telegram</button>
  <button onclick="switchTab('ai')">AI Providers</button>
</nav>

<!-- STATUS TAB -->
<div id="tab-status" class="tab-content active">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadStatus()">Refresh</button>
    <span class="refresh-ts" id="status-ts"></span>
  </div>
  <div class="grid3" id="status-grid">
    <div class="card"><div class="empty">Loading...</div></div>
  </div>
</div>

<!-- SOURCES TAB -->
<div id="tab-sources" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadSources()">Refresh</button>
    <span class="refresh-ts" id="sources-ts"></span>
  </div>
  <div id="sources-content"><div class="empty">Loading...</div></div>
</div>

<!-- FILTERS TAB -->
<div id="tab-filters" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadFilters()">Refresh</button>
    <button class="btn" onclick="openFilterModal()">+ New Filter</button>
    <span class="refresh-ts" id="filters-ts"></span>
  </div>
  <div id="filters-content"><div class="empty">Loading...</div></div>
</div>

<!-- ROUTING TAB -->
<div id="tab-routing" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadRouting()">Refresh</button>
    <button class="btn" onclick="openRoutingModal()">+ New Rule</button>
    <span class="refresh-ts" id="routing-ts"></span>
  </div>
  <div id="routing-content"><div class="empty">Loading...</div></div>
</div>

<!-- REVIEW QUEUE TAB -->
<div id="tab-queue" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadQueue()">Refresh</button>
    <button class="btn" onclick="runMockIntelligence()" id="btn-run-intel">Run Mock Intelligence</button>
    <select id="queue-status-filter" style="width:140px" onchange="loadQueue()">
      <option value="">All</option>
      <option value="pending">Pending</option>
      <option value="approved">Approved</option>
      <option value="rejected">Rejected</option>
    </select>
    <span class="refresh-ts" id="queue-ts"></span>
  </div>
  <div id="intel-result" style="display:none;margin-bottom:10px"></div>
  <div id="intel-counts" style="margin-bottom:10px"></div>
  <div id="queue-content"><div class="empty">Loading...</div></div>
</div>

<!-- TELEGRAM TAB -->
<div id="tab-telegram" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadTelegram()">Refresh</button>
    <span class="refresh-ts" id="telegram-ts"></span>
  </div>
  <div id="telegram-content"><div class="empty">Loading...</div></div>
</div>

<!-- AI PROVIDERS TAB -->
<div id="tab-ai" class="tab-content">
  <div class="toolbar">
    <button class="btn btn-primary" onclick="loadAI()">Refresh</button>
    <span class="refresh-ts" id="ai-ts"></span>
  </div>
  <div id="ai-content"><div class="empty">Loading...</div></div>
</div>

<!-- FILTER MODAL -->
<div class="modal-overlay" id="filter-modal">
  <div class="modal">
    <h2>Filter</h2>
    <div class="form-row"><label>Name</label><input id="fm-name" placeholder="Filter name"></div>
    <div class="form-row">
      <label>Enabled</label>
      <select id="fm-enabled"><option value="true">Yes</option><option value="false">No</option></select>
    </div>
    <div class="form-row">
      <label>Market Scope (comma-separated: KR, US, KR_ETF, US_ETF)</label>
      <input id="fm-market-scope" value="KR,US,KR_ETF,US_ETF">
    </div>
    <div class="form-row">
      <label>Source Types (comma-separated: news, disclosure, macro, flow)</label>
      <input id="fm-source-types" value="news,disclosure,macro,flow">
    </div>
    <div class="form-row">
      <label>Symbols (comma-separated, leave blank for all)</label>
      <input id="fm-symbols" placeholder="005930,AAPL,...">
    </div>
    <div class="form-row">
      <label>Keywords Include (comma-separated)</label>
      <input id="fm-kw-include" placeholder="">
    </div>
    <div class="form-row">
      <label>Keywords Exclude (comma-separated)</label>
      <input id="fm-kw-exclude" placeholder="">
    </div>
    <div class="form-grid">
      <div class="form-row">
        <label>Min Importance</label>
        <select id="fm-importance">
          <option value="low">Low</option>
          <option value="medium" selected>Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      <div class="form-row">
        <label>Freshness Window (minutes)</label>
        <input id="fm-freshness" type="number" value="1440" min="60">
      </div>
    </div>
    <div class="form-grid">
      <div class="form-row">
        <label>Send to Telegram</label>
        <select id="fm-telegram"><option value="false" selected>No</option><option value="true">Yes</option></select>
      </div>
      <div class="form-row">
        <label>Send to VultureInv</label>
        <select id="fm-vultureinv"><option value="true" selected>Yes</option><option value="false">No</option></select>
      </div>
    </div>
    <div class="form-row">
      <label>Requires Owner Review</label>
      <select id="fm-review"><option value="true" selected>Yes</option><option value="false">No</option></select>
    </div>
    <div class="modal-footer">
      <button class="btn" onclick="closeFilterModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveFilter()">Save</button>
    </div>
  </div>
</div>

<!-- ROUTING MODAL -->
<div class="modal-overlay" id="routing-modal">
  <div class="modal">
    <h2>Routing Rule</h2>
    <div class="form-row"><label>Filter ID</label><input id="rm-filter-id" placeholder="Filter ID"></div>
    <div class="form-row">
      <label>Enabled</label>
      <select id="rm-enabled"><option value="true">Yes</option><option value="false">No</option></select>
    </div>
    <div class="form-row">
      <label>Destinations (comma-separated: review_queue, telegram_brief, vultureinv_snapshot)</label>
      <input id="rm-destinations" value="review_queue">
    </div>
    <div class="form-row">
      <label>Explain Routing Decision</label>
      <select id="rm-explain"><option value="true" selected>Yes</option><option value="false">No</option></select>
    </div>
    <div class="modal-footer">
      <button class="btn" onclick="closeRoutingModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveRouting()">Save</button>
    </div>
  </div>
</div>

<script>
const BASE = '';
let currentTab = 'status';
let statusInterval = null;

function ts() { return new Date().toLocaleTimeString('ko-KR'); }

function switchTab(tab) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  document.querySelectorAll('nav button').forEach((el, i) => {
    const tabs = ['status','sources','filters','routing','queue','telegram','ai'];
    if (tabs[i] === tab) el.classList.add('active');
  });
  currentTab = tab;
  const loaders = {status:loadStatus,sources:loadSources,filters:loadFilters,routing:loadRouting,queue:loadQueue,telegram:loadTelegram,ai:loadAI};
  if (loaders[tab]) loaders[tab]();
}

function dotHtml(ok) {
  if (ok === true || ok === 'ok' || ok === 'running') return '<span class="dot dot-ok"></span>';
  if (ok === false || ok === 'stopped' || ok === 'error') return '<span class="dot dot-err"></span>';
  if (ok === 'stale') return '<span class="dot dot-warn"></span>';
  return '<span class="dot dot-off"></span>';
}
function colorVal(v, cls) { return `<span class="${cls}">${v}</span>`; }

async function loadStatus() {
  try {
    const [health, status, settings, snapshots] = await Promise.all([
      fetch(BASE + '/health').then(r=>r.json()),
      fetch(BASE + '/status').then(r=>r.json()),
      fetch(BASE + '/settings/redacted').then(r=>r.json()),
      Promise.all(['regime','flow','catalysts'].map(t =>
        fetch(BASE + '/snapshots/' + t + '/latest').then(r=>r.json()).catch(()=>({freshness_state:'error'}))
      )),
    ]);
    document.getElementById('hdr-env').textContent = status.service?.env || 'local';
    document.getElementById('hdr-ver').textContent = status.service?.version || '';
    document.getElementById('hdr-ts').textContent = 'updated ' + ts();
    document.getElementById('status-ts').textContent = ts();

    const latestJob = status.latest_job_run;
    const snapshotNames = ['regime','flow','catalysts'];

    document.getElementById('status-grid').innerHTML = `
      <div class="card">
        <h3>Service</h3>
        <div class="row"><span class="k">API</span><span class="v">${dotHtml(health.status === 'ok')} ${colorVal(health.status || 'ok', 'ok')}</span></div>
        <div class="row"><span class="k">Scheduler</span><span class="v">${dotHtml(status.scheduler?.status)} ${status.scheduler?.status || '—'}</span></div>
        <div class="row"><span class="k">Storage</span><span class="v">${dotHtml(status.storage?.status)} ${status.storage?.status || '—'}</span></div>
        <div class="row"><span class="k">DB path</span><span class="v" style="font-size:10px;max-width:70%;overflow:hidden;text-overflow:ellipsis">${status.storage?.db_path || '—'}</span></div>
        <div class="row"><span class="k">Snapshots</span><span class="v">${status.storage?.snapshot_count ?? '—'}</span></div>
      </div>
      <div class="card">
        <h3>Latest Job Run</h3>
        ${latestJob ? `
          <div class="row"><span class="k">Job</span><span class="v">${latestJob.job_name}</span></div>
          <div class="row"><span class="k">Status</span><span class="v">${dotHtml(latestJob.status === 'completed')} ${latestJob.status}</span></div>
          <div class="row"><span class="k">Started</span><span class="v" style="font-size:10px">${latestJob.started_at?.slice(0,19).replace('T',' ')}</span></div>
          <div class="row"><span class="k">Finished</span><span class="v" style="font-size:10px">${latestJob.finished_at?.slice(0,19).replace('T',' ') || '—'}</span></div>
          <div class="row"><span class="k">Message</span><span class="v" style="font-size:10px">${latestJob.message || '—'}</span></div>
        ` : '<div class="empty">No job runs yet</div>'}
      </div>
      <div class="card">
        <h3>Snapshots</h3>
        ${snapshots.map((s, i) => `
          <div class="row">
            <span class="k">${snapshotNames[i]}</span>
            <span class="v">${dotHtml(s.freshness_state)} ${s.freshness_state || 'n/a'}</span>
          </div>
        `).join('')}
        <div class="row"><span class="k">VultureInv</span><span class="v">${dotHtml(status.vultureinv?.reachable)} ${status.vultureinv?.reachable ? 'reachable' : 'unreachable'}</span></div>
      </div>
    `;
  } catch(e) {
    document.getElementById('status-grid').innerHTML = `<div class="card"><div class="empty err">Error: ${e.message}</div></div>`;
  }
}

async function loadSources() {
  try {
    const settings = await fetch(BASE + '/settings/redacted').then(r=>r.json());
    document.getElementById('sources-ts').textContent = ts();
    const cfg = [
      {name:'KRX', configured: '(built-in)', enabled: false},
      {name:'FRED', configured: settings.fred_configured, enabled: settings.fred_configured},
      {name:'OpenDART', configured: settings.opendart_configured, enabled: settings.opendart_configured},
      {name:'SEC', configured: settings.sec_user_agent_configured, enabled: settings.sec_user_agent_configured},
    ];
    document.getElementById('sources-content').innerHTML = `
      <div class="card">
        <h3>Data Sources</h3>
        <table>
          <thead><tr><th>Source</th><th>Configured</th><th>Status</th><th>Notes</th></tr></thead>
          <tbody>
            ${cfg.map(s => `
              <tr>
                <td>${s.name}</td>
                <td>${s.configured === true ? colorVal('Yes','ok') : s.configured === false ? colorVal('No','warn') : s.configured}</td>
                <td>${s.enabled ? '<span class="tag tag-warn">stub</span>' : '<span class="tag tag-off">disabled</span>'}</td>
                <td style="color:var(--dim);font-size:11px">v1: mock provider only</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      <div class="card" style="margin-top:12px">
        <h3>Mock Provider</h3>
        <div class="row"><span class="k">Status</span><span class="v ok">active</span></div>
        <div class="row"><span class="k">Types</span><span class="v">regime, flow, catalysts</span></div>
        <div class="row"><span class="k">Schedule</span><span class="v">every 30 min</span></div>
        <div class="row"><span class="k">Manual trigger</span><span class="v"><button class="btn" onclick="triggerMock()" style="padding:2px 8px;font-size:11px">Run now</button></span></div>
      </div>
    `;
  } catch(e) {
    document.getElementById('sources-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

async function triggerMock() {
  try {
    const r = await fetch(BASE + '/jobs/refresh/mock', {method:'POST'}).then(r=>r.json());
    alert('Mock job: ' + JSON.stringify(r));
    loadSources();
  } catch(e) { alert('Error: ' + e.message); }
}

async function loadFilters() {
  try {
    const data = await fetch(BASE + '/filters').then(r=>r.json());
    document.getElementById('filters-ts').textContent = ts();
    const filters = data.filters || [];
    if (!filters.length) {
      document.getElementById('filters-content').innerHTML = '<div class="empty">No filters configured.</div>';
      return;
    }
    document.getElementById('filters-content').innerHTML = `
      <table>
        <thead><tr><th>Name</th><th>Enabled</th><th>Market</th><th>Source Types</th><th>Min Importance</th><th>Telegram</th><th>VultureInv</th><th>Review</th></tr></thead>
        <tbody>
          ${filters.map(f => `
            <tr>
              <td><strong>${f.name}</strong><br><span style="color:var(--dim);font-size:10px">${f.id}</span></td>
              <td>${f.enabled ? '<span class="tag tag-ok">On</span>' : '<span class="tag tag-off">Off</span>'}</td>
              <td><div class="chip-list">${(f.market_scope||[]).map(m=>`<span class="chip">${m}</span>`).join('')}</div></td>
              <td><div class="chip-list">${(f.source_types||[]).map(s=>`<span class="chip">${s}</span>`).join('')}</div></td>
              <td>${f.min_importance || '—'}</td>
              <td>${f.telegram_enabled ? '<span class="tag tag-ok">Yes</span>' : '<span class="tag tag-off">No</span>'}</td>
              <td>${f.vultureinv_enabled ? '<span class="tag tag-ok">Yes</span>' : '<span class="tag tag-off">No</span>'}</td>
              <td>${f.requires_owner_review ? '<span class="tag tag-warn">Required</span>' : '<span class="tag tag-off">No</span>'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch(e) {
    document.getElementById('filters-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

async function loadRouting() {
  try {
    const data = await fetch(BASE + '/routing').then(r=>r.json());
    document.getElementById('routing-ts').textContent = ts();
    const rules = data.rules || [];
    if (!rules.length) {
      document.getElementById('routing-content').innerHTML = '<div class="empty">No routing rules configured.</div>';
      return;
    }
    document.getElementById('routing-content').innerHTML = `
      <table>
        <thead><tr><th>ID</th><th>Filter ID</th><th>Enabled</th><th>Destinations</th><th>Explain</th><th>Created</th></tr></thead>
        <tbody>
          ${rules.map(r => `
            <tr>
              <td style="font-size:10px;color:var(--dim)">${r.id}</td>
              <td>${r.filter_id}</td>
              <td>${r.enabled ? '<span class="tag tag-ok">On</span>' : '<span class="tag tag-off">Off</span>'}</td>
              <td><div class="chip-list">${(r.destinations||[]).map(d=>`<span class="chip">${d}</span>`).join('')}</div></td>
              <td>${r.explain ? '<span class="tag tag-info">Yes</span>' : '<span class="tag tag-off">No</span>'}</td>
              <td style="font-size:10px">${r.created_at?.slice(0,10)||'—'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch(e) {
    document.getElementById('routing-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

async function loadIntelStatus() {
  try {
    const data = await fetch(BASE + '/intelligence/status').then(r=>r.json());
    const counts = data.queue_counts || {};
    const total = data.queue_total || 0;
    const latest = data.latest_run;
    const countBadges = ['pending','approved','rejected'].map(s =>
      `<span class="chip" style="${s==='pending'?'color:var(--amber)':s==='approved'?'color:var(--green)':'color:var(--red)'}">${s}: ${counts[s]||0}</span>`
    ).join('');
    document.getElementById('intel-counts').innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;font-size:12px">
        <span style="color:var(--dim)">Queue:</span>
        ${countBadges}
        <span style="color:var(--dim);margin-left:4px">total ${total}</span>
        ${latest ? `<span style="color:var(--dim);font-size:10px;margin-left:auto">Last run: ${latest.ran_at?.slice(0,19).replace('T',' ')} — created ${latest.created_count}, skipped ${latest.skipped_count}</span>` : ''}
      </div>
    `;
  } catch(e) {
    document.getElementById('intel-counts').innerHTML = '';
  }
}

async function runMockIntelligence() {
  const btn = document.getElementById('btn-run-intel');
  btn.disabled = true;
  btn.textContent = 'Running...';
  const el = document.getElementById('intel-result');
  el.style.display = 'none';
  try {
    const r = await fetch(BASE + '/intelligence/run/mock', {method:'POST'}).then(r=>r.json());
    const cls = r.created_count > 0 ? 'tag-ok' : 'tag-off';
    const warn = r.warnings?.length ? `<span style="color:var(--amber);font-size:11px"> ⚠ ${r.warnings.join('; ')}</span>` : '';
    const filters = r.matched_filters?.length ? r.matched_filters.join(', ') : '(none)';
    el.innerHTML = `<div class="card" style="border-color:${r.created_count>0?'var(--green)':'var(--border)'}">
      <span class="tag ${cls}">created ${r.created_count}</span>
      <span class="tag tag-off" style="margin-left:4px">skipped ${r.skipped_count}</span>
      <span style="color:var(--dim);font-size:11px;margin-left:8px">matched filters: ${filters}</span>
      ${warn}
    </div>`;
    el.style.display = 'block';
    loadQueue();
    loadIntelStatus();
  } catch(e) {
    el.innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
    el.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Run Mock Intelligence';
  }
}

async function loadQueue() {
  loadIntelStatus();
  try {
    const statusFilter = document.getElementById('queue-status-filter').value;
    const url = BASE + '/review-queue' + (statusFilter ? '?status=' + statusFilter : '');
    const data = await fetch(url).then(r=>r.json());
    document.getElementById('queue-ts').textContent = ts();
    const items = data.items || [];
    document.getElementById('queue-content').innerHTML = items.length ? `
      <table>
        <thead><tr><th>Status</th><th>Type</th><th>Title</th><th>Filter ID</th><th>Rule ID</th><th>Created</th></tr></thead>
        <tbody>
          ${items.map(item => `
            <tr>
              <td>${item.status === 'pending' ? '<span class="tag tag-warn">Pending</span>' : item.status === 'approved' ? '<span class="tag tag-ok">Approved</span>' : '<span class="tag tag-err">Rejected</span>'}</td>
              <td><span class="chip">${item.source_type}</span></td>
              <td style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${item.title || '(no title)'}</td>
              <td style="font-size:10px;color:var(--dim)">${item.matched_filter_id || '—'}</td>
              <td style="font-size:10px;color:var(--dim)">${item.routing_rule_id || '—'}</td>
              <td style="font-size:10px">${item.created_at?.slice(0,16).replace('T',' ')||'—'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    ` : `<div class="empty">No items${statusFilter ? ' with status: ' + statusFilter : ''} — click "Run Mock Intelligence" to populate</div>`;
  } catch(e) {
    document.getElementById('queue-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

async function loadTelegram() {
  try {
    const [status, settings] = await Promise.all([
      fetch(BASE + '/status').then(r=>r.json()),
      fetch(BASE + '/settings/redacted').then(r=>r.json()),
    ]);
    document.getElementById('telegram-ts').textContent = ts();
    const tg = status.telegram || {};
    document.getElementById('telegram-content').innerHTML = `
      <div class="card" style="max-width:400px">
        <h3>Telegram</h3>
        <div class="row"><span class="k">Bot configured</span><span class="v">${tg.configured ? colorVal('Yes','ok') : colorVal('No','warn')}</span></div>
        <div class="row"><span class="k">Allowed chats</span><span class="v">${tg.allowed_chat_count ?? 0}</span></div>
        <div class="row"><span class="k">Token present</span><span class="v">${settings.telegram_configured ? colorVal('Yes','ok') : colorVal('No — set TELEGRAM_BOT_TOKEN in .env','warn')}</span></div>
      </div>
      ${!tg.configured ? `
        <div class="card" style="margin-top:12px;max-width:500px;border-color:var(--amber)">
          <h3>Setup Required</h3>
          <div style="font-size:12px;color:var(--dim);line-height:1.6">
            Add to <code style="color:var(--text)">.env</code>:<br>
            <code style="color:var(--accent)">TELEGRAM_BOT_TOKEN=&lt;bot token&gt;</code><br>
            <code style="color:var(--accent)">TELEGRAM_ALLOWED_CHAT_IDS=&lt;chat_id1&gt;,&lt;chat_id2&gt;</code><br><br>
            Never paste tokens in this UI. Edit the .env file directly.
          </div>
        </div>
      ` : ''}
    `;
  } catch(e) {
    document.getElementById('telegram-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

async function loadAI() {
  try {
    const [status, settings] = await Promise.all([
      fetch(BASE + '/status').then(r=>r.json()),
      fetch(BASE + '/settings/redacted').then(r=>r.json()),
    ]);
    document.getElementById('ai-ts').textContent = ts();
    const ai = status.ai || {};
    document.getElementById('ai-content').innerHTML = `
      <div class="grid2">
        <div class="card">
          <h3>AI Policy</h3>
          <div class="row"><span class="k">Live AI enabled</span><span class="v">${ai.live_ai_enabled ? colorVal('Yes — all AI providers may run','warn') : colorVal('No (safe default)','ok')}</span></div>
          <div class="row"><span class="k">Gemini live</span><span class="v">${ai.gemini_live_enabled ? colorVal('Enabled','warn') : colorVal('Disabled','dim')}</span></div>
          <div class="row"><span class="k">Grok live</span><span class="v">${ai.grok_live_enabled ? colorVal('Enabled','warn') : colorVal('Disabled','dim')}</span></div>
          <div style="margin-top:10px;font-size:11px;color:var(--dim)">AI providers are owner-triggered only. OpenClaw summarizes stored bundles only — no numeric scores.</div>
        </div>
        <div class="card">
          <h3>Provider Config</h3>
          <div class="row"><span class="k">OpenClaw</span><span class="v">${settings.openclaw_configured ? colorVal('Configured','ok') : colorVal('Not set','off')}</span></div>
          <div class="row"><span class="k">OpenClaw model</span><span class="v">${settings.openclaw_model || '—'}</span></div>
          <div class="row"><span class="k">Gemini</span><span class="v">${settings.gemini_configured ? colorVal('Configured','ok') : colorVal('Not set','off')}</span></div>
          <div class="row"><span class="k">Gemini model</span><span class="v">${settings.gemini_model || '—'}</span></div>
          <div class="row"><span class="k">Grok</span><span class="v">${settings.grok_configured ? colorVal('Configured','ok') : colorVal('Not set','off')}</span></div>
          <div class="row"><span class="k">Grok model</span><span class="v">${settings.grok_model || '—'}</span></div>
        </div>
      </div>
      <div class="card" style="margin-top:12px;border-color:var(--border)">
        <h3>Allowed AI Operations</h3>
        <div style="font-size:12px;line-height:1.8">
          <div class="ok">✓ Owner-triggered text summary from stored source bundle</div>
          <div class="ok">✓ Scheduled summary if explicitly enabled in routing policy</div>
          <div class="err">✗ Full-universe automatic AI scoring</div>
          <div class="err">✗ Numeric risk / position-sizing from AI output</div>
          <div class="err">✗ Trade/entry decisions from AI provider</div>
        </div>
      </div>
    `;
  } catch(e) {
    document.getElementById('ai-content').innerHTML = `<div class="empty err">Error: ${e.message}</div>`;
  }
}

// --- Filter modal ---
function openFilterModal() {
  document.getElementById('fm-name').value = '';
  document.getElementById('fm-enabled').value = 'true';
  document.getElementById('fm-market-scope').value = 'KR,US,KR_ETF,US_ETF';
  document.getElementById('fm-source-types').value = 'news,disclosure,macro,flow';
  document.getElementById('fm-symbols').value = '';
  document.getElementById('fm-kw-include').value = '';
  document.getElementById('fm-kw-exclude').value = '';
  document.getElementById('fm-importance').value = 'medium';
  document.getElementById('fm-freshness').value = '1440';
  document.getElementById('fm-telegram').value = 'false';
  document.getElementById('fm-vultureinv').value = 'true';
  document.getElementById('fm-review').value = 'true';
  document.getElementById('filter-modal').classList.add('open');
}
function closeFilterModal() { document.getElementById('filter-modal').classList.remove('open'); }

function splitCsv(v) { return v.split(',').map(s=>s.trim()).filter(Boolean); }

async function saveFilter() {
  const body = {
    name: document.getElementById('fm-name').value.trim(),
    enabled: document.getElementById('fm-enabled').value === 'true',
    market_scope: splitCsv(document.getElementById('fm-market-scope').value),
    source_types: splitCsv(document.getElementById('fm-source-types').value),
    symbols: splitCsv(document.getElementById('fm-symbols').value),
    keywords_include: splitCsv(document.getElementById('fm-kw-include').value),
    keywords_exclude: splitCsv(document.getElementById('fm-kw-exclude').value),
    min_importance: document.getElementById('fm-importance').value,
    freshness_window_minutes: parseInt(document.getElementById('fm-freshness').value) || 1440,
    telegram_enabled: document.getElementById('fm-telegram').value === 'true',
    vultureinv_enabled: document.getElementById('fm-vultureinv').value === 'true',
    requires_owner_review: document.getElementById('fm-review').value === 'true',
  };
  if (!body.name) { alert('Name is required'); return; }
  try {
    const r = await fetch(BASE + '/filters', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)}).then(r=>r.json());
    if (r.ok) { closeFilterModal(); loadFilters(); }
    else alert('Error: ' + JSON.stringify(r));
  } catch(e) { alert('Error: ' + e.message); }
}

// --- Routing modal ---
function openRoutingModal() {
  document.getElementById('rm-filter-id').value = '';
  document.getElementById('rm-enabled').value = 'true';
  document.getElementById('rm-destinations').value = 'review_queue';
  document.getElementById('rm-explain').value = 'true';
  document.getElementById('routing-modal').classList.add('open');
}
function closeRoutingModal() { document.getElementById('routing-modal').classList.remove('open'); }

async function saveRouting() {
  const body = {
    filter_id: document.getElementById('rm-filter-id').value.trim(),
    enabled: document.getElementById('rm-enabled').value === 'true',
    destinations: splitCsv(document.getElementById('rm-destinations').value),
    explain: document.getElementById('rm-explain').value === 'true',
  };
  if (!body.filter_id) { alert('Filter ID is required'); return; }
  try {
    const r = await fetch(BASE + '/routing', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)}).then(r=>r.json());
    if (r.ok) { closeRoutingModal(); loadRouting(); }
    else alert('Error: ' + JSON.stringify(r));
  } catch(e) { alert('Error: ' + e.message); }
}

// Close modals on overlay click
document.querySelectorAll('.modal-overlay').forEach(el => {
  el.addEventListener('click', e => { if (e.target === el) el.classList.remove('open'); });
});

// Initial load
loadStatus();
setInterval(loadStatus, 30000);
</script>
</body>
</html>"""


@router.get("/admin", response_class=HTMLResponse)
def admin_ui() -> HTMLResponse:
    return HTMLResponse(content=_HTML, status_code=200)
