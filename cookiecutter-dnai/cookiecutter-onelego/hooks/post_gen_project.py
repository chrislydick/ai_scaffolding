#!/usr/bin/env python3
import subprocess, sys, os

def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)

if not os.path.isdir(".git"):
    run(["git", "init"])

# ensure scripts are executable
os.makedirs("scripts", exist_ok=True)
try:
    os.chmod("scripts/ban_binaries.sh", 0o755)
except FileNotFoundError:
    pass

# install pre-commit locally if available
try:
    run([sys.executable, "-m", "pip", "install", "-U", "pre-commit"])
    run(["pre-commit", "install"])
except Exception as e:
    print("WARN: pre-commit install skipped:", e)

print("✅ Security pack ready. Run `make security` to scan.")

