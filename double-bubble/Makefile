SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

DEPS := \
  boto3 botocore python-dotenv pandas pyathena sqlalchemy Jinja2 \
  ruff black mypy pytest requests

.PHONY: env lint test eval kb-load deploy-aws rollback-aws seed score run

env:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install $(DEPS)
	@echo "[env] Ready. Activate: source $(VENV)/bin/activate"

lint:
	$(VENV)/bin/ruff check src || true
	$(VENV)/bin/black --check src || true
	$(VENV)/bin/mypy src || true

test:
	$(VENV)/bin/pytest -q

eval:
	@echo "[eval] Running eval suite: light"
	$(VENV)/bin/pytest -q tests/eval || true

kb-load:
	@if [ -f src/app/rag/ingest.py ]; then \
		$(PY) src/app/rag/ingest.py; \
	else \
		echo "[kb-load] RAG ingest not available for project_type=analysis"; \
	fi

deploy-aws:
	@echo "[deploy-aws] Packaging SAM template (infra/aws/sam-template.yaml)"
	@command -v sam >/dev/null 2>&1 || { echo >&2 "AWS SAM CLI not installed"; exit 0; }
	sam deploy --guided --template-file infra/aws/sam-template.yaml || true

rollback-aws:
	@echo "[rollback-aws] Not implemented; use CloudFormation console or sam delete"

seed:
	$(PY) cli/dnai.py seed || true

score:
	@if [ -f src/app/tabular/score.py ]; then \
		$(PY) src/app/tabular/score.py; \
	else \
		echo "[score] Tabular score not available"; \
	fi

run:
	@echo "No local server. Deploy with 'make deploy-aws' or call handlers in tests."

.PHONY: build-web
build-web:
	$(PY) scripts/build_web.py --out web/double-bubble-analyzer-multi.html
