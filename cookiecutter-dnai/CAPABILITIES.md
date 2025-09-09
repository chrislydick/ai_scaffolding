# Capabilities & Features Overview

This repository provides two complementary cookiecutter templates designed to help teams ship fast and safe:
- Security guard‑rails to catch issues early and audit exceptions
- Engineering and data science scaffolding to move from prototype → production smoothly

Legend: † Limited support / placeholder areas

**Security Guard‑Rails**
- Pre‑commit hooks: Terraform fmt/validate/tflint, Checkov, Trivy (IaC), gitleaks, detect‑secrets, black, ruff, bandit, and a binary/hidden‑code gate
- CI Security Pipeline: pre‑commit checks, Terraform plan JSON scans (Checkov), OPA/Conftest policy checks, SBOM (CycloneDX), OpenSSF Scorecard, SARIF upload
- Policy + Waivers: OPA policies with `policy/opa/waivers.yaml` (reason + expiry) for auditable, time‑boxed exceptions
- Overrides: explicit `security-override` PR label to permit reviewed waivers without blocking merges
- Secrets & Binary Gates: `.gitleaks.toml`, `.secrets.baseline`, and `scripts/ban_binaries.sh` reject secrets and hidden binaries
- Governance Files: `CODEOWNERS`, PR template, `.gitattributes`, `SECURITY.md`, docs/SECURITY‑OVERRIDES.md
- Local Commands: `make security` runs all local scans; `make sbom` builds a CycloneDX SBOM
- Default‑Pass Setup: CI passes on a fresh project (no Terraform required); guard‑rails engage as infra is added
- Template Source: security pack is optional and can be layered onto any project; consult your security team for current guidance.

**Engineering & Data Science Velocity**
- uv‑First Python: fast envs with `pyproject.toml`, `uv sync`, and `uv run`; CI uses `astral-sh/setup-uv`
- Make Targets: `make env`, `make lint`, `make test`, `make eval`, `make kb-load`, `make deploy-aws`, plus per‑UI `ui-install`/`ui-serve`
- CLI: `dnai` with common subcommands (chat, ingest, eval, deploy, catalog, tfgen, script passthrough)
- Project Types: rag | checklist | tabular_ml | hybrid | analysis | script | dashboard†
- UI Options: web | streamlit | react | angular† | node† | amplify† | staticwebapps†
- Cloud/Storage: AWS primary; Azure†; storage: s3‑athena | onelake‑fabric† | sap‑bw‑hana†
- Data Model → Terraform: define datasets in `config/data_model.yaml`, then `dnai tfgen` or `make tfgen` writes providers.tf/main.tf/variables.tf/outputs.tf; integrates with OPA waivers
- Governance: PII redaction, content filters, telemetry; optional Purview client
- Deploy: AWS SAM template and `make deploy-aws`; no Docker required for local dev
- Quality: ruff/black/mypy/pytest; light eval tests included; CI runs fast via uv

**When to Use This Template**
- cookiecutter‑dnai: accelerate prototyping and delivery for data/AI apps (RAG, checklists, tabular ML, scripts). Add security guard‑rails as needed.

**Getting Started**
- Data/AI project: `python3 -m cookiecutter -o . cookiecutter-dnai ...`
- To add security guard‑rails, see your org’s security pack or internal docs.

Questions or gaps? Open an issue or ask for a tailored scaffold.

