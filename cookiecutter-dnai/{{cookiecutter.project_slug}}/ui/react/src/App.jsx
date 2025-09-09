import { useState } from 'react'

function App() {
  const [api, setApi] = useState('')
  const [auth, setAuth] = useState('')
  const [q, setQ] = useState('')
  const [out, setOut] = useState('(awaiting request)')

  async function send() {
    if (!api) { setOut('Set API base URL'); return }
    setOut('Requesting...')
    try {
      const url = api.replace(/\/$/, '') + '/chat'
      const headers = { 'Content-Type': 'application/json' }
      if (auth) headers['Authorization'] = auth
      const resp = await fetch(url, { method: 'POST', headers, body: JSON.stringify({ q }) })
      const text = await resp.text()
      try { setOut(JSON.stringify(JSON.parse(text), null, 2)) } catch { setOut(text) }
    } catch (e) {
      setOut('Error: ' + e)
    }
  }

  return (
    <main>
      <h1>{{ cookiecutter.project_name }} — React</h1>
      <p className="sub">Simple React UI that POSTs to the /chat endpoint.</p>
      <div className="card">
        <label>API base URL</label>
        <input value={api} onChange={e => setApi(e.target.value)} placeholder="https://..." />
        <label>Authorization header (optional)</label>
        <input value={auth} onChange={e => setAuth(e.target.value)} placeholder="Bearer ..." />
        <label>Prompt</label>
        <textarea value={q} onChange={e => setQ(e.target.value)} rows={4} />
        <div style={{ marginTop: 8 }}>
          <button className="primary" onClick={send}>Send</button>
        </div>
      </div>
      <h2>Response</h2>
      <pre className="out">{out}</pre>
    </main>
  )
}

export default App

