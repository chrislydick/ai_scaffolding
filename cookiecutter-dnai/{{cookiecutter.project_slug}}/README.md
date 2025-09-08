{{ cookiecutter.project_name }}

Quickstart
- make env: creates venv and installs deps.
- make kb-load: runs RAG ingest (if project_type=rag|hybrid).
- make deploy-aws: deploys API via SAM (if cloud=aws).
 - make tfgen: generates Terraform files from `config/data_model.yaml`.
{% if cookiecutter.ui in ["web","streamlit","react","angular","node"] %}
 - make ui-install: installs UI deps (if needed)
 - make ui-serve: serves UI at http://localhost:5173
{% endif %}

Scaffold New Project
Use this repo’s cookiecutter to spin up a new project elsewhere:

```
python3 -m cookiecutter --no-input -o . cookiecutter-dnai \
  project_slug=my-new-project \
  project_name="My New Project" \
  project_type=checklist \
  cloud=aws \
  storage=s3-athena \
  ui=amplify \
  auth=iam \
  eval_suite=light
```

Options
- project_type: rag | checklist | tabular_ml | hybrid | analysis | script | dashboard*
- cloud: aws | azure*
- storage: s3-athena | onelake-fabric* | sap-bw-hana*
- ui: none | web | streamlit | react | angular* | node* | amplify* | staticwebapps*
- auth: iam | entra*
- eval_suite: light | full*

Setup
1) Create a virtualenv and install dependencies:
   make env
   - If [uv](https://docs.astral.sh/uv/) is installed, the Makefile uses uv for a fast venv and installs.
   - Otherwise it falls back to `python -m venv` + `pip`.
   - Dependencies live in `pyproject.toml`; uv will create `uv.lock` — commit it.
   - Install uv (optional): macOS/Linux `curl -Ls https://astral.sh/uv/install.sh | sh`

2) Configure environment variables (copy .env.example to .env and edit):
   - AWS_REGION, AWS_PROFILE for AWS
   - APP_ENV, PROJECT_TYPE, STORAGE

3) Load knowledge base (RAG only):
   make kb-load

4) Deploy to AWS (if cloud=aws):
   make deploy-aws

CLI
- dnai chat --q "hello"
- dnai ingest --kb data/kb/*
- dnai catalog  # sync assets/glossary to Purview (if configured)
- dnai tfgen    # write Terraform to infra/terraform from config/data_model.yaml
{% if cookiecutter.project_type in ["analysis", "script"] %}
- dnai script -- --name world  # runs scripts/{{ cookiecutter.script_name }}.py with passthrough args
- make run-script              # convenience target
{% endif %}

Notes
- No Docker or local web server required; handlers are Lambda-style.
- The template conditionally includes legos for:
  project_type={{ cookiecutter.project_type }}, cloud={{ cookiecutter.cloud }}, storage={{ cookiecutter.storage }}, ui={{ cookiecutter.ui }}, auth={{ cookiecutter.auth }}, eval_suite={{ cookiecutter.eval_suite }}.

Legend
- * Limited support / placeholders included but not fully implemented yet.
  - azure: AOAI client and Azure IaC are placeholders; primary path is AWS.
  - onelake-fabric: IO adapters are placeholders; S3/Athena is primary today.
  - sap-bw-hana: adapter provided with optional SQL/OData hooks; requires SAP clients and network access.
  - ui web: simple static UI scaffold only; bring your own hosting (Amplify/CloudFront etc.).
  - ui streamlit: simple Streamlit app; install with `uvx streamlit` or add to deps.
  - ui react: Vite React scaffold; run with Node tooling.
  - ui angular/node: scaffolds/docs; requires Node tooling and setup.
  - ui amplify/staticwebapps: no UI scaffold; choose for documentation/intent only.
  - auth entra: thin header check placeholder; no full AAD integration.
  - eval_suite full: structure only; baseline tests are stubs by default.
  - project_type dashboard: Power BI dashboard folder and guidance only; no PBIX generated.

Terraform generation
- Define datasets in `config/data_model.yaml`.
- Run `dnai tfgen` or `make tfgen` to generate `.tf` files under `infra/terraform`.
- For AWS, this emits:
  - `aws_glue_catalog_database` and one `aws_glue_catalog_table` per dataset
  - Optional S3 bucket resources (set `create: true` per bucket)
  - `aws_athena_workgroup` wired to `output_location`
- For Azure, a stub is generated (extend as needed for ADLS/Fabric).
- Apply via Terraform:
  - `cd infra/terraform && terraform init && terraform plan`

{% if cookiecutter.ui == 'web' %}
Web UI (static)
- Files under `ui/web/` provide a minimal HTML/JS UI that calls the `/chat` endpoint.
- Set your deployed API base URL in `ui/web/config.js` (e.g., API Gateway URL).
- Run `make ui-serve`, then open http://localhost:5173 to test.
- For IAM-protected APIs, provide a valid `Authorization` header value in the UI.
{% elif cookiecutter.ui == 'streamlit' %}
Web UI (Streamlit)
- Files under `ui/streamlit/` provide a Streamlit app that calls `/chat`.
- Install/run: `make ui-serve` (uses `uvx streamlit` if available).
- Configure API base URL in the app input.
{% elif cookiecutter.ui == 'react' %}
Web UI (React)
- Files under `ui/react/` include a Vite React app.
- Install deps: `make ui-install`; Start dev: `make ui-serve`.
- Configure API base URL in the input field.
{% elif cookiecutter.ui == 'angular' %}
Web UI (Angular)
- Placeholder scaffold and instructions in `ui/angular/README.md`.
{% elif cookiecutter.ui == 'node' %}
Web UI (Node/Express)
- Files under `ui/node/` provide an Express server serving a small UI and proxy.
- Set `BACKEND_URL` env to your API base; `make ui-install && make ui-serve`.
{% endif %}

Storage: SAP BW/HANA (on‑prem)
- Set environment variables for SQL access: `SAP_HOST`, `SAP_PORT`, `SAP_USER`, `SAP_PASSWORD`, `SAP_SCHEMA`.
- Install SAP HANA client (hdbcli) or a SQLAlchemy dialect for HANA to enable SQL queries.
- For BW OData, set `SAP_ODATA_BASE_URL` (and optional `SAP_ODATA_AUTH`) and use `src/app/core/io_adapters/sap_bw_io.py`.
- This adapter is provided as a stub; networking/VPN and SAP client libraries are required and not bundled.
