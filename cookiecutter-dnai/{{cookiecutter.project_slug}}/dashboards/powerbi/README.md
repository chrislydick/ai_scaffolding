Power BI Dashboard (placeholder)

Overview
- This project type is focused on delivering a Power BI dashboard backed by cloud storage (S3/Athena or OneLake/Fabric).
- This folder is a placeholder for .pbix files, dataset definitions, and queries.

Suggested next steps
- Create a new .pbix file in this directory.
- Configure data sources:
  - AWS: Athena via the Power BI connector; point to tables in Glue/Athena. Use workgroup/output location from config/settings.yaml.
  - Azure: Fabric/OneLake or Azure SQL; use onelake-fabric storage as configured.
- Publish and configure refresh per your environment.

Notes
- The cookiecutter marks Azure and Fabric paths as limited support (placeholders). Adjust connections accordingly.

