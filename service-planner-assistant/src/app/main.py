"""
Entrypoint helper: dispatch CLI help.

Usage:
  python -m src.app.main cli   # show CLI help
"""
import sys
import subprocess


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "cli":
        print("Usage: python -m src.app.main cli")
        return
    subprocess.call([sys.executable, "cli/dnai.py", "--help"])


if __name__ == "__main__":
    main()
