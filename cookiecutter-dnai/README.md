cookiecutter-dnai

Overview
- A flexible Cookiecutter template for data + AI projects on AWS or Azure.
- Mix-and-match legos: RAG, checklists, tabular ML, or lightweight analysis/script projects.
- Post‑generation hook prunes unused legos based on your choices.

Choices (extra-context keys)
- project_slug: short folder/repo name (required)
- project_name: human‑readable name
- project_type: rag | checklist | tabular_ml | hybrid | analysis | script | dashboard†
- cloud: aws | azure†
- storage: s3-athena | onelake-fabric† | sap-bw-hana†
- ui: none | web | streamlit | react | angular† | node† | amplify† | staticwebapps†
- auth: iam | entra†
- eval_suite: light | full†
- script_name: default script filename under scripts/ (analysis/script only; default: app)
- scaffold_script: yes | no (whether to create scripts/{{script_name}}.py)

Legend
- † Limited support / placeholders included but not fully implemented yet.
  - azure: AOAI client and Azure IaC are placeholders; primary path is AWS.
  - onelake-fabric: IO adapters are placeholders; S3/Athena is primary today.
  - sap-bw-hana: adapter stub; requires SAP HANA client/driver and/or BW OData exposure.
  - ui web: simple static UI scaffold; bring your own hosting (Amplify/CloudFront/Azure Static Web Apps).
  - ui streamlit: simple Streamlit app scaffold; install/run locally or deploy as needed.
  - ui react: Vite React scaffold; requires Node tooling.
  - ui angular/node: scaffolds and docs only; requires Node tooling and further setup.
  - ui amplify/staticwebapps: no UI scaffold; choose for documentation/intent only.
  - auth entra: thin header check placeholder; no full AAD integration.
  - eval_suite full: structure only; baseline tests are stubs by default.
  - project_type dashboard: Power BI dashboard folder and guidance only; no PBIX generated.

Generate (local template path)
- Example: Checklist on AWS with Amplify UI
  python3 -m cookiecutter --no-input -o . cookiecutter-dnai \
    project_slug=service-planner-assistant \
    project_name="Service Planner Assistant" \
    project_type=checklist \
    cloud=aws \
    storage=s3-athena \
    ui=amplify \
    auth=iam \
    eval_suite=light

- Example: Analysis project (scripts/) on AWS
  python3 -m cookiecutter --no-input -o . cookiecutter-dnai \
    project_slug=double-bubble \
    project_name="Double Bubble Analyzer" \
    project_type=analysis \
    cloud=aws \
    storage=s3-athena \
    auth=iam \
    eval_suite=light \
    script_name=build \
    scaffold_script=yes

- Example: Script on Azure with OneLake/Fabric + Entra
  python3 -m cookiecutter --no-input -o . cookiecutter-dnai \
    project_slug=panorama_with_bb \
    project_name="Panorama With Bounding Box" \
    project_type=script \
    cloud=azure \
    storage=onelake-fabric \
    ui=staticwebapps \
    auth=entra \
    eval_suite=light \
    script_name=app \
    scaffold_script=yes

What gets generated
- README with Make targets (env, test, eval, kb-load, deploy-aws), and CLI usage.
- Makefile uses uv by default for env and commands (ruff/mypy/pytest); falls back to pip if uv is not installed.
- CLI `dnai` with common subcommands; for analysis/script, includes `dnai script -- ...` passthrough.
- AWS SAM template (when cloud=aws). Azure IaC stubs are included when cloud=azure.
- Governance legos (PII redaction, content filters, telemetry), and optional Purview client.

Notes
- Post‑gen pruning removes adapters/clients you didn’t pick (e.g., Fabric/OneLake on AWS).
- For analysis/script, `scripts/` is added. The default script can be disabled via `scaffold_script=no`.
- After generation:
  - make env
  - make test
  - if RAG/hybrid: make kb-load
  - if AWS: make deploy-aws
