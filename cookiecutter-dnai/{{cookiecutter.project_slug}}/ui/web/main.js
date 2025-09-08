async function callChat(apiBase, q, auth) {
  const url = apiBase.replace(/\/$/, '') + '/chat';
  const headers = { 'Content-Type': 'application/json' };
  if (auth) headers['Authorization'] = auth;
  const resp = await fetch(url, { method: 'POST', headers, body: JSON.stringify({ q }) });
  const text = await resp.text();
  try { return JSON.stringify(JSON.parse(text), null, 2); } catch { return text; }
}

window.addEventListener('DOMContentLoaded', () => {
  const elQ = document.getElementById('q');
  const elAuth = document.getElementById('auth');
  const elBtn = document.getElementById('send');
  const elOut = document.getElementById('out');
  elBtn.addEventListener('click', async () => {
    const api = window.API_BASE_URL || '';
    if (!api) { elOut.textContent = 'Set API_BASE_URL in ui/web/config.js'; return; }
    elOut.textContent = 'Requesting...';
    try {
      elOut.textContent = await callChat(api, elQ.value, elAuth.value);
    } catch (e) {
      elOut.textContent = 'Error: ' + e;
    }
  });
});

