#!/usr/bin/env python3
import argparse
import os
import subprocess


def cmd_init(args):
    print("Initialized project:")
    print(f"  cloud={{{ cookiecutter.cloud }}} storage={{{ cookiecutter.storage }}} type={{{ cookiecutter.project_type }}}")


def cmd_ingest(args):
    os.environ.setdefault("KB_GLOB", args.kb)
    subprocess.call(["python", "src/app/rag/ingest.py"])  # best effort


def cmd_chat(args):
    # Call local FastAPI route if running, else direct model
    try:
        import requests

        r = requests.post("http://127.0.0.1:8000/chat", json={"q": args.q}, timeout=3)
        print(r.json())
        return
    except Exception:
        pass
    try:
        from src.app.core.models.bedrock_client import BedrockClient

        client = BedrockClient()
        print(client.generate(task="rag", prompt=args.q))
    except Exception as ex:
        print(f"chat failed: {ex}")


def cmd_train(args):
    subprocess.call(["python", "src/app/tabular/train.py"])  # stub


def cmd_score(args):
    subprocess.call(["python", "src/app/tabular/score.py"])  # stub


def cmd_eval(args):
    subprocess.call(["pytest", "-q", "tests/eval"])  # stub


def cmd_deploy(args):
    subprocess.call(["make", "deploy-aws"])  # aws path only


def main():
    p = argparse.ArgumentParser(prog="one", description="One command for DNAI")
    sub = p.add_subparsers(required=True)

    sp = sub.add_parser("init"); sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("ingest"); sp.add_argument("--kb", default="data/kb/*"); sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser("chat"); sp.add_argument("--q", required=True); sp.set_defaults(func=cmd_chat)

    sp = sub.add_parser("train"); sp.set_defaults(func=cmd_train)
    sp = sub.add_parser("score"); sp.set_defaults(func=cmd_score)
    sp = sub.add_parser("eval"); sp.set_defaults(func=cmd_eval)
    sp = sub.add_parser("deploy"); sp.set_defaults(func=cmd_deploy)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

