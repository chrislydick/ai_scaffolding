"""
Entrypoint helper: dispatch CLI or API.

Usage:
  python -m app.main api   # run API (dev)
  python -m app.main cli   # show CLI help
"""
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.main [api|cli]")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "api":
        import uvicorn

        uvicorn.run("app.api.handlers:app", host="0.0.0.0", port=8000, reload=True)
    elif cmd == "cli":
        import subprocess

        subprocess.call([sys.executable, "cli/dnai.py", "--help"])
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
