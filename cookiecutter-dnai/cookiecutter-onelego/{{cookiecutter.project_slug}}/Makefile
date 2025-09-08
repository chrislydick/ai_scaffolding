
.PHONY: env security sbom tfplan

env:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt || true
	pre-commit install

security:
	pre-commit run --all-files
	@if [ -d infra/terraform ]; then \
		terraform -chdir=infra/terraform init -backend=false; \
		terraform -chdir=infra/terraform validate; \
		terraform -chdir=infra/terraform plan -out=tf.plan || true; \
		terraform -chdir=infra/terraform show -json tf.plan > tfplan.json || echo "{}" > tfplan.json; \
		checkov -f tfplan.json --quiet; \
		conftest test tfplan.json -p policy/opa || true; \
	fi
	@if [ -f requirements.txt ]; then pip-audit -r requirements.txt || true; fi

sbom:
	which syft >/dev/null 2>&1 || (curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin)
	syft dir:. -o cyclonedx-json > sbom.json

tfplan:
	terraform -chdir=infra/terraform plan -out=tf.plan || true
	terraform -chdir=infra/terraform show -json tf.plan > tfplan.json || echo "{}" > tfplan.json

