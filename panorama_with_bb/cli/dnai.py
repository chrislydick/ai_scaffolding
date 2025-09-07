#!/usr/bin/env python3
import argparse
import os
import subprocess
import json
import sys


def cmd_init(args):
    print("Initialized project:")
    print("  cloud=aws storage=s3-athena type=script")


def cmd_ingest(args):
    os.environ.setdefault("KB_GLOB", args.kb)
    subprocess.call(["python", "src/app/rag/ingest.py"])  # best effort


def cmd_chat(args):
    # Direct model call (no local server)
    try:
        from src.app.core.models.bedrock_client import BedrockClient

        client = BedrockClient()
        print(client.generate(task="rag", prompt=args.q))
    except Exception as ex:
        print(json.dumps({"answer": f"Local mode: {args.q}", "error": str(ex)}))


def cmd_train(args):
    subprocess.call(["python", "src/app/tabular/train.py"])  # stub


def cmd_score(args):
    subprocess.call(["python", "src/app/tabular/score.py"])  # stub


def cmd_eval(args):
    subprocess.call(["pytest", "-q", "tests/eval"])  # stub


def cmd_deploy(args):
    subprocess.call(["make", "deploy-aws"])  # aws path only


def cmd_catalog(args):
    try:
        from src.app.governance.purview_client import register_s3_asset, upsert_glossary_term
        import yaml

        with open("config/purview.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        assets = cfg.get("assets", [])
        for a in assets:
            if a.get("type") == "s3":
                ok = register_s3_asset(a.get("name"), a.get("uri"))
                print(f"[purview] register {a.get('uri')}: {'ok' if ok else 'skip'}")
        for g in cfg.get("glossary", []):
            ok = upsert_glossary_term("default", g.get("term"), g.get("definition", ""))
            print(f"[purview] glossary {g.get('term')}: {'ok' if ok else 'skip'}")
    except Exception as ex:
        print(f"[purview] skipped: {ex}")


def cmd_panorama(args):
    cmd = [
        sys.executable,
        "scripts/panorama_with_bb.py",
        "--lat", str(args.lat),
        "--lon", str(args.lon),
        "--radius", str(args.radius),
    ]
    if args.years:
        cmd += ["--years", args.years]
    if args.flickr_key:
        cmd += ["--flickr_key", args.flickr_key]
    if args.wikimedia:
        cmd += ["--wikimedia"]
    if args.mapillary_token:
        cmd += ["--mapillary_token", args.mapillary_token]
    if args.google_key:
        cmd += ["--google_key", args.google_key]
    subprocess.call(cmd)


def cmd_script(args):
    # Generic wrapper: run scripts/panorama_with_bb.py with passthrough args
    cmd = [sys.executable, "scripts/panorama_with_bb.py"] + (args.args or [])
    subprocess.call(cmd)


def main():
    p = argparse.ArgumentParser(prog="dnai", description="DNAI command line")
    sub = p.add_subparsers(required=True)

    sp = sub.add_parser("init"); sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("ingest"); sp.add_argument("--kb", default="data/kb/*"); sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser("chat"); sp.add_argument("--q", required=True); sp.set_defaults(func=cmd_chat)

    sp = sub.add_parser("train"); sp.set_defaults(func=cmd_train)
    sp = sub.add_parser("score"); sp.set_defaults(func=cmd_score)
    sp = sub.add_parser("eval"); sp.set_defaults(func=cmd_eval)
    sp = sub.add_parser("deploy"); sp.set_defaults(func=cmd_deploy)
    sp = sub.add_parser("catalog"); sp.set_defaults(func=cmd_catalog)
    sp = sub.add_parser("panorama");
    sp.add_argument("--lat", type=float, required=True)
    sp.add_argument("--lon", type=float, required=True)
    sp.add_argument("--radius", type=float, required=True)
    sp.add_argument("--years", default=None)
    sp.add_argument("--flickr_key", default=None)
    sp.add_argument("--wikimedia", action="store_true")
    sp.add_argument("--mapillary_token", default=None)
    sp.add_argument("--google_key", default=None)
    sp.set_defaults(func=cmd_panorama)
    sp = sub.add_parser("script", help="Run scripts/panorama_with_bb.py; pass args after --")
    sp.add_argument('args', nargs=argparse.REMAINDER)
    sp.set_defaults(func=cmd_script)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
