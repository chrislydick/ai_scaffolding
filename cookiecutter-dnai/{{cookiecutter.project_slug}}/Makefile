SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

DEPS := \
  boto3 botocore python-dotenv pandas pyathena sqlalchemy Jinja2 \
  ruff black mypy pytest requests PyYAML

.PHONY: env lint test eval kb-load deploy-aws rollback-aws seed score run tfgen{% if cookiecutter.ui in ["web","streamlit","react","angular","node"] %} ui-serve ui-install{% endif %}

env:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		echo "[env] Using uv for venv and dependencies"; \
		uv venv $(VENV); \
		uv sync --group dev; \
	else \
		echo "[env] Using python venv + pip (uv not found)"; \
		python3 -m venv $(VENV); \
		$(PIP) install --upgrade pip; \
		$(PIP) install $(DEPS); \
	fi
	@echo "[env] Ready. Activate: source $(VENV)/bin/activate"

lint:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run ruff check src || true; \
		uv run black --check src || true; \
		uv run mypy src || true; \
	else \
		$(VENV)/bin/ruff check src || true; \
		$(VENV)/bin/black --check src || true; \
		$(VENV)/bin/mypy src || true; \
	fi

test:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run pytest -q; \
	else \
		$(VENV)/bin/pytest -q; \
	fi

eval:
	@echo "[eval] Running eval suite: {{ cookiecutter.eval_suite }}"
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run pytest -q tests/eval || true; \
	else \
		$(VENV)/bin/pytest -q tests/eval || true; \
	fi

tfgen:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run python cli/dnai.py tfgen; \
	else \
		$(PY) cli/dnai.py tfgen; \
	fi
{% if cookiecutter.ui == 'web' %}

.PHONY: ui-serve
ui-serve:
	@set -e; \
	cd ui/web && python3 -m http.server 5173
.PHONY: ui-install
ui-install:
	@echo "[ui-install] static web UI requires no install"
{% endif %}
{% if cookiecutter.ui == 'streamlit' %}

.PHONY: ui-serve
ui-serve:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uvx streamlit run ui/streamlit/app.py --server.port 5173; \
	else \
		python -m streamlit run ui/streamlit/app.py --server.port 5173; \
	fi
.PHONY: ui-install
ui-install:
	@echo "[ui-install] using uvx streamlit or ensure streamlit is installed"
{% endif %}
{% if cookiecutter.ui == 'react' %}

.PHONY: ui-serve
ui-serve:
	@set -e; \
	command -v npm >/dev/null 2>&1 || { echo "npm not found"; exit 1; }; \
	cd ui/react && npm run dev
.PHONY: ui-install
ui-install:
	@set -e; \
	command -v npm >/dev/null 2>&1 || { echo "npm not found"; exit 1; }; \
	cd ui/react && npm install
{% endif %}
{% if cookiecutter.ui == 'angular' %}

.PHONY: ui-serve
ui-serve:
	@echo "[ui-serve] Angular scaffold is a placeholder. See ui/angular/README.md"
.PHONY: ui-install
ui-install:
	@echo "[ui-install] Angular scaffold is a placeholder. See ui/angular/README.md"
{% endif %}
{% if cookiecutter.ui == 'node' %}

.PHONY: ui-serve
ui-serve:
	@set -e; \
	command -v npm >/dev/null 2>&1 || { echo "npm not found"; exit 1; }; \
	cd ui/node && npm start
.PHONY: ui-install
ui-install:
	@set -e; \
	command -v npm >/dev/null 2>&1 || { echo "npm not found"; exit 1; }; \
	cd ui/node && npm install
{% endif %}

kb-load:
	@if [ -f src/app/rag/ingest.py ]; then \
		if command -v uv >/dev/null 2>&1; then \
			uv run python src/app/rag/ingest.py; \
		else \
			$(PY) src/app/rag/ingest.py; \
		fi; \
	else \
		echo "[kb-load] RAG ingest not available for project_type={{ cookiecutter.project_type }}"; \
	fi

deploy-aws:
	@echo "[deploy-aws] Packaging SAM template (infra/aws/sam-template.yaml)"
	@command -v sam >/dev/null 2>&1 || { echo >&2 "AWS SAM CLI not installed"; exit 0; }
	sam deploy --guided --template-file infra/aws/sam-template.yaml || true

rollback-aws:
	@echo "[rollback-aws] Not implemented; use CloudFormation console or sam delete"

seed:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run python cli/dnai.py seed || true; \
	else \
		$(PY) cli/dnai.py seed || true; \
	fi

score:
	@if [ -f src/app/tabular/score.py ]; then \
		if command -v uv >/dev/null 2>&1; then \
			uv run python src/app/tabular/score.py; \
		else \
			$(PY) src/app/tabular/score.py; \
		fi; \
	else \
		echo "[score] Tabular score not available"; \
	fi

run:
	@echo "No local server. Deploy with 'make deploy-aws' or call handlers in tests."
{% if cookiecutter.project_type in ["analysis", "script"] %}

.PHONY: run-script
run-script:
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv run python scripts/{{ cookiecutter.script_name }}.py --name world; \
	else \
		$(PY) scripts/{{ cookiecutter.script_name }}.py --name world; \
	fi
{% endif %}
{% if cookiecutter.project_type == 'dashboard' %}

.PHONY: dashboard-open
dashboard-open:
	@echo "Open Power BI Desktop and load dashboards/powerbi/*.pbix (placeholder)."
{% endif %}
