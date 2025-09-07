Panorama With Bounding Box

Quickstart
- make env: creates venv and installs deps.
- make kb-load: runs RAG ingest (if project_type=rag|hybrid).
- make deploy-aws: deploys API via SAM (if cloud=aws).

Setup
1) Create a virtualenv and install dependencies:
   make env

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

Notes
- No Docker or local web server required; handlers are Lambda-style.
- The template conditionally includes legos for:
  project_type=script, cloud=aws, storage=s3-athena, ui=amplify, auth=iam, eval_suite=light.
