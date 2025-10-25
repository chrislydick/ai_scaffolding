#!/usr/bin/env python3
"""
Builds the multi-employee Double Bubble Analyzer HTML to a target path.

Usage:
  python scripts/build_web.py [--out web/double-bubble-analyzer-multi.html]
"""
import argparse
from pathlib import Path


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>PSE Double Bubble Analyzer — Multi</title>
<style>
  :root{
    --bg:#0f1115;
    --panel:#171a21;
    --text:#e7e9ee;
    --muted:#a0a4ae;
    --accent:#4aa3ff;
    --ok:#3ecf8e;
    --warn:#ffb648;
    --bad:#ff5d5d;
    --grid:#2a2f3a;
    --chip:#262b36;
  }
  html, body { height:100%; }
  body{
    margin:0; font-family:system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
    background:var(--bg); color:var(--text);
  }
  header{
    padding:16px 20px; border-bottom:1px solid var(--grid);
    position:sticky; top:0; background:rgba(15,17,21,0.9); backdrop-filter: blur(8px);
    z-index: 20;
  }
  header h1{ margin:0 0 4px 0; font-size:18px; font-weight:600; letter-spacing:0.2px; }
  header .sub{ color:var(--muted); font-size:13px; }
  main{ padding:18px 20px 60px; max-width:1200px; margin:0 auto; }
  .row{ display:flex; gap:16px; flex-wrap:wrap;}
  .card{
    background:var(--panel); border:1px solid var(--grid); border-radius:12px; padding:14px 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  }
  .card h2{ margin:2px 0 10px; font-size:16px; }
  .controls{ display:grid; grid-template-columns: repeat(12, minmax(0,1fr)); gap:12px; }
  .controls .field{ grid-column: span 3; display:flex; flex-direction:column; gap:6px; }
  .controls .field.wide{ grid-column: span 6; }
  .controls label{ font-size:12px; color:var(--muted); }
  .controls input, .controls select, .controls button, textarea{
    width:100%; box-sizing:border-box; padding:8px 10px; border-radius:8px; border:1px solid var(--grid);
    background:#0c0f14; color:var(--text); font-size:13px; outline:none;
  }
  .controls button{ cursor:pointer; background:linear-gradient(180deg, #1a2230, #10151d); }
  .controls button.primary{ background: linear-gradient(180deg, #2270ff, #1a57c7); border:0; color:white; }
  .controls .hint{ font-size:11px; color:var(--muted); }
  .chips{ display:flex; flex-wrap:wrap; gap:6px; }
  .chip{ background:var(--chip); border:1px solid var(--grid); padding:6px 8px; border-radius:999px; font-size:12px; color:var(--muted); }
  .viz { position:relative; }
  .legend{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; font-size:12px; color:var(--muted); margin-top:8px; }
  .legend .swatch{ width:16px; height:10px; border-radius:3px; display:inline-block; border:1px solid var(--grid); background: rgba(100,180,255,0.35); }
  .legend .swatch.hatch{ background: repeating-linear-gradient(45deg, rgba(255,93,93,0.15) 0 4px, rgba(255,93,93,0.35) 4px 8px); }
  .legend .swatch.callin{ border:1px dashed var(--muted); background: rgba(100,180,255,0.2); }
  .legend .swatch.dev{ background: rgba(255,182,72,0.25); border:1px solid var(--warn); }
  .split{ display:grid; grid-template-columns: 1fr; gap:16px; }
  @media(min-width: 1024px){ .split{ grid-template-columns: 1.6fr 0.8fr; } }
  svg{ width:100%; display:block; }
  .axis line, .axis path{ stroke:var(--grid); }
  .axis text{ fill:var(--muted); font-size:12px; }
  .foot{ margin-top:4px; font-size:12px; color:var(--muted); }
  table{ width:100%; border-collapse: collapse; font-size:13px; }
  th, td{ padding:8px 10px; border-bottom:1px solid var(--grid); text-align:left; }
  th{ position: sticky; top: 0; background: #11141a; cursor:pointer; user-select:none; }
  tr:hover{ background:#131823; }
  .kbd{ background:#0a0d12; border:1px solid var(--grid); padding:2px 6px; border-radius:6px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size:12px; }
  .note{ color:var(--muted); font-size:12px; }
  .pill{ padding:2px 8px; border-radius:999px; border:1px solid var(--grid); display:inline-block; font-size:12px; }
  .pill.ok{ color:var(--ok); border-color: rgba(62,207,142,0.4); }
  .pill.bad{ color:var(--bad); border-color: rgba(255,93,93,0.5); }
  .pill.warn{ color:var(--warn); border-color: rgba(255,182,72,0.5); }
  .muted{ color:var(--muted); }
  .spacer{ height:8px; }
  .hint-row{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; font-size:12px; color:var(--muted); }
  .right{ text-align:right; }
  /* Multi-select styling */
  #employeeSelect{ min-height: 140px; }
  .emp-buttons{ display:flex; gap:8px; }
  .help-tip{
    display:inline-flex; align-items:center; justify-content:center;
    width:18px; height:18px; border-radius:50%;
    border:1px solid rgba(74,163,255,0.8); font-size:11px; margin-left:6px;
    cursor:help; color:var(--accent); background:rgba(74,163,255,0.12); font-weight:600;
  }
  .help-tip:hover{ border-color:var(--accent); background:rgba(74,163,255,0.2); }
  .dow-picker{ display:flex; gap:6px; flex-wrap:wrap; }
  .dow-picker button{
    flex:1 1 32px; padding:6px 10px; border-radius:8px; border:1px solid var(--grid);
    background:#0c0f14; color:var(--text); font-size:12px; cursor:pointer;
  }
  .dow-picker button.active{ background:var(--accent); color:#fff; border-color:var(--accent); }
  .calendar-grid{ display:flex; gap:16px; flex-wrap:wrap; }
  .calendar-month{ flex:1 1 240px; min-width:220px; border:1px solid var(--grid); border-radius:10px; padding:10px; background:#11141a; }
  .calendar-month-title{ font-size:13px; font-weight:600; margin-bottom:6px; }
  .calendar-month table{ width:100%; border-collapse:collapse; font-size:12px; }
  .calendar-month th{ color:var(--muted); text-align:center; padding-bottom:4px; }
  .calendar-cell{ border:1px solid var(--grid); height:54px; vertical-align:top; padding:4px; position:relative; }
  .calendar-cell.empty{ background:rgba(255,255,255,0.01); border-style:dashed; opacity:0.3; }
  .calendar-cell .day-num{ font-size:11px; color:var(--muted); }
  .calendar-cell .badge{ margin-top:4px; display:inline-block; padding:2px 6px; border-radius:999px; font-size:11px; border:1px solid var(--grid); color:var(--muted); }
  .calendar-cell.has-db{ background:rgba(255,93,93,0.12); border-color:rgba(255,93,93,0.5); }
  .calendar-cell.has-db .badge{ border-color:rgba(255,93,93,0.4); color:var(--bad); }
  .overlay-header{ display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; }
  .overlay-header button{ padding:6px 10px; border-radius:8px; border:1px solid var(--grid); background:#0c0f14; color:var(--text); cursor:pointer; }
  .overlay-scroll-area{ max-height:520px; overflow:auto; border:1px solid var(--grid); border-radius:12px; padding:8px 10px; background:rgba(15,17,21,0.75); }
</style>
</head>
<body>
  <header>
    <h1>PSE Double Bubble Analyzer — Multi</h1>
    <div class="sub">Stack multiple employees as separate rows on a shared 0–24h timeline. Double‑bubble and deviations highlighted.</div>
  </header>
  <main>
    <div class="card">
      <h2>1) Load data</h2>
      <div class="controls">
        <div class="field wide">
          <label>Upload CSV (preferred hourly grid: <span class="kbd">employee_id,calendar_date,00..23[,shift_type,...]</span>; legacy <span class="kbd">start_datetime,end_datetime</span> rows still work)</label>
          <input type="file" id="fileInput" accept=".csv" />
          <div class="hint">Each row should be a single employee + date. Hour columns hold 0–1 hours for that slot (e.g., 0.5 = 30m). Legacy start/end rows or ISO timestamps remain supported. A <span class="kbd">shift_time</span> code (REG, CHOL, OT1, OT2, PLVE, PTO) is required.</div>
        </div>
        <div class="field wide">
          <label>CSV URL (optional)</label>
          <input type="url" id="csvUrl" placeholder="https://example.com/shifts.csv" />
        </div>
        <div class="field" style="align-self:end;">
          <label>&nbsp;</label>
          <button id="fetchBtn">Fetch CSV</button>
        </div>
        <div class="field">
          <label>&nbsp;</label>
          <button id="loadSampleBtn">Load Demo Sample</button>
          <div class="hint">Synthetic data to showcase features.</div>
        </div>
      </div>
      <div class="spacer"></div>
      <div id="loadStatus" class="note"></div>
    </div>

    <div class="spacer"></div>

    <div class="card">
      <h2>2) Parameters</h2>
      <div class="controls">
        <div class="field">
          <label>Rest threshold (hours) for double-bubble</label>
          <input type="number" id="restThreshold" value="8" min="0" step="0.25"/>
        </div>
        <div class="field">
          <label>Deviation threshold (hours) vs. baseline</label>
          <input type="number" id="devThreshold" value="1" min="0" step="0.25"/>
        </div>
        <div class="field">
          <label>Baseline source</label>
          <select id="baselineMode">
            <option value="scheduled">Median of <strong>scheduled</strong> shifts</option>
            <option value="all">Median of all shifts</option>
          </select>
        </div>
        <div class="field">
          <label>Date range — start</label>
          <input type="date" id="dateStart" />
        </div>
        <div class="field">
          <label>Date range — end</label>
          <input type="date" id="dateEnd" />
        </div>

        <div class="field wide">
          <label>Days of week</label>
          <div id="dowPicker" class="dow-picker">
            <button type="button" data-day="1" class="active" title="Monday">M</button>
            <button type="button" data-day="2" class="active" title="Tuesday">T</button>
            <button type="button" data-day="3" class="active" title="Wednesday">W</button>
            <button type="button" data-day="4" class="active" title="Thursday">Th</button>
            <button type="button" data-day="5" class="active" title="Friday">F</button>
            <button type="button" data-day="6" class="active" title="Saturday">Sa</button>
            <button type="button" data-day="0" class="active" title="Sunday">Su</button>
          </div>
          <div class="hint">Only the selected days render in the overlay, flagged list, and calendar.</div>
        </div>

        <div class="field wide">
          <label>Employees (multi‑select)</label>
          <select id="employeeSelect" multiple></select>
          <div class="emp-buttons">
            <button id="selectAllEmpBtn">Select All</button>
            <button id="clearEmpBtn">Clear</button>
          </div>
          <div class="hint">Hold <span class="kbd">Ctrl</span>/<span class="kbd">Cmd</span> or <span class="kbd">Shift</span> to select multiple. Use the buttons to select all/clear quickly.</div>
        </div>

        <div class="field">
          <label>Availability filter column (optional)</label>
          <select id="availabilityColumn"></select>
          <div class="hint">If set, alternates must match the selected employee on this column (e.g., same crew or district).</div>
        </div>

        <div class="field wide">
          <label>Cost centers (required field in data)</label>
          <input type="search" id="costCenterSearch" placeholder="Search cost centers…" />
          <select id="costCenterSelect" multiple></select>
          <div class="hint">Hold Ctrl/Cmd or Shift to multi-select. Leave empty to include all cost centers.</div>
        </div>

        <div class="field">
          <label>Base rate ($/hr)</label>
          <input type="number" id="baseRate" value="100" min="0" step="1" />
        </div>
        <div class="field">
          <label>Double-bubble multiplier</label>
          <input type="number" id="dbMultiplier" value="2" min="1" step="0.1" />
        </div>

        <div class="field" style="align-self:end;">
          <label>&nbsp;</label>
          <button class="primary" id="applyBtn">Apply / Recompute</button>
        </div>
      </div>
      <div class="hint-row">
        <div>Legend:</div>
        <div class="legend">
          <span class="swatch"></span> Shift
          <span class="swatch hatch"></span> Double-bubble (&lt; rest threshold)
          <span class="swatch callin"></span> Call-in / OT2 (dashed outline)
          <span class="swatch dev"></span> Deviates from baseline (&gt; threshold)
        </div>
      </div>
    </div>

    <div class="spacer"></div>

    <div class="split">
      <div class="card viz">
        <h2>3) Overlay timeline (stacked 0–24h rows)</h2>
        <div class="overlay-header">
          <div id="chartTitle" class="note">Select one or more employees to render.</div>
          <button id="sortOverlayBtn" type="button">Name ↑</button>
        </div>
        <div class="overlay-scroll-area">
          <svg id="overlayChart" preserveAspectRatio="xMidYMid meet"></svg>
        </div>
        <div class="foot">Each row is an employee; each rectangle is a shift segment (cross‑midnight split). Hover for details. Use Save to export PNG.</div>
        <div class="spacer"></div>
        <div class="row">
          <button id="savePngBtn">Save chart as PNG</button>
        </div>
      </div>

      <div class="card">
        <h2>4) Summary</h2>
        <div id="summaryChips" class="chips"></div>
        <div class="spacer"></div>
        <div class="note">Signals across the current date range and parameters:</div>
        <div id="summaryList"></div>
      </div>
    </div>

    <div class="spacer"></div>

    <div class="card">
      <h2>5) Flagged incidents (<span id="flagCount">0</span>)</h2>
      <div class="row">
        <button id="exportCsvBtn">Export flagged CSV</button>
      </div>
      <div class="spacer"></div>
      <div style="max-height:420px; overflow:auto;">
        <table id="flagTable">
          <thead>
            <tr>
              <th data-sort="employee_id">Employee</th>
              <th data-sort="start">Start</th>
              <th data-sort="end">End</th>
              <th data-sort="hours">Hours</th>
              <th data-sort="rest_gap_h">Rest Gap (h)</th>
              <th data-sort="double_bubble">Double‑Bubble</th>
              <th data-sort="callin">Call‑in <span class="help-tip" title="Marked when the shift_time code is a call-in/OT1/OT2 entry.">?</span></th>
              <th data-sort="deviation">Deviation <span class="help-tip" title="Difference between this shift’s start/end and the employee’s median baseline; flagged if max delta exceeds the deviation threshold.">?</span></th>
              <th data-sort="avail_count">Alternates Available <span class="help-tip" title="Counts other employees who were off (no overlap) and had ≥ rest threshold hours before the shift; they must also match the availability column if one is set.">?</span></th>
              <th data-sort="est_savings">$ Savings (est.)</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
      <div class="foot">“Alternates Available” counts other employees who were off and would not be <span class="kbd">&lt; rest threshold</span> if they’d taken this shift (optionally constrained by the availability column).</div>
    </div>

    <div class="spacer"></div>

    <div class="card">
      <h2>6) Calendar view (selected employees)</h2>
      <div id="calendarHint" class="note">Select employees to visualize double-bubble days.</div>
      <div id="calendarGrid" class="calendar-grid"></div>
    </div>

    <div class="spacer"></div>

    <div class="card">
      <h2>Assumptions & Notes</h2>
      <ul class="note">
        <li>Double‑bubble eligibility is attributed to the <em>current shift</em> only when its immediately prior shift was overtime (OT1/OT2/call-in) <em>and</em> the rest gap from that shift’s end to this shift’s start is below the threshold.</li>
        <li>“Availability” for alternates: not on a concurrent shift and their rest gap before the flagged shift is ≥ threshold; optionally must match on the chosen column (crew/district/job_class).</li>
        <li>“Normal shift” baseline: median start/end per employee. If “scheduled” has no coverage, falls back to all shifts.</li>
        <li>Cost savings estimate assumes the flagged shift paid at <span class="kbd">base_rate × multiplier</span> could have been covered at <span class="kbd">base_rate</span>.</li>
      </ul>
    </div>
  </main>

  <script defer src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
  <script>
  // ---------- Utilities ----------
  const $ = sel => document.querySelector(sel);
  const fmt2 = n => (Math.round(n*100)/100).toFixed(2);
  const pad = (n) => n<10 ? "0"+n : ""+n;
  const toLocalISO = (d) => d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())+" "+pad(d.getHours())+":"+pad(d.getMinutes());
  const parseMaybe = (s) => {
    if (s instanceof Date) return s;
    if (typeof s === "string") {
      let t = s.trim();
      if (!t) return null;
      t = t.replace(/\//g, "-");
      if (/^\d{4}-\d{2}-\d{2}$/.test(t)) t += " 00:00";
      t = t.replace("T"," ");
      const d = new Date(t);
      if (isNaN(d)) return null;
      return d;
    }
    return null;
  };
  const minutesOfDay = (d) => d.getHours()*60 + d.getMinutes() + d.getSeconds()/60;
  const hoursBetween = (a,b) => (b - a) / 36e5;
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n, d.getHours(), d.getMinutes(), d.getSeconds());
  const HOUR_COLUMNS = Array.from({length:24}, (_,i)=> pad(i));
  const DEFAULT_DAYS = [0,1,2,3,4,5,6];
  const MONTH_NAMES = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  const DOW_LABELS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
  const SHIFT_TIME_ALIASES = {
    "reg": "reg",
    "regular": "reg",
    "scheduled": "reg",
    "chol": "chol",
    "company holiday": "chol",
    "ot2": "ot2",
    "ot": "ot2",
    "overtime 2x": "ot2",
    "call-in": "call-in",
    "callin": "call-in",
    "ot1": "ot1",
    "overtime 1.5x": "ot1",
    "plve": "plve",
    "unpaid leave": "plve",
    "pto": "pto",
    "paid time off": "pto"
  };
  const SHIFT_TIME_DESCRIPTIONS = {
    "reg": "REG — regular time",
    "chol": "CHOL — company holiday",
    "ot2": "OT2 — overtime 2×",
    "ot1": "OT1 — overtime 1.5×",
    "plve": "PLVE — unpaid leave",
    "pto": "PTO — paid time off",
    "call-in": "Call-in"
  };
  const canonicalShiftType = (value) => {
    const norm = (value ?? "").toString().trim().toLowerCase();
    if (!norm) return "";
    return SHIFT_TIME_ALIASES[norm] || norm;
  };
  const SHIFT_TIME_FIELDS = ["shift_time","shiftTime","SHIFT_TIME"];
  const getShiftTypeFromRow = (row) => {
    for (const key of SHIFT_TIME_FIELDS){
      if (row && row[key] != null && row[key] !== "") return canonicalShiftType(row[key]);
    }
    return "";
  };
  const describeShiftType = (value) => SHIFT_TIME_DESCRIPTIONS[canonicalShiftType(value)] || (value ? value.toString() : "—");
  const SCHEDULED_TYPES = new Set(["reg","regular","scheduled","chol"]);
  const CALLIN_TYPES = new Set(["call-in","callin","ot2","ot1","ot"]);
  const OVERTIME_TYPES = new Set(["ot1","ot2","call-in","callin","ot"]);
  const isScheduledType = (value) => SCHEDULED_TYPES.has(canonicalShiftType(value));
  const isCallInType = (value) => CALLIN_TYPES.has(canonicalShiftType(value));
  const isOvertimeType = (value) => OVERTIME_TYPES.has(canonicalShiftType(value));
  const COST_CENTER_FIELDS = ["cost_center","CostCenter","costCenter","COST_CENTER"];
  const getCostCenterFromRow = (row) => {
    for (const key of COST_CENTER_FIELDS){
      if (row && row[key] != null && row[key] !== "") return row[key].toString().trim();
    }
    return "";
  };

  function parseCalendarDate(value){
    if (value == null) return null;
    const text = value.toString().trim();
    if (!text) return null;
    const slash = text.match(/^(\d{1,2})[\/-](\d{1,2})[\/-](\d{2,4})$/);
    if (slash){
      const mm = parseInt(slash[1], 10);
      const dd = parseInt(slash[2], 10);
      let yy = parseInt(slash[3], 10);
      if (yy < 100) yy += 2000;
      return new Date(yy, mm-1, dd);
    }
    const parsed = new Date(text);
    if (isNaN(parsed)) return null;
    return new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate());
  }

  function isHourlyRow(row){
    if (!row) return false;
    const dateVal = row.calendar_date ?? row.calendarDate ?? row.CalendarDate ?? row.date;
    if (!dateVal) return false;
    return HOUR_COLUMNS.some(col => Object.prototype.hasOwnProperty.call(row, col));
  }

  function expandHourlyRow(row, stats){
    if (!isHourlyRow(row)) return null;
    const emp = (row.employee_id ?? row.Employee ?? row.emp ?? "").toString().trim();
    const dateRaw = row.calendar_date ?? row.calendarDate ?? row.CalendarDate ?? row.date ?? "";
    const day = parseCalendarDate(dateRaw);
    const typ = getShiftTypeFromRow(row);
    const costCenter = getCostCenterFromRow(row);
    if (!emp || !day) return [];
    if (!typ){
      if (stats) stats.missingShiftTime = (stats.missingShiftTime || 0) + 1;
      return [];
    }
    if (!costCenter){
      if (stats) stats.missingCostCenter = (stats.missingCostCenter || 0) + 1;
      return [];
    }
    const baseRaw = {...row, cost_center: costCenter};
    const segs = [];
    let current = null;
    for (const col of HOUR_COLUMNS){
      if (!Object.prototype.hasOwnProperty.call(row, col)) continue;
      const rawVal = row[col];
      const val = typeof rawVal === "number" ? rawVal : parseFloat(rawVal);
      if (!val || !isFinite(val) || val <= 0){
        if (current){ segs.push(current); current = null; }
        continue;
      }
      const clamped = Math.min(Math.max(val, 0), 1);
      const hourInt = parseInt(col, 10);
      if (isNaN(hourInt)) continue;
      const slotStart = new Date(day.getFullYear(), day.getMonth(), day.getDate(), hourInt, 0, 0);
      const slotEnd = new Date(slotStart.getTime() + clamped * 36e5);
      if (current && Math.abs(slotStart.getTime() - current.end.getTime()) < 1){
        current.end = slotEnd;
      } else {
        if (current) segs.push(current);
        current = {
          employee_id: emp,
          start: slotStart,
          end: slotEnd,
          shift_type: typ,
          cost_center: costCenter,
          raw: {...baseRaw}
        };
      }
    }
    if (current) segs.push(current);
    return segs;
  }

  function parseCSVbasic(text){
    const rows = [];
    let i=0, field="", row=[], inQuotes=false;
    while(i < text.length){
      const c = text[i];
      if (inQuotes){
        if (c === '"'){
          if (text[i+1] === '"'){ field+='"'; i++; }
          else inQuotes=false;
        } else field += c;
      } else {
        if (c === '"'){ inQuotes=true; }
        else if (c === ','){ row.push(field); field=""; }
        else if (c === '\n' || c === '\r'){
          if (field !== "" || row.length>0){ row.push(field); rows.push(row); row=[]; field=""; }
          if (c === '\r' && text[i+1] === '\n') i++;
        } else field += c;
      }
      i++;
    }
    if (field !== "" || row.length>0){ row.push(field); rows.push(row); }
    const header = rows.shift() || [];
    return rows.map(r => {
      const o={};
      header.forEach((h,idx)=>{ o[h.trim()] = (r[idx] ?? "").trim(); });
      return o;
    });
  }

  // ---------- Core state ----------
  let rawRows = [];
  let shifts = [];
let flaggedShifts = [];
let employees = [];
let optionalCols = [];
let employeeCostCenters = new Map();
let costCenters = [];
let costCenterEmployees = new Map();
let overlaySortAsc = true;
  let params = {
    restThreshold: 8,
    devThreshold: 1,
    baselineMode: "scheduled",
    baseRate: 100,
    dbMultiplier: 2,
    dateStart: null,
    dateEnd: null,
    daysOfWeek: new Set(DEFAULT_DAYS),
    costCenters: new Set()
  };

  // ---------- Loading ----------
  async function loadFromFile(file){
    const text = await file.text();
    return parseCSV(text);
  }
  async function loadFromUrl(url){
    const res = await fetch(url);
    if (!res.ok) throw new Error("Fetch failed: " + res.status);
    const text = await res.text();
    return parseCSV(text);
  }
  function parseCSV(text){
    let rows;
    if (window.Papa){
      const out = Papa.parse(text, {header:true, dynamicTyping:false, skipEmptyLines:true});
      rows = out.data;
    } else {
      rows = parseCSVbasic(text);
    }
    return rows;
  }

  // ---------- Transformations ----------
  function normalizeRows(rows, stats=null){
    const out = [];
    for (const r of rows){
      const hourly = expandHourlyRow(r, stats);
      if (hourly){
        out.push(...hourly);
        continue;
      }
      const emp = (r.employee_id ?? r.Employee ?? r.emp ?? "").toString().trim();
      const st = parseMaybe(r.start_datetime ?? r.start ?? r.start_time ?? r.Start ?? "");
      const en = parseMaybe(r.end_datetime ?? r.end ?? r.end_time ?? r.End ?? "");
      const typ = getShiftTypeFromRow(r);
      const costCenter = getCostCenterFromRow(r);
      if (!typ){
        if (stats) stats.missingShiftTime = (stats.missingShiftTime || 0) + 1;
        continue;
      }
      if (!costCenter){
        if (stats) stats.missingCostCenter = (stats.missingCostCenter || 0) + 1;
        continue;
      }
      if (!emp || !st || !en) continue;
      if (en < st){
        const en2 = addDays(en, 1);
        out.push({employee_id: emp, start: st, end: en2, shift_type: typ, cost_center: costCenter, raw:{...r, cost_center: costCenter}});
      } else {
        out.push({employee_id: emp, start: st, end: en, shift_type: typ, cost_center: costCenter, raw:{...r, cost_center: costCenter}});
      }
      // copy optional keys for availability matching
      for (const k of Object.keys(r)){
        if (!(k in out[out.length-1].raw)) out[out.length-1].raw[k] = r[k];
      }
    }
    return out.sort((a,b)=> a.employee_id.localeCompare(b.employee_id) || a.start - b.start || a.end - b.end);
  }

  function applyDateFilter(arr){
    let {dateStart, dateEnd} = params;
    if (!dateStart && !dateEnd) return arr;
    return arr.filter(s=>{
      const d = s.start;
      if (dateStart && d < dateStart) return false;
      if (dateEnd){
        const endDay = new Date(dateEnd.getFullYear(), dateEnd.getMonth(), dateEnd.getDate(), 23,59,59);
        if (d > endDay) return false;
      }
      return true;
    });
  }

  function applyDayOfWeekFilter(arr){
    const days = params.daysOfWeek;
    if (!days || days.size === 0 || days.size === DEFAULT_DAYS.length) return arr;
    return arr.filter(s=> days.has(s.start.getDay()));
  }

  function applyCostCenterFilter(arr){
    const centers = params.costCenters;
    if (!centers || centers.size === 0) return arr;
    return arr.filter(s=> s.cost_center && centers.has(s.cost_center));
  }

  function computeRestAndFlags(arr){
    const list = arr.slice();
    let prevByEmp = new Map();
    for (const s of list){
      const key = s.employee_id;
      const prev = prevByEmp.get(key) || null;
      s.prev_end = prev ? prev.end : null;
      s.rest_gap_h = prev ? hoursBetween(prev.end, s.start) : null;
      const prevWasOT = prev ? isOvertimeType(prev.shift_type) : false;
      s.double_bubble = (s.rest_gap_h != null) ? (prevWasOT && s.rest_gap_h < params.restThreshold) : false;
      prevByEmp.set(key, s);
    }
    return list;
  }

  function perEmployeeBaseline(arr){
    const byEmp = new Map();
    for (const s of arr){
      if (!byEmp.has(s.employee_id)) byEmp.set(s.employee_id, []);
      byEmp.get(s.employee_id).push(s);
    }
    const baseline = new Map();
    for (const [emp, list] of byEmp){
      const pool = (params.baselineMode === "scheduled")
        ? list.filter(x=> isScheduledType(x.shift_type))
        : list.slice();
      const use = pool.length ? pool : list;
      const smins = use.map(x=> minutesOfDay(x.start)).sort((a,b)=>a-b);
      const emins = use.map(x=> minutesOfDay(x.end)).sort((a,b)=>a-b);
      const med = (arr)=> arr.length? (arr.length%2? arr[(arr.length-1)/2] : (arr[arr.length/2-1]+arr[arr.length/2])/2) : null;
      baseline.set(emp, {start_min: med(smins), end_min: med(emins)});
    }
    return baseline;
  }

  function computeDeviations(arr, baseline){
    for (const s of arr){
      const bl = baseline.get(s.employee_id);
      if (!bl || bl.start_min==null || bl.end_min==null){
        s.deviation = false;
        s.dev_hours = 0;
      } else {
        const dStart = Math.abs(minutesOfDay(s.start) - bl.start_min) / 60;
        const dEnd   = Math.abs(minutesOfDay(s.end) - bl.end_min) / 60;
        const dev = Math.max(dStart, dEnd);
        s.dev_hours = dev;
        s.deviation = dev > params.devThreshold;
      }
    }
    return arr;
  }

  function splitCrossMidnightForViz(arr){
    const segs = [];
    for (const s of arr){
      const startMin = minutesOfDay(s.start);
      const endMin   = minutesOfDay(s.end);
      const crosses  = s.end.toDateString() !== s.start.toDateString();
      if (crosses){
        segs.push({...s, vstart: startMin/60, vend: 24});
        segs.push({...s, vstart: 0, vend: endMin/60});
      } else {
        segs.push({...s, vstart: startMin/60, vend: endMin/60});
      }
    }
    return segs.filter(x=> x.vend > x.vstart);
  }

  function buildAvailabilityIndex(arr){
    const byEmp = new Map();
    for (const s of arr){
      if (!byEmp.has(s.employee_id)) byEmp.set(s.employee_id, []);
      byEmp.get(s.employee_id).push(s);
    }
    for (const [emp, list] of byEmp){
      list.sort((a,b)=> a.start - b.start);
      let prevEnd = null;
      for (const x of list){
        x._prevEndForEmp = prevEnd;
        prevEnd = x.end;
      }
    }
    return byEmp;
  }

  function overlaps(aStart, aEnd, bStart, bEnd){
    return (aStart < bEnd) && (bStart < aEnd);
  }

  function findAlternates(flagShift, idxByEmp, availabilityCol){
    const start = flagShift.start, end = flagShift.end;
    const out = [];
    for (const [emp, list] of idxByEmp.entries()){
      if (emp === flagShift.employee_id) continue;
      if (availabilityCol){
        const v = (flagShift.raw?.[availabilityCol] ?? "").toString();
        const candidateSample = (list[0]?.raw?.[availabilityCol] ?? "").toString();
        if (v && candidateSample && v !== candidateSample) continue;
      }
      let busy = false;
      for (const s of list){
        if (overlaps(start, end, s.start, s.end)){ busy = true; break; }
        if (s.start > end) break;
      }
      if (busy) continue;
      let prevEnd = null;
      for (const s of list){
        if (s.end <= start) prevEnd = s.end; else break;
      }
      const restH = prevEnd ? hoursBetween(prevEnd, start) : Infinity;
      if (restH >= params.restThreshold){
        out.push({employee_id: emp, restH});
      }
    }
    return out;
  }

  // ---------- Visualization (multi-rows) ----------
  function getSelectedEmployees(){
    const sel = document.querySelector("#employeeSelect");
    if (!sel) return [];
    return Array.from(sel.selectedOptions).map(o=>o.value);
  }

  function getSelectedCostCenters(){
    const sel = document.querySelector("#costCenterSelect");
    if (!sel) return [];
    return Array.from(sel.selectedOptions).map(o=>o.value).filter(Boolean);
  }

  function updateEmployeeFilterByCostCenter(forceDefault=false){
    const empSel = document.querySelector("#employeeSelect");
    if (!empSel) return;
    const selectedCenters = getSelectedCostCenters();
    const includeAll = selectedCenters.length === 0;
    const allowed = new Set();
    if (includeAll){
      employees.forEach(emp=> allowed.add(emp));
    } else {
      selectedCenters.forEach(cc=>{
        const set = costCenterEmployees.get(cc);
        if (set) set.forEach(emp=> allowed.add(emp));
      });
    }
    const prev = forceDefault ? new Set() : new Set(getSelectedEmployees());
    const list = Array.from(allowed).sort((a,b)=> a.localeCompare(b));
    empSel.innerHTML = "";
    list.forEach((emp, idx)=>{
      const opt = document.createElement("option");
      opt.value = emp; opt.textContent = emp;
      if (forceDefault){
        opt.selected = idx < Math.min(3, list.length);
      } else if (prev.size){
        opt.selected = prev.has(emp);
      } else {
        opt.selected = idx < Math.min(3, list.length);
      }
      empSel.appendChild(opt);
    });
    if (!list.length){
      empSel.innerHTML = "";
    }
  }

  function renderOverlayForEmployees(empIds){
    const inputList = Array.isArray(empIds) ? empIds : [];
    const svg = document.getElementById("overlayChart");
    const list = inputList.slice().sort((a,b)=> overlaySortAsc ? a.localeCompare(b) : b.localeCompare(a));
    const N = list.length;
    const W = 1000;
    const padL=220, padR=30, padT=18, padB=30;
    const rowH = 90;           // height per employee row
    const gap = 10;            // vertical gap between rows
    const H = padT + (N? (N*rowH + (N-1)*gap) : 120) + padB;

    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.style.height = Math.max(220, H) + "px";
    svg.setAttribute("data-height", Math.max(220, H));
    svg.innerHTML = "";

    const g = document.createElementNS("http://www.w3.org/2000/svg","g");
    svg.appendChild(g);

    const x = (h) => padL + (h/24) * (W - padL - padR);
    const yRowTop = (i) => padT + i*(rowH + gap);
    const yRowBot = (i) => yRowTop(i) + rowH;

    // axis grid across all rows
    const axis = document.createElementNS("http://www.w3.org/2000/svg","g");
    axis.setAttribute("class","axis");
    for (let h=0; h<=24; h+=2){
      const X = x(h);
      const ln = document.createElementNS("http://www.w3.org/2000/svg","line");
      ln.setAttribute("x1", X); ln.setAttribute("x2", X);
      ln.setAttribute("y1", padT); ln.setAttribute("y2", H-padB);
      ln.setAttribute("stroke", getComputedStyle(svg).getPropertyValue("--grid") || "#2a2f3a");
      ln.setAttribute("stroke-width", "1");
      ln.setAttribute("opacity", h%6===0 ? "0.7" : "0.35");
      axis.appendChild(ln);

      const tx = document.createElementNS("http://www.w3.org/2000/svg","text");
      tx.setAttribute("x", X); tx.setAttribute("y", H-8);
      tx.setAttribute("text-anchor","middle");
      tx.setAttribute("fill", "#a0a4ae");
      tx.setAttribute("font-size","12");
      tx.textContent = h.toString();
      axis.appendChild(tx);
    }
    g.appendChild(axis);

    // rows
    const defs = document.createElementNS("http://www.w3.org/2000/svg","defs");
    defs.innerHTML = `
      <pattern id="hatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
        <rect width="8" height="8" fill="rgba(255,93,93,0.18)"></rect>
        <line x1="0" y1="0" x2="0" y2="8" stroke="rgba(255,93,93,0.5)" stroke-width="2"></line>
      </pattern>
    `;
    g.appendChild(defs);

    const tooltip = document.createElement("div");
    Object.assign(tooltip.style, {
      position:"absolute", padding:"8px 10px", background:"#0b0e14", color:"#e7e9ee",
      border:"1px solid #2a2f3a", borderRadius:"8px", pointerEvents:"none", fontSize:"12px",
      transform:"translate(-50%, -110%)", display:"none", zIndex:5
    });
    const container = svg.parentElement;
    if (container){
      const existing = container.querySelector(".overlay-tooltip");
      if (existing) existing.remove();
      tooltip.className = "overlay-tooltip";
      container.appendChild(tooltip);
    }

    function showTip(evt, text){
      tooltip.innerHTML = text;
      tooltip.style.display = "block";
      const rect = svg.getBoundingClientRect();
      tooltip.style.left = (evt.clientX - rect.left) + "px";
      tooltip.style.top  = (evt.clientY - rect.top) + "px";
    }
    function hideTip(){ tooltip.style.display="none"; }

    list.forEach((empId, idx) => {
      const top = yRowTop(idx), bot = yRowBot(idx);
      const label = document.createElementNS("http://www.w3.org/2000/svg","text");
      label.setAttribute("x", padL - 12);
      label.setAttribute("y", top + rowH/2);
      label.setAttribute("text-anchor","end");
      label.setAttribute("dominant-baseline","middle");
      label.setAttribute("fill", "#e7e9ee");
      label.setAttribute("font-size","13");
      label.textContent = empId;
      g.appendChild(label);

      const bg = document.createElementNS("http://www.w3.org/2000/svg","rect");
      bg.setAttribute("x", padL); bg.setAttribute("y", top+2);
      bg.setAttribute("width", W - padL - padR); bg.setAttribute("height", rowH - 4);
      bg.setAttribute("fill", "rgba(255,255,255,0.02)");
      g.appendChild(bg);

      if (idx>0){
        const sep = document.createElementNS("http://www.w3.org/2000/svg","line");
        sep.setAttribute("x1", padL); sep.setAttribute("x2", W - padR);
        sep.setAttribute("y1", top - gap/2); sep.setAttribute("y2", top - gap/2);
        sep.setAttribute("stroke", getComputedStyle(svg).getPropertyValue("--grid") || "#2a2f3a");
        sep.setAttribute("stroke-width", "1");
        sep.setAttribute("opacity", "0.6");
        g.appendChild(sep);
      }

      const empShifts = shifts.filter(s=> s.employee_id===empId);
      const segs = splitCrossMidnightForViz(empShifts);

      for (const s of segs){
        const X = x(s.vstart), Wd = x(s.vend) - x(s.vstart);
        const r = document.createElementNS("http://www.w3.org/2000/svg","rect");
        r.setAttribute("x", X); r.setAttribute("y", top + 8);
        r.setAttribute("width", Math.max(1, Wd)); r.setAttribute("height", rowH - 16);
        r.setAttribute("fill", "rgba(100,180,255,0.32)");
        const isCallin = isCallInType(s.shift_type);
        r.setAttribute("stroke", s.deviation ? "#ffb648" : (isCallin ? "#a0a4ae" : "rgba(0,0,0,0)"));
        r.setAttribute("stroke-width", isCallin ? "1.5" : (s.deviation ? "1.5":"0"));
        r.setAttribute("stroke-dasharray", isCallin ? "4 4" : (s.deviation ? "0" : "0"));
        if (s.double_bubble) r.setAttribute("fill", "url(#hatch)");

        const durH = hoursBetween(s.start, s.end);
        const callin = isCallin;
        const shiftLabel = describeShiftType(s.shift_type);
        const tip = `
          <div><strong>${s.employee_id}</strong></div>
          <div>${shiftLabel}</div>
          <div>${toLocalISO(s.start)} → ${toLocalISO(s.end)} (${fmt2(durH)}h)</div>
          <div>Call-in: <span class="${callin?'pill ok':'pill'}">${callin?'Yes':'No'}</span> &nbsp; Double-bubble: <span class="${s.double_bubble?'pill bad':'pill'}">${s.double_bubble?'Yes':'No'}</span></div>
          <div>Rest before: ${s.rest_gap_h==null?'-':fmt2(s.rest_gap_h)+'h'} &nbsp; Deviation: ${s.deviation?fmt2(s.dev_hours)+'h':'No'}</div>
        `;
        r.addEventListener("mousemove", (e)=> showTip(e, tip));
        r.addEventListener("mouseleave", hideTip);
        g.appendChild(r);
      }
    });

    document.querySelector("#chartTitle").textContent = N ? `${N} employee${N>1?'s':''} selected` : "Select one or more employees to render.";
  }

  function renderSummary(){
    const byEmp = {};
    for (const s of shifts){
      const emp = s.employee_id;
      if (!byEmp[emp]) byEmp[emp] = {total:0, db:0, near:0, minRest:Infinity, medRest:null, rests:[]};
      byEmp[emp].total++;
      if (s.double_bubble) byEmp[emp].db++;
      if (s.rest_gap_h!=null){
        byEmp[emp].rests.push(s.rest_gap_h);
        byEmp[emp].minRest = Math.min(byEmp[emp].minRest, s.rest_gap_h);
        if (s.rest_gap_h >= params.restThreshold-1 && s.rest_gap_h < params.restThreshold) byEmp[emp].near++;
      }
    }
    const chips = document.querySelector("#summaryChips"); chips.innerHTML = "";
    const list = document.querySelector("#summaryList"); list.innerHTML = "";
    if (!Object.keys(byEmp).length){ list.innerHTML = '<div class="note">No data in current range.</div>'; return; }

    const arr = Object.entries(byEmp).map(([emp, v])=>{
      v.rests.sort((a,b)=>a-b);
      const med = v.rests.length ? (v.rests.length%2? v.rests[(v.rests.length-1)/2] : (v.rests[v.rests.length/2-1]+v.rests[v.rests.length/2])/2) : null;
      v.medRest = med;
      return {employee_id: emp, total:v.total, db:v.db, near:v.near, minRest:v.minRest, medRest:v.medRest, rate: v.total? v.db/v.total : 0};
    }).sort((a,b)=> b.db - a.db || b.rate - a.rate);

    const top = arr.slice(0,5);
    for (const v of top){
      const el = document.createElement("div");
      el.className = "chip";
      el.textContent = `${v.employee_id}: ${v.db} DB (${fmt2(v.rate*100)}%) • min rest ${v.minRest===Infinity?'-':fmt2(v.minRest)}h`;
      chips.appendChild(el);
    }

    const ul = document.createElement("ul");
    ul.className = "note";
    ul.innerHTML = `
      <li><strong>${arr.length}</strong> employees in range; top DB count: <strong>${arr[0].employee_id}</strong> (${arr[0].db}).</li>
      <li>Median rest gaps near threshold: ${arr.reduce((acc,v)=> acc+v.near,0)} events in [${params.restThreshold-1}, ${params.restThreshold})h.</li>
    `;
    list.appendChild(ul);
  }

  function renderFlagTable(){
    const tbody = document.querySelector("#flagTable tbody");
    tbody.innerHTML = "";
    const selected = getSelectedEmployees();
    const selectedSet = new Set(selected);
    if (!selected.length){
      document.querySelector("#flagCount").textContent = "0";
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 10;
      td.innerHTML = '<div class="note">Select one or more employees to see flagged incidents.</div>';
      tr.appendChild(td);
      tbody.appendChild(tr);
      return;
    }
    const filtered = flaggedShifts.filter(f=> selectedSet.has(f.employee_id));
    document.querySelector("#flagCount").textContent = filtered.length;
    if (!filtered.length){
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 10;
      td.innerHTML = '<div class="note">No double-bubble incidents for the selected employees.</div>';
      tr.appendChild(td);
      tbody.appendChild(tr);
      return;
    }
    for (const f of filtered){
      const tr = document.createElement("tr");
      const dur = hoursBetween(f.start, f.end);
      const availNames = f._alternates?.slice(0,6).map(a=>a.employee_id).join(", ");
      const savings = f._estSavings ?? 0;
      tr.innerHTML = `
        <td>${f.employee_id}</td>
        <td>${toLocalISO(f.start)}</td>
        <td>${toLocalISO(f.end)}</td>
        <td>${fmt2(dur)}</td>
        <td>${f.rest_gap_h==null?'-':fmt2(f.rest_gap_h)}</td>
        <td>${f.double_bubble?'<span class="pill bad">Yes</span>':'<span class="pill">No</span>'}</td>
        <td>${isCallInType(f.shift_type)?'<span class="pill ok">Yes</span>':'<span class="pill">No</span>'}</td>
        <td>${f.deviation?'<span class="pill warn">'+fmt2(f.dev_hours)+'h</span>':'<span class="pill">No</span>'}</td>
        <td title="${availNames||''}">${f._alternates?.length||0}</td>
        <td class="right">${fmt2(savings)}</td>
      `;
      tbody.appendChild(tr);
    }
    makeTableSortable("flagTable");
  }

  function renderCalendarView(){
    const container = document.querySelector("#calendarGrid");
    const hint = document.querySelector("#calendarHint");
    if (!container || !hint) return;
    container.innerHTML = "";
    const selected = getSelectedEmployees();
    if (!selected.length){
      hint.textContent = "Select employees to visualize double-bubble days.";
      return;
    }
    const selectedSet = new Set(selected);
    const relevant = shifts.filter(s=> selectedSet.has(s.employee_id));
    if (!relevant.length){
      hint.textContent = "No shifts in range for the selected employees.";
      return;
    }
    hint.textContent = "Highlighted days show double-bubble events for the selected employees.";
    const months = buildCalendarData(relevant);
    if (!months.length){
      container.innerHTML = '<div class="note">No calendar data to display.</div>';
      return;
    }
    months.forEach(monthData=>{
      const monthEl = document.createElement("div");
      monthEl.className = "calendar-month";
      monthEl.innerHTML = buildMonthTable(monthData);
      container.appendChild(monthEl);
    });
  }

  function buildCalendarData(list){
    const byMonth = new Map();
    for (const s of list){
      if (!s.start) continue;
      const year = s.start.getFullYear();
      const month = s.start.getMonth();
      const day = s.start.getDate();
      const key = `${year}-${month}`;
      if (!byMonth.has(key)) byMonth.set(key, {year, month, days:new Map()});
      const monthEntry = byMonth.get(key);
      if (!monthEntry.days.has(day)){
        monthEntry.days.set(day, {double:false, employees:new Set(), dbEmployees:new Set(), shifts:[]});
      }
      const info = monthEntry.days.get(day);
      info.employees.add(s.employee_id);
      if (s.double_bubble){
        info.double = true;
        info.dbEmployees.add(s.employee_id);
      }
      info.shifts.push(s);
    }
    return Array.from(byMonth.values()).sort((a,b)=> (a.year - b.year) || (a.month - b.month));
  }

  function buildMonthTable(data){
    const firstDow = new Date(data.year, data.month, 1).getDay();
    const daysInMonth = new Date(data.year, data.month+1, 0).getDate();
    const header = DOW_LABELS.map(d=> `<th>${d}</th>`).join("");
    let rows = "";
    let day = 1;
    for (let week=0; week<6 && day <= daysInMonth; week++){
      let row = "<tr>";
      for (let dow=0; dow<7; dow++){
        if ((week===0 && dow < firstDow) || day > daysInMonth){
          row += '<td class="calendar-cell empty"></td>';
        } else {
          const info = data.days.get(day);
          const classes = ["calendar-cell"];
          if (info && info.double) classes.push("has-db");
          let badge = "";
          if (info){
            badge = info.double
              ? `<div class="badge db">${info.dbEmployees.size} DB</div>`
              : `<div class="badge">${info.employees.size} shift${info.employees.size>1?"s":""}</div>`;
          }
          const tooltip = info ? `Employees: ${Array.from(info.employees).join(", ")}` : "";
          const safeTitle = tooltip.replace(/"/g, "&quot;");
          row += `<td class="${classes.join(" ")}"${tooltip?` title="${safeTitle}"`:""}><div class="day-num">${day}</div>${badge}</td>`;
          day++;
        }
      }
      row += "</tr>";
      rows += row;
    }
    return `
      <div class="calendar-month-title">${MONTH_NAMES[data.month]} ${data.year}</div>
      <table>
        <thead><tr>${header}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  function makeTableSortable(tableId){
    const table = document.getElementById(tableId);
    if (!table || table.dataset.sortableInit === "1") return;
    table.dataset.sortableInit = "1";
    const ths = table.querySelectorAll("th");
    let sortKey = null, asc = true;
    ths.forEach(th => {
      th.addEventListener("click", ()=>{
        const key = th.dataset.sort;
        if (!key) return;
        if (sortKey === key) asc = !asc; else { sortKey = key; asc = true; }
        const rows = Array.from(table.querySelectorAll("tbody tr"));
        rows.sort((a,b)=>{
          const av = val(a, key), bv = val(b, key);
          if (av < bv) return asc? -1 : 1;
          if (av > bv) return asc? 1 : -1;
          return 0;
        });
        const tb = table.querySelector("tbody");
        rows.forEach(r=>tb.appendChild(r));
      });
    });
    function val(tr, key){
      const tds = tr.children;
      switch(key){
        case "employee_id": return tds[0].innerText;
        case "start": return tds[1].innerText;
        case "end": return tds[2].innerText;
        case "hours": return parseFloat(tds[3].innerText)||0;
        case "rest_gap_h": return parseFloat(tds[4].innerText)||0;
        case "double_bubble": return tds[5].innerText.includes("Yes")?1:0;
        case "callin": return tds[6].innerText.includes("Yes")?1:0;
        case "deviation": return tds[7].innerText.includes("No")?0:parseFloat(tds[7].innerText)||0;
        case "avail_count": return parseInt(tds[8].innerText)||0;
        case "est_savings": return parseFloat(tds[9].innerText)||0;
        default: return tds[0].innerText;
      }
    }
  }

  function exportFlaggedCSV(flagged){
    const header = ["employee_id","start_datetime","end_datetime","duration_hours","rest_gap_hours","double_bubble","shift_type","deviation_hours","alternates_available","est_savings"];
    const lines = [header.join(",")];
    for (const f of flagged){
      const dur = hoursBetween(f.start, f.end);
      const line = [
        f.employee_id,
        toLocalISO(f.start),
        toLocalISO(f.end),
        fmt2(dur),
        f.rest_gap_h==null? "": fmt2(f.rest_gap_h),
        f.double_bubble? "1":"0",
        f.shift_type||"",
        f.deviation? fmt2(f.dev_hours) : "0",
        (f._alternates?.length||0),
        fmt2(f._estSavings||0)
      ].map(v=> `"${String(v).replace(/"/g,'""')}"`).join(",");
      lines.push(line);
    }
    const blob = new Blob([lines.join("\n")], {type:"text/csv;charset=utf-8;"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "double_bubble_flagged.csv"; a.click();
    URL.revokeObjectURL(url);
  }

  function initDayOfWeekPicker(){
    const buttons = Array.from(document.querySelectorAll("#dowPicker button"));
    if (!buttons.length) return;
    buttons.forEach(btn=>{
      btn.addEventListener("click", ()=>{
        btn.classList.toggle("active");
        if (!document.querySelector("#dowPicker button.active")){
          buttons.forEach(b=> b.classList.add("active"));
        }
        recomputeAll();
      });
    });
  }

  function filterCostCenterOptions(term){
    const select = document.querySelector("#costCenterSelect");
    if (!select) return;
    const value = (term || "").toLowerCase();
    Array.from(select.options).forEach(opt=>{
      opt.hidden = value && !opt.value.toLowerCase().includes(value);
    });
  }

  function saveSvgAsPng(svgId){
    const svg = document.getElementById(svgId);
    const xml = new XMLSerializer().serializeToString(svg);
    const svg64 = btoa(unescape(encodeURIComponent(xml)));
    const height = parseInt(svg.getAttribute("data-height")) || 260;
    const width = 1200;
    const img = new Image();
    img.onload = function(){
      const canvas = document.createElement("canvas");
      canvas.width = width; canvas.height = height * (width / (svg.viewBox.baseVal.width || 1000));
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#0f1115"; ctx.fillRect(0,0,canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(function(blob){
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = "overlay_chart.png"; a.click();
        URL.revokeObjectURL(url);
      });
    };
    img.src = "data:image/svg+xml;base64,"+svg64;
  }

  // ---------- Wiring ----------
  function formatLoadStatus(prefix, info){
    const missingShift = info?.stats?.missingShiftTime || 0;
    const missingCost = info?.stats?.missingCostCenter || 0;
    const parts = [];
    if (missingShift) parts.push(`${missingShift} row${missingShift===1?"":"s"} missing shift_time`);
    if (missingCost) parts.push(`${missingCost} row${missingCost===1?"":"s"} missing cost_center`);
    if (parts.length) return `${prefix} Skipped ${parts.join("; ")}.`;
    return prefix;
  }

  document.querySelector("#fileInput").addEventListener("change", async (e)=>{
    const f = e.target.files[0];
    if (!f) return;
    try{
      document.querySelector("#loadStatus").textContent = "Parsing CSV…";
      rawRows = await loadFromFile(f);
      const info = afterLoad();
      document.querySelector("#loadStatus").textContent = formatLoadStatus(`Loaded ${rawRows.length} rows from file.`, info);
    }catch(err){
      console.error(err);
      document.querySelector("#loadStatus").textContent = "Error loading file: " + err.message;
    }
  });
  document.querySelector("#fetchBtn").addEventListener("click", async ()=>{
    const url = document.querySelector("#csvUrl").value.trim();
    if (!url) return;
    try{
      document.querySelector("#loadStatus").textContent = "Fetching CSV…";
      rawRows = await loadFromUrl(url);
      const info = afterLoad();
      document.querySelector("#loadStatus").textContent = formatLoadStatus(`Loaded ${rawRows.length} rows from URL.`, info);
    }catch(err){
      console.error(err);
      document.querySelector("#loadStatus").textContent = "Error fetching: " + err.message;
    }
  });
  document.querySelector("#loadSampleBtn").addEventListener("click", ()=>{
    const hourCols = HOUR_COLUMNS.slice();
    const header = ["employee_id","calendar_date", ...hourCols, "shift_time","cost_center","shift_type","crew","district","job_class"];
    const sampleRows = [
      {
        employee_id:"E001",
        calendar_date:"08/11/2025",
        shift_time:"REG",
        cost_center:"CC-100",
        shift_type:"scheduled",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "07":1,"08":1,"09":1,"10":1,"11":1,"12":1,"13":1,"14":0.5 }
      },
      {
        employee_id:"E001",
        calendar_date:"08/12/2025",
        shift_time:"REG",
        cost_center:"CC-100",
        shift_type:"scheduled",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "07":1,"08":1,"09":1,"10":1,"11":1,"12":1,"13":1,"14":1,"15":0.5 }
      },
      {
        employee_id:"E001",
        calendar_date:"08/13/2025",
        shift_time:"OT2",
        cost_center:"CC-200",
        shift_type:"call-in",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "19":1,"20":1,"21":1,"22":1,"23":0.75 }
      },
      {
        employee_id:"E002",
        calendar_date:"08/11/2025",
        shift_time:"REG",
        cost_center:"CC-200",
        shift_type:"reg",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "06":1,"07":1,"08":1,"09":1,"10":1,"11":1,"12":1,"13":1 }
      },
      {
        employee_id:"E002",
        calendar_date:"08/12/2025",
        shift_time:"REG",
        cost_center:"CC-200",
        shift_type:"reg",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "06":1,"07":1,"08":1,"09":1,"10":1,"11":1,"12":1,"13":1,"14":1,"15":1,"16":0.5,"21":1,"22":1,"23":0.5 }
      },
      {
        employee_id:"E002",
        calendar_date:"08/13/2025",
        shift_time:"OT2",
        cost_center:"CC-200",
        shift_type:"ot2",
        crew:"A",
        district:"North",
        job_class:"Lineman",
        hours:{ "04":1,"05":1,"06":0.5 }
      },
      {
        employee_id:"E003",
        calendar_date:"08/11/2025",
        shift_time:"PTO",
        cost_center:"CC-300",
        shift_type:"pto",
        crew:"B",
        district:"South",
        job_class:"Apprentice",
        hours:{}
      },
      {
        employee_id:"E003",
        calendar_date:"08/12/2025",
        shift_time:"REG",
        cost_center:"CC-300",
        shift_type:"scheduled",
        crew:"B",
        district:"South",
        job_class:"Apprentice",
        hours:{ "05":1,"06":1,"07":1,"08":1,"09":1,"10":1,"11":1,"12":1 }
      }
    ];
    const lines = [header.join(",")];
    sampleRows.forEach(row=>{
      const cells = [row.employee_id, row.calendar_date];
      hourCols.forEach(col=>{
        const val = row.hours && Object.prototype.hasOwnProperty.call(row.hours, col) ? row.hours[col] : "";
        cells.push(val === undefined ? "" : val);
      });
      cells.push(row.shift_time || "");
      cells.push(row.cost_center || "");
      cells.push(row.shift_type || "");
      cells.push(row.crew);
      cells.push(row.district);
      cells.push(row.job_class);
      lines.push(cells.join(","));
    });
    rawRows = parseCSV(lines.join("\n"));
    const info = afterLoad();
    document.querySelector("#loadStatus").textContent = formatLoadStatus(`Loaded demo sample (${rawRows.length} rows; hourly grid).`, info);
  });

  document.querySelector("#applyBtn").addEventListener("click", ()=> recomputeAll());
  document.querySelector("#employeeSelect").addEventListener("change", ()=>{
    const selected = getSelectedEmployees();
    renderOverlayForEmployees(selected);
    renderFlagTable();
    renderCalendarView();
  });
  document.querySelector("#exportCsvBtn").addEventListener("click", ()=> {
    const selected = getSelectedEmployees();
    if (!selected.length){
      alert("Select at least one employee before exporting flagged incidents.");
      return;
    }
    const selectedSet = new Set(selected);
    const flagged = flaggedShifts.filter(s=> selectedSet.has(s.employee_id));
    if (!flagged.length){
      alert("No flagged incidents for the selected employees.");
      return;
    }
    exportFlaggedCSV(flagged);
  });
  document.querySelector("#savePngBtn").addEventListener("click", ()=> saveSvgAsPng("overlayChart"));
  document.querySelector("#selectAllEmpBtn").addEventListener("click", ()=> {
    const sel = document.querySelector("#employeeSelect");
    Array.from(sel.options).forEach(o=> o.selected = true);
    const selected = getSelectedEmployees();
    renderOverlayForEmployees(selected);
    renderFlagTable();
    renderCalendarView();
  });
  document.querySelector("#clearEmpBtn").addEventListener("click", ()=> {
    const sel = document.querySelector("#employeeSelect");
    Array.from(sel.options).forEach(o=> o.selected = false);
    const selected = getSelectedEmployees();
    renderOverlayForEmployees(selected);
    renderFlagTable();
    renderCalendarView();
  });
  const costCenterSelectEl = document.querySelector("#costCenterSelect");
  if (costCenterSelectEl){
    costCenterSelectEl.addEventListener("change", ()=> {
      updateEmployeeFilterByCostCenter();
      recomputeAll();
    });
  }
  const costCenterSearchEl = document.querySelector("#costCenterSearch");
  if (costCenterSearchEl){
    costCenterSearchEl.addEventListener("input", (e)=> filterCostCenterOptions(e.target.value));
  }
  const sortBtn = document.querySelector("#sortOverlayBtn");
  const updateOverlaySortButton = ()=>{
    if (sortBtn) sortBtn.textContent = overlaySortAsc ? "Name ↑" : "Name ↓";
  };
  if (sortBtn){
    updateOverlaySortButton();
    sortBtn.addEventListener("click", ()=>{
      overlaySortAsc = !overlaySortAsc;
      updateOverlaySortButton();
      renderOverlayForEmployees(getSelectedEmployees());
    });
  }

  function afterLoad(){
    const stats = {missingShiftTime:0, missingCostCenter:0};
    const normalized = normalizeRows(rawRows, stats);
    // optional columns for availability filter
    const sample = rawRows[0] || {};
    const known = new Set(["employee_id","start_datetime","end_datetime","shift_type","shift_time","SHIFT_TIME","shiftTime","cost_center","CostCenter","costCenter","COST_CENTER","Employee","Start","End","start","end","type","calendar_date","calendarDate","CalendarDate","date"]);
    HOUR_COLUMNS.forEach(col=> known.add(col));
    optionalCols = Object.keys(sample).filter(k=> !known.has(k));
    const selAvail = document.querySelector("#availabilityColumn"); selAvail.innerHTML = '<option value="">(none)</option>';
    optionalCols.forEach(c=>{
      const opt = document.createElement("option"); opt.value=c; opt.textContent=c; selAvail.appendChild(opt);
    });
    // employees list
    const empSet = new Set(normalized.map(s=> s.employee_id));
    employees = Array.from(empSet).filter(Boolean).sort();
    const empSel = document.querySelector("#employeeSelect"); empSel.innerHTML = "";
    employees.forEach(e=>{
      const opt = document.createElement("option"); opt.value=e; opt.textContent=e; empSel.appendChild(opt);
    });
    // sensible default: select up to first 3
    employees.slice(0, Math.min(3, employees.length)).forEach((e, i)=> { empSel.options[i].selected = true; });

    employeeCostCenters = new Map();
    costCenterEmployees = new Map();
    const ccSet = new Set();
    normalized.forEach(s=>{
      if (!s.cost_center) return;
      ccSet.add(s.cost_center);
      if (!employeeCostCenters.has(s.employee_id)) employeeCostCenters.set(s.employee_id, new Set());
      employeeCostCenters.get(s.employee_id).add(s.cost_center);
      if (!costCenterEmployees.has(s.cost_center)) costCenterEmployees.set(s.cost_center, new Set());
      costCenterEmployees.get(s.cost_center).add(s.employee_id);
    });
    costCenters = Array.from(ccSet).sort();
    const ccSelect = document.querySelector("#costCenterSelect");
    if (ccSelect){
      ccSelect.innerHTML = "";
      costCenters.forEach(cc=>{
        const opt = document.createElement("option"); opt.value = cc; opt.textContent = cc; opt.selected = true; ccSelect.appendChild(opt);
      });
    }
    const ccSearch = document.querySelector("#costCenterSearch");
    if (ccSearch){ ccSearch.value = ""; filterCostCenterOptions(""); }
    updateEmployeeFilterByCostCenter(true);

    // default date range from data
    const dates = normalized.map(s=> s.start).filter(Boolean).sort((a,b)=>a-b);
    if (dates.length){
      const s = dates[0], e = dates[dates.length-1];
      document.querySelector("#dateStart").value = s.toISOString().slice(0,10);
      document.querySelector("#dateEnd").value   = e.toISOString().slice(0,10);
    } else {
      document.querySelector("#dateStart").value = "";
      document.querySelector("#dateEnd").value = "";
    }
    recomputeAll();
    return {stats, normalizedCount: normalized.length};
  }

  function pullParams(){
    params.restThreshold = parseFloat(document.querySelector("#restThreshold").value)||8;
    params.devThreshold  = parseFloat(document.querySelector("#devThreshold").value)||1;
    params.baselineMode  = document.querySelector("#baselineMode").value || "scheduled";
    params.baseRate      = parseFloat(document.querySelector("#baseRate").value)||0;
    params.dbMultiplier  = parseFloat(document.querySelector("#dbMultiplier").value)||1;
    const dS = document.querySelector("#dateStart").value ? new Date(document.querySelector("#dateStart").value + "T00:00:00") : null;
    const dE = document.querySelector("#dateEnd").value ? new Date(document.querySelector("#dateEnd").value + "T00:00:00") : null;
    params.dateStart = dS; params.dateEnd = dE;
    const dayButtons = document.querySelectorAll("#dowPicker button");
    const activeDays = Array.from(dayButtons).filter(btn=> btn.classList.contains("active")).map(btn=> parseInt(btn.dataset.day, 10));
    params.daysOfWeek = new Set((activeDays.length ? activeDays : DEFAULT_DAYS));
    const ccSelect = document.querySelector("#costCenterSelect");
    const ccChosen = ccSelect ? Array.from(ccSelect.selectedOptions).map(o=>o.value).filter(Boolean) : [];
    params.costCenters = new Set(ccChosen);
  }

  function recomputeAll(){
    pullParams();
    const availabilityCol = document.querySelector("#availabilityColumn").value || "";

    // 1) Normalize
    const base = normalizeRows(rawRows);
    // 2) Rest + flags (use full history so first in-range shift still gets prior context)
    const annotated = computeRestAndFlags(base);
    // 3) Date filter (view)
    const ranged = applyDateFilter(annotated);
    // 4) Day-of-week filter
    const dowFiltered = applyDayOfWeekFilter(ranged);
    // 5) Cost center filter
    const ccFiltered = applyCostCenterFilter(dowFiltered);
    let computed = ccFiltered;
    // 6) Baseline
    const bl = perEmployeeBaseline(computed);
    // 7) Deviations
    computed = computeDeviations(computed, bl);
    // 8) Save global
    shifts = computed;

    // 9) Alternates for flagged shifts
    const idx = buildAvailabilityIndex(computed);
    const flagged = computed.filter(s=> s.double_bubble);
    for (const s of flagged){
      const alts = findAlternates(s, idx, availabilityCol);
      s._alternates = alts;
      const hours = Math.max(0, hoursBetween(s.start, s.end));
      const premium = params.baseRate * params.dbMultiplier;
      const normal  = params.baseRate;
      s._estSavings = alts.length>0 ? (premium - normal) * hours : 0;
    }

    flaggedShifts = flagged;

    // Render
    renderOverlayForEmployees(getSelectedEmployees());
    renderSummary();
    renderFlagTable();
    renderCalendarView();
  }

  initDayOfWeekPicker();

  // Init
  document.querySelector("#loadStatus").textContent = "Awaiting CSV… Upload a file or paste a URL.";
  </script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="web/double-bubble-analyzer-multi.html")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HTML, encoding="utf-8")
    print(f"wrote: {out}")


if __name__ == "__main__":
    main()
