cookiecutter-dnai

Overview
- A flexible Cookiecutter template for data + AI projects on AWS or Azure.
- Mix-and-match legos: RAG, checklists, tabular ML, or lightweight analysis/script projects.
- Post‑generation hook prunes unused legos based on your choices.

Choices (extra-context keys)
- project_slug: short folder/repo name (required)
- project_name: human‑readable name
- project_type: rag | checklist | tabular_ml | hybrid | analysis | script
- cloud: aws | azure
- storage: s3-athena | onelake-fabric
- ui: none | amplify | staticwebapps
- auth: iam | entra
- eval_suite: light | full
- script_name: default script filename under scripts/ (analysis/script only; default: app)
- scaffold_script: yes | no (whether to create scripts/{{script_name}}.py)

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
- Makefile configured for a local venv (no Docker).
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

