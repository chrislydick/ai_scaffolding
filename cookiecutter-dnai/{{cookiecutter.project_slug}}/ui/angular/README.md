Angular UI (placeholder)

Scaffold
- Ensure Node and Angular CLI are installed: `npm install -g @angular/cli`
- Create app under `ui/angular/` (or replace this folder):
  `ng new app --directory . --style css --routing false`

Proxy to backend (dev)
- Create `proxy.conf.json`:
  {
    "/api": {
      "target": "https://<your-api-base>",
      "secure": true,
      "changeOrigin": true,
      "pathRewrite": { "^/api": "" }
    }
  }
- Start: `ng serve --proxy-config proxy.conf.json`

Call /chat
- Use Angular HttpClient to POST to `/api/chat` with `{ q: string }`.

