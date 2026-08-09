#!/usr/bin/env python3
"""Validate blueprints.yaml against blueprints.schema.json plus the checks a JSON
schema cannot express (unique IDs, references between blueprints, URL shapes).

Usage: bin/validate_index.py [blueprints.yaml] [blueprints.schema.json]
"""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ORG = "vanillabp-blueprints"
PLATFORMS = ("springboot", "quarkus")

REPO_URL = "https://github.com/{org}/{id}-{platform}"
AGENTS_MD_URL = "https://raw.githubusercontent.com/{org}/{id}-{platform}/main/AGENTS.md"


def fail(errors):
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    print(f"\n{len(errors)} problem(s) found in the blueprints index.", file=sys.stderr)
    sys.exit(1)


def schema_errors(index, schema):
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(index), key=str):
        location = "/".join(str(part) for part in error.absolute_path) or "(root)"
        errors.append(f"{location}: {error.message}")
    return errors


def semantic_errors(index):
    errors = []
    blueprints = index.get("blueprints", [])
    ids = [blueprint.get("id") for blueprint in blueprints]

    for duplicate in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"blueprint ID '{duplicate}' is used more than once")

    known = set(ids)
    for blueprint in blueprints:
        blueprint_id = blueprint.get("id")

        base = blueprint.get("base")
        if base is not None and base not in known:
            errors.append(
                f"{blueprint_id}: 'base' references the unknown blueprint '{base}'"
            )
        if base == blueprint_id:
            errors.append(f"{blueprint_id}: 'base' references the blueprint itself")

        for other in blueprint.get("composes_with", []):
            if other not in known:
                errors.append(
                    f"{blueprint_id}: 'composes_with' references"
                    f" the unknown blueprint '{other}'"
                )
            if other == blueprint_id:
                errors.append(
                    f"{blueprint_id}: 'composes_with' references the blueprint itself"
                )

        for platform in PLATFORMS:
            entry = blueprint.get("platforms", {}).get(platform, {})
            if entry.get("status") != "available":
                continue
            expected = {
                "repo": REPO_URL.format(org=ORG, id=blueprint_id, platform=platform),
                "agents_md": AGENTS_MD_URL.format(
                    org=ORG, id=blueprint_id, platform=platform
                ),
            }
            for key, expected_value in expected.items():
                if entry.get(key) != expected_value:
                    errors.append(
                        f"{blueprint_id}/{platform}: '{key}' is '{entry.get(key)}',"
                        f" expected '{expected_value}'"
                    )

    return errors


def main():
    args = sys.argv[1:]
    root = Path(__file__).resolve().parent.parent
    index_file = Path(args[0]) if len(args) > 0 else root / "blueprints.yaml"
    schema_file = Path(args[1]) if len(args) > 1 else root / "blueprints.schema.json"

    index = yaml.safe_load(index_file.read_text(encoding="utf-8"))
    schema = json.loads(schema_file.read_text(encoding="utf-8"))

    errors = schema_errors(index, schema)
    if not errors:
        # Reporting reference errors on a structurally broken index is only noise.
        errors = semantic_errors(index)
    if errors:
        print(f"{index_file} is not a valid blueprints index:\n", file=sys.stderr)
        fail(errors)

    blueprints = index["blueprints"]
    available = sum(
        1
        for blueprint in blueprints
        for platform in PLATFORMS
        if blueprint["platforms"][platform]["status"] == "available"
    )
    print(
        f"{index_file.name} is valid:"
        f" {len(blueprints)} blueprints,"
        f" {available} of {len(blueprints) * len(PLATFORMS)} platform variants available"
    )


if __name__ == "__main__":
    main()
