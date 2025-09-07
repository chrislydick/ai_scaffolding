Panorama With Bounding Box

Quickstart
- make env: creates venv and installs deps.
- make kb-load: runs RAG ingest (if project_type=rag|hybrid).
- make deploy-aws: deploys API via SAM (if cloud=aws).

Scaffold New Project
Create a new project from the template:

```
python3 -m cookiecutter --no-input -o . cookiecutter-dnai \
  project_slug=my-new-project \
  project_name="My New Project" \
  project_type=script \
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
- dnai catalog  # sync assets/glossary to Purview (if configured)
- dnai panorama --lat 47.6062 --lon -122.3321 --radius 1000 --wikimedia
  - Optional keys: --flickr_key YOUR_KEY, --google_key YOUR_KEY, --mapillary_token YOUR_TOKEN, --years "2021,2023"
  - Outputs a timestamped folder per run, with images saved under <run>/<service>/
 - dnai script -- --lat 47.6062 --lon -122.3321 --radius 1000 --wikimedia
 - make run-script  # runs the script with sample args

Notes
- No Docker or local web server required; handlers are Lambda-style.
- The template conditionally includes legos for:
  project_type=script, cloud=aws, storage=s3-athena, ui=amplify, auth=iam, eval_suite=light.
