
## Security
- Install hooks: `make env` (runs `pre-commit install`).
- Local scan: `make security` (IaC + code + secrets + OPA).
- SBOM: `make sbom` (CycloneDX JSON).
- Overrides: see **docs/SECURITY-OVERRIDES.md** for targeted, time-boxed waivers with reasons. Avoid repo-wide ignores.
[![ci-security](https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/actions/workflows/ci-security.yml/badge.svg)](https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.project_slug}}/actions/workflows/ci-security.yml)

