from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any, List
import textwrap
import sys

import yaml


PARQUET_IO = {
    "input_format": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
    "output_format": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
    "serde": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
    "classification": "parquet",
}

CSV_IO = {
    "input_format": "org.apache.hadoop.mapred.TextInputFormat",
    "output_format": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
    "serde": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
    "classification": "csv",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r") as f:
        return yaml.safe_load(f) or {}


def hcl_quote(s: str) -> str:
    return s.replace("\"", "\\\"")


def gen_providers_tf(cloud: str) -> str:
    if cloud == "aws":
        return textwrap.dedent(
            """
            terraform {
              required_version = ">= 1.5.0"
              required_providers {
                aws = {
                  source  = "hashicorp/aws"
                  version = "~> 5.0"
                }
              }
            }

            provider "aws" {
              region = var.aws_region
            }
            """
        ).strip()
    else:
        return textwrap.dedent(
            """
            terraform {
              required_version = ">= 1.5.0"
              required_providers {
                azurerm = {
                  source  = "hashicorp/azurerm"
                  version = ">= 3.0"
                }
              }
            }

            provider "azurerm" {
              features {}
            }
            """
        ).strip()


def gen_variables_tf(cloud: str, settings: Dict[str, Any], model: Dict[str, Any]) -> str:
    aws = settings.get("aws", {})
    region = aws.get("region", "us-east-1")
    raw_bucket = aws.get("s3_bucket_raw", f"{settings['project']['slug']}-raw")
    wg = (model.get("workgroup") or settings.get("aws", {}).get("athena", {}).get("workgroup") or "primary")
    out_loc = (
        model.get("output_location")
        or settings.get("aws", {}).get("athena", {}).get("output_location")
        or f"s3://{settings['project']['slug']}-athena-results/"
    )

    if cloud == "aws":
        return textwrap.dedent(
            f"""
            variable "aws_region" {{ type = string, default = "{hcl_quote(region)}" }}
            variable "project_slug" {{ type = string, default = "{hcl_quote(settings['project']['slug'])}" }}
            variable "glue_db_name" {{ type = string, default = "{hcl_quote(model.get('database') or settings['project']['slug'] + '_db')}" }}
            variable "raw_bucket" {{ type = string, default = "{hcl_quote(raw_bucket)}" }}
            variable "create_buckets" {{ type = bool, default = false }}
            variable "athena_workgroup" {{ type = string, default = "{hcl_quote(wg)}" }}
            variable "athena_output_location" {{ type = string, default = "{hcl_quote(out_loc)}" }}
            """
        ).strip()
    else:
        rg = settings.get("azure", {}).get("resource_group", f"{settings['project']['slug']}-rg")
        return textwrap.dedent(
            f"""
            variable "azure_resource_group" {{ type = string, default = "{hcl_quote(rg)}" }}
            variable "project_slug" {{ type = string, default = "{hcl_quote(settings['project']['slug'])}" }}
            """
        ).strip()


def gen_aws_core_tf(model: Dict[str, Any]) -> str:
    # Buckets are optional to create
    bucket_resources: List[str] = []
    for b in model.get("buckets", []) or []:
        name = b.get("name")
        create = bool(b.get("create", False))
        res = textwrap.dedent(
            f"""
            resource "aws_s3_bucket" "{name.replace('-', '_')}" {{
              count  = var.create_buckets ? 1 : 0
              bucket = "{hcl_quote(name)}"
            }}
            """
        )
        if create:
            bucket_resources.append(res.strip())

    wg = textwrap.dedent(
        """
        resource "aws_athena_workgroup" "wg" {
          name = var.athena_workgroup
          configuration {
            result_configuration {
              output_location = var.athena_output_location
            }
            enforce_workgroup_configuration = false
          }
        }
        """
    ).strip()

    db = textwrap.dedent(
        """
        resource "aws_glue_catalog_database" "db" {
          name = var.glue_db_name
        }
        """
    ).strip()

    return "\n\n".join(filter(None, [*bucket_resources, wg, db]))


def column_block(col: Dict[str, Any]) -> str:
    name = col["name"]
    typ = col.get("type", "string")
    return textwrap.dedent(
        f"""
        columns {{
          name = "{hcl_quote(name)}"
          type = "{hcl_quote(typ)}"
        }}
        """
    ).strip()


def partition_block(pk: Dict[str, Any]) -> str:
    name = pk["name"]
    typ = pk.get("type", "string")
    return textwrap.dedent(
        f"""
        partition_keys {{
          name = "{hcl_quote(name)}"
          type = "{hcl_quote(typ)}"
        }}
        """
    ).strip()


def gen_aws_tables_tf(model: Dict[str, Any]) -> str:
    tables: List[str] = []
    for ds in model.get("datasets", []) or []:
        name = ds["name"]
        bucket = ds.get("bucket", "${var.raw_bucket}")
        path = ds.get("path", f"{name}/")
        fmt = (ds.get("format") or "parquet").lower()
        io = PARQUET_IO if fmt == "parquet" else CSV_IO

        cols = "\n".join(column_block(c) for c in ds.get("columns", []) or [])
        pks = "\n".join(partition_block(p) for p in ds.get("partition_keys", []) or [])

        storage_desc = textwrap.dedent(
            f"""
            storage_descriptor {{
              location      = "s3://{hcl_quote(bucket)}/{hcl_quote(path)}"
              input_format  = "{io['input_format']}"
              output_format = "{io['output_format']}"
              ser_de_info {{
                serialization_library = "{io['serde']}"
                parameters = {{
                  "serialization.format" = "1"
                }}
              }}
              {cols}
            }}
            """
        ).strip()

        tbl = textwrap.dedent(
            f"""
            resource "aws_glue_catalog_table" "{name}" {{
              name          = "{hcl_quote(name)}"
              database_name = aws_glue_catalog_database.db.name
              table_type    = "EXTERNAL_TABLE"

              {storage_desc}

              {pks}

              parameters = {{
                classification = "{io['classification']}"
              }}
            }}
            """
        ).strip()
        tables.append(tbl)

    return "\n\n".join(tables)


def gen_outputs_tf(cloud: str) -> str:
    if cloud == "aws":
        return textwrap.dedent(
            """
            output "glue_database" {
              value = aws_glue_catalog_database.db.name
            }

            output "athena_workgroup" {
              value = aws_athena_workgroup.wg.name
            }
            """
        ).strip()
    else:
        return textwrap.dedent(
            """
            output "note" {
              value = "Azure Terraform stub generated; extend with storage + Fabric/Lakehouse."
            }
            """
        ).strip()


def generate(out_dir: Path, settings_path: Path, model_path: Path) -> None:
    settings = load_yaml(settings_path)
    model = load_yaml(model_path)
    cloud = (settings.get("runtime", {}) or {}).get("cloud", "aws")

    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "providers.tf").write_text(gen_providers_tf(cloud) + "\n")
    (out_dir / "variables.tf").write_text(gen_variables_tf(cloud, settings, model) + "\n")

    if cloud == "aws":
        core = gen_aws_core_tf(model)
        tables = gen_aws_tables_tf(model)
        (out_dir / "main.tf").write_text((core + "\n\n" + tables).strip() + "\n")
    else:
        (out_dir / "main.tf").write_text(
            textwrap.dedent(
                """
                # Azure path is a stub; extend with storage account, containers, Synapse/Fabric as needed.
                # Example resources:
                # resource "azurerm_resource_group" "rg" { name = var.azure_resource_group location = "eastus" }
                """
            ).lstrip()
        )

    (out_dir / "outputs.tf").write_text(gen_outputs_tf(cloud) + "\n")

    # .gitignore for TF working dir
    (out_dir / ".gitignore").write_text(
        textwrap.dedent(
            """
            .terraform/
            .terraform.*
            terraform.tfstate
            terraform.tfstate.*
            crash.log
            override.tf
            override.tf.json
            *_override.tf
            *_override.tf.json
            .terraform.lock.hcl
            """
        ).lstrip()
    )


def main(argv: List[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Generate Terraform from data model")
    ap.add_argument("--out", default="infra/terraform", help="Output directory for .tf files")
    ap.add_argument("--settings", default="config/settings.yaml", help="Settings YAML path")
    ap.add_argument("--model", default="config/data_model.yaml", help="Data model YAML path")
    args = ap.parse_args(argv)

    generate(Path(args.out), Path(args.settings), Path(args.model))
    print(f"[tfgen] Wrote Terraform to {args.out}")


if __name__ == "__main__":
    main(sys.argv[1:])

