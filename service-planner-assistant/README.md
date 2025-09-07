Service Planner Assistant

Quickstart
- make env: creates venv and installs deps.
- make kb-load: runs RAG ingest (if project_type=rag|hybrid).
- make deploy-aws: deploys API via SAM (if cloud=aws).

Scaffold New Project
Generate a new project from this template (examples below adjust options):

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
- project_type: rag | checklist | tabular_ml | hybrid | analysis | script
- cloud: aws | azure
- storage: s3-athena | onelake-fabric
- ui: none | amplify | staticwebapps
- auth: iam | entra
- eval_suite: light | full

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

Notes
- The template conditionally includes legos for:
  project_type=checklist, cloud=aws, storage=s3-athena, ui=amplify, auth=iam, eval_suite=light.
