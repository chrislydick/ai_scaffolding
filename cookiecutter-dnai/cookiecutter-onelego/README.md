# cookiecutter-onelego

Security-first cookiecutter template with pre-commit hooks, CI security scans, OPA policies with waivers, and local Make targets.

## Quick Start
- Install: `pip install cookiecutter`
- Generate a project:
  
  ```bash
  python3 -m cookiecutter -o . cookiecutter-onelego \
    project_slug=my-secure-project \
    github_org=my-github-org \
    org_domain=example.com
  ```
- Enter the new project folder and run:
  
  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  pip install -U pip && pip install -r requirements.txt
  pre-commit install
  make security
  ```

## What You Get
- Pre-commit hooks: Terraform fmt/validate/tflint, Checkov, Trivy (IaC), gitleaks, detect-secrets, black, ruff, bandit, and a binary/hidden-code gate.
- CI: runs all scanners, OPA/Conftest against Terraform plan JSON, SBOM (Scorecard included), honors `security-override` PR label.
- OPA waivers: `policy/opa/waivers.yaml` (reason + expiry) to allow auditable exceptions.
- Makefile targets: `make security`, `make sbom`, `make tfplan` for local checks.
- Docs: `SECURITY.md`, `docs/SECURITY-OVERRIDES.md`, PR template, `CODEOWNERS`, `.gitattributes`.

## Notes
- CI passes on a clean skeleton; once Terraform is added under `infra/terraform/`, the same guard-rails and waiver flow apply automatically.
- Update `.secrets.baseline` via: `detect-secrets scan > .secrets.baseline`.
