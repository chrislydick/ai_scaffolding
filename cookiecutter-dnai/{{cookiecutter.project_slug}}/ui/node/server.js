import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
app.use(express.json())
app.use(express.static(path.join(__dirname, 'static')))

// Simple proxy to backend /chat; set BACKEND_URL env
const BACKEND = process.env.BACKEND_URL || ''
app.post('/api/chat', async (req, res) => {
  if (!BACKEND) return res.status(500).json({ error: 'Set BACKEND_URL' })
  try {
    const r = await fetch(BACKEND.replace(/\/$/, '') + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(req.headers.authorization ? { Authorization: req.headers.authorization } : {}) },
      body: JSON.stringify(req.body)
    })
    const text = await r.text()
    res.type('application/json').send(text)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.listen(5173, () => console.log('Node UI on http://localhost:5173'))
