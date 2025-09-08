
# Security Overrides & Waivers

When a scanner is wrong/noisy, use a **targeted waiver with a reason and expiry**.

## Options by tool
- **Checkov**: inline `#checkov:skip=<RULE> Reason: ...` (single resource only).
- **Trivy**: `.trivyignore` with rule/path and comment.
- **OPA/Conftest**: add an entry to `policy/opa/waivers.yaml` (reason + expiry).
- **gitleaks/detect-secrets**: update `.gitleaks.toml` or refresh `.secrets.baseline`.
- **bandit/ruff/mypy**: use narrow `# nosec`, `# noqa`, `# type: ignore[...]`.

## Governance
- Link the PR to an issue that explains the context.
- Add the `security-override` label so CI shows an explicit allow.
- Security/Infra CODEOWNERS must approve overrides.
- Prefer **temporary** waivers with an expiry and a backlog ticket to remove.

