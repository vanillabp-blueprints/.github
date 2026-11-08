#!/usr/bin/env python3
"""Render the blueprint catalogue of profile/README.md from blueprints.yaml.

Everything between the two markers below is generated; the prose around them is written
by hand. This is why blueprints.yaml is the single source of truth: prose and index
cannot drift apart if one of them is produced by the other.

There is one table per category, not one per platform: the catalogue is the same for
both, and repeating it twice made the page long without saying more. Which platforms a
blueprint exists for is a column, and each platform links its own repository.

Usage: bin/render_index.py [--check]
       --check exits non-zero if the file is not up to date, without writing it.
"""

import sys
from pathlib import Path

import yaml

BEGIN = "<!-- BEGIN GENERATED - edit blueprints.yaml, not this section -->"
END = "<!-- END GENERATED -->"

PLATFORMS = [("springboot", "Spring Boot"), ("quarkus", "Quarkus")]

# The platforms of a cockpit frontend are the UI frameworks it is written in.
FRONTEND_PLATFORMS = [("react", "React"), ("angular", "Angular"), ("vue", "Vue")]

CATEGORIES = [
    ("module", "Workflow module structure and runtime"),
    ("persistence", "Persistence of workflow aggregates"),
    ("bpmn", "BPMN scenarios"),
    ("cockpit", "Business Cockpit"),
    ("showcase", "Showcase"),
]

# A line below the heading, for a category whose table needs one more word than its title.
CATEGORY_INTROS = {
    "cockpit": (
        "Blueprints for a workflow module whose user tasks the"
        " [Business Cockpit](https://github.com/vanillabp/business-cockpit) shows. The"
        " frontends build with npm and not with Maven. So they exist per UI framework, and"
        " their *Platforms* column names React, Angular and Vue."
    ),
}


def is_frontend(blueprint):
    return any(platform in blueprint["platforms"] for platform, _ in FRONTEND_PLATFORMS)


def platforms_cell(blueprint):
    """One cell naming every platform, linking the ones which exist."""
    parts = []
    # A frontend says 'not-applicable' for both Java platforms. Repeating that in every row
    # would only push its frameworks out of sight, and the category intro says it once.
    for platform, label in FRONTEND_PLATFORMS if is_frontend(blueprint) else PLATFORMS:
        entry = blueprint["platforms"].get(platform)
        if entry is None:
            continue
        if entry["status"] == "available":
            parts.append(f"[{label}]({entry['repo']})")
        elif entry["status"] == "not-applicable":
            # Not 'planned' with a footnote: this one is never going to arrive, and the
            # reason belongs where a reader looks for the link.
            parts.append(f"{label} *(not applicable: {entry['reason']})*")
        else:
            parts.append(f"{label} *(planned)*")
    # A line break rather than a separator: the entries line up below each other, which a
    # trailing '(planned)' on one of them would otherwise push out of alignment.
    return "<br>".join(parts)


def render(blueprints):
    total = len(blueprints)
    counts = []
    for platform, label in PLATFORMS:
        states = [blueprint["platforms"][platform]["status"] for blueprint in blueprints]
        # The denominator leaves out what this platform cannot have anyway, so the figure
        # says how far the platform has come rather than how rare its idioms are.
        possible = len(states) - states.count("not-applicable")
        counts.append(f"{states.count('available') or 'none'} of {possible} for {label}")
    frontend_states = [
        entry["status"]
        for blueprint in blueprints
        for platform, _ in FRONTEND_PLATFORMS
        if (entry := blueprint["platforms"].get(platform)) is not None
    ]
    if frontend_states:
        # One figure for all frameworks: a count per framework would be three figures of one
        # or two each, and nobody picks a blueprint by them.
        possible = len(frontend_states) - frontend_states.count("not-applicable")
        counts.append(
            f"{frontend_states.count('available') or 'none'} of {possible}"
            " for the frontends of the Business Cockpit"
        )

    lines = [
        f"{total} blueprints, published today: {', '.join(counts)}. If a blueprint has not"
        " been published for a platform yet, the platform is listed as planned, not left out."
        " If a blueprint cannot exist for a platform, the platform is listed as not"
        " applicable, with the reason.",
        "",
    ]

    for category, category_label in CATEGORIES:
        of_category = [
            blueprint for blueprint in blueprints if blueprint["category"] == category
        ]
        if not of_category:
            continue
        lines += [f"### {category_label}", ""]
        if category in CATEGORY_INTROS:
            lines += [CATEGORY_INTROS[category], ""]
        lines += [
            "| Blueprint | What it shows | BPMN elements | Platforms |",
            "|---|---|---|---|",
        ]
        for blueprint in of_category:
            elements = (
                ", ".join(f"`{element}`" for element in blueprint["covers"]["bpmn"])
                or "—"
            )
            lines.append(
                f"| `{blueprint['id']}` | {blueprint['title']} | {elements}"
                f" | {platforms_cell(blueprint)} |"
            )
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

    generated = render(blueprints)

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
