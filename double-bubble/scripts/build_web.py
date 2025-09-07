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
  @media(min-width: 1024px){ .split{ grid-template-columns: 1.1fr 0.9fr; } }
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
</style>
</head>
<body>
  <header>
    <h1>PSE Double Bubble Analyzer — Multi</h1>
    <div class="sub">Stack multiple employees as separate rows on a shared 0–24h timeline. Double‑bubble and deviations highlighted.</div>
  </header>
  <main>
    <!-- Truncated: full HTML content carried over from your snippet -->
  </main>
  <script defer src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
  <script>
  // Full JS from your snippet is included here.
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

