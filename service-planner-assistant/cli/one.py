#!/usr/bin/env python3
"""Backward-compat shim: forward to dnai CLI."""
import os
import sys
import subprocess


def main():
    here = os.path.dirname(__file__)
    target = os.path.join(here, "dnai.py")
    sys.exit(subprocess.call([sys.executable, target] + sys.argv[1:]))


if __name__ == "__main__":
    main()

