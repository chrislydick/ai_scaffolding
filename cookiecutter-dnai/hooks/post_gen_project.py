#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

PROJECT_TYPE = "{{ cookiecutter.project_type }}"
CLOUD = "{{ cookiecutter.cloud }}"
STORAGE = "{{ cookiecutter.storage }}"
AUTH = "{{ cookiecutter.auth }}"
EVAL_SUITE = "{{ cookiecutter.eval_suite }}"
SCRIPT_NAME = "{{ cookiecutter.script_name }}"
SCAFFOLD_SCRIPT = "{{ cookiecutter.scaffold_script }}"

root = Path.cwd()

def rm(path: Path):
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)

def maybe_remove_by_project_type():
    rag = root / "src" / "app" / "rag"
    chk = root / "src" / "app" / "checklists"
    tab = root / "src" / "app" / "tabular"
    if PROJECT_TYPE == "rag":
        rm(chk)
        rm(tab)
    elif PROJECT_TYPE == "checklist":
        rm(rag)
        rm(tab)
    elif PROJECT_TYPE == "tabular_ml":
        rm(rag)
        rm(chk)
    elif PROJECT_TYPE in {"analysis", "script", "dashboard"}:
        # Keep core + governance; remove feature-specific legos
        rm(rag)
        rm(chk)
        rm(tab)
    # hybrid keeps all
    # Remove default script scaffold if not requested or for other project types
    if PROJECT_TYPE not in {"analysis", "script"}:
        rm(root / "scripts" / f"{SCRIPT_NAME}.py")
    else:
        if str(SCAFFOLD_SCRIPT).lower() not in {"yes", "y", "true", "1"}:
            rm(root / "scripts" / f"{SCRIPT_NAME}.py")

def maybe_remove_by_cloud():
    aws = root / "infra" / "aws"
    azure = root / "infra" / "azure"
    models = root / "src" / "app" / "core" / "models"
    if CLOUD == "aws":
        rm(azure)
        # Optional: remove Azure OpenAI client if present
        rm(models / "aoai_client.py")
    else:
        rm(aws)
        # Optional: remove Bedrock client if Azure is chosen
        rm(models / "bedrock_client.py")

def maybe_remove_by_storage():
    io_dir = root / "src" / "app" / "core" / "io_adapters"
    if STORAGE == "s3-athena":
        rm(io_dir / "fabric_io.py")
        rm(io_dir / "onelake_io.py")
        rm(io_dir / "blob_io.py")
    else:
        rm(io_dir / "s3_io.py")
        rm(io_dir / "athena_io.py")

def maybe_trim_eval_suite():
    # For light suite, keep a single eval test
    eval_dir = root / "tests" / "eval"
    if EVAL_SUITE == "light":
        # Keep retrieval, remove classify
        rm(eval_dir / "test_eval_classify.py")

def main():
    maybe_remove_by_project_type()
    maybe_remove_by_cloud()
    maybe_remove_by_storage()
    maybe_trim_eval_suite()

if __name__ == "__main__":
    main()
