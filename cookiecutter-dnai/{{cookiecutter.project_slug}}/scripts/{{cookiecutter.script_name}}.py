"""
Default script scaffold for analysis/script projects.

Usage:
  python scripts/{{ cookiecutter.script_name }}.py --name world
  dnai script -- --name world
"""
import argparse


def main():
    ap = argparse.ArgumentParser(description="{{ cookiecutter.project_name }} script")
    ap.add_argument("--name", default="world")
    args = ap.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()

