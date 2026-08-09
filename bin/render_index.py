#!/usr/bin/env python3
"""Render the blueprint catalogue of profile/README.md from blueprints.yaml.

Everything between the two markers below is generated; the prose around them is written
by hand. This is why blueprints.yaml is the single source of truth: prose and index
cannot drift apart if one of them is produced by the other.

Usage: bin/render_index.py [--check]
       --check exits non-zero if the file is not up to date, without writing it.
"""

import sys
from pathlib import Path

import yaml

BEGIN = "<!-- BEGIN GENERATED - edit blueprints.yaml, not this section -->"
END = "<!-- END GENERATED -->"

PLATFORMS = [("springboot", "Spring Boot"), ("quarkus", "Quarkus")]

CATEGORIES = [
    ("module", "Workflow module structure and runtime"),
    ("persistence", "Persistence of workflow aggregates"),
    ("bpmn", "BPMN scenarios"),
    ("showcase", "Showcase"),
]


def render(blueprints, platform, label):
    available = [
        blueprint
        for blueprint in blueprints
        if blueprint["platforms"][platform]["status"] == "available"
    ]
    lines = [f"## {label}", ""]
    if available:
        lines += [
            f"{len(available)} of {len(blueprints)} blueprints are available for"
            f" {label}. Clone the one you need - each is a repository of its own.",
            "",
        ]
    else:
        lines += [
            f"No blueprint has been published for {label} yet. The catalogue below is"
            " what is planned.",
            "",
        ]

    for category, category_label in CATEGORIES:
        of_category = [
            blueprint for blueprint in blueprints if blueprint["category"] == category
        ]
        if not of_category:
            continue
        lines += [
            f"### {category_label}",
            "",
            "| Blueprint | What it shows | BPMN elements |",
            "|---|---|---|",
        ]
        for blueprint in of_category:
            entry = blueprint["platforms"][platform]
            if entry["status"] == "available":
                name = f"[`{blueprint['id']}`]({entry['repo']})"
            else:
                name = f"`{blueprint['id']}` *(planned)*"
            elements = (
                ", ".join(f"`{element}`" for element in blueprint["covers"]["bpmn"])
                or "—"
            )
            lines.append(f"| {name} | {blueprint['title']} | {elements} |")
        lines.append("")

    return lines


def main():
    root = Path(__file__).resolve().parent.parent
    readme_file = root / "profile" / "README.md"
    index = yaml.safe_load((root / "blueprints.yaml").read_text(encoding="utf-8"))
    blueprints = index["blueprints"]

    readme = readme_file.read_text(encoding="utf-8")
    if BEGIN not in readme or END not in readme:
        print(
            f"{readme_file} does not contain the markers\n  {BEGIN}\n  {END}",
            file=sys.stderr,
        )
        sys.exit(2)

    generated = []
    for platform, label in PLATFORMS:
        generated += render(blueprints, platform, label)

    head, rest = readme.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    rendered = head + BEGIN + "\n\n" + "\n".join(generated).rstrip() + "\n\n" + END + tail

    if "--check" in sys.argv[1:]:
        if rendered != readme:
            print(
                f"{readme_file} is out of date - run bin/render_index.py",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"{readme_file.name} is up to date")
        return

    if rendered == readme:
        print(f"{readme_file.name} is already up to date")
        return
    readme_file.write_text(rendered, encoding="utf-8")
    print(f"{readme_file.name} rendered from blueprints.yaml")


if __name__ == "__main__":
    main()
