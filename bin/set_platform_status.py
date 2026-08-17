#!/usr/bin/env python3
"""Set the status of one platform of one blueprint in blueprints.yaml.

This is written by CI, not by hand: the split job of the monorepo marks a platform
'available' once the blueprint has actually been pushed into its own repository. The index
therefore never claims a repository which does not exist - and 'planned' is not a promise
anybody has to remember to keep.

The file is edited round-trip, so its comments and formatting survive.

Usage: bin/set_platform_status.py --id <blueprint-id> --platform <platform>
                                  --status available|planned [--index blueprints.yaml]

Exits 0 and reports 'unchanged' if the entry already says what it should, so the caller can
run it unconditionally.

'not-applicable' is not among the values this script writes, and an entry which says so is
not overwritten either: that a platform cannot have a blueprint at all is a statement about
the platform, made by a person while adding the blueprint, not something a job derives from
a directory that happens to exist.
"""

import argparse
import io
import sys
from pathlib import Path

from ruamel.yaml import YAML

ORG = "vanillabp-blueprints"
PLATFORMS = ("springboot", "quarkus")

REPO_URL = "https://github.com/{org}/{id}-{platform}"
AGENTS_MD_URL = "https://raw.githubusercontent.com/{org}/{id}-{platform}/main/AGENTS.md"


def keep_comment_last(entry, previous_last, new_last):
    """Moves whatever trails the entry behind its new last key.

    Everything following a mapping belongs to the key read last: the blank line before the
    next blueprint, the comment introducing the next category. Writing keys after that one
    would leave that comment in the middle of the entry - which is how this index once grew
    a section headline between 'status' and 'repo'.
    """

    trailing = entry.ca.items
    if previous_last != new_last and previous_last in trailing:
        trailing[new_last] = trailing.pop(previous_last)


def yaml_parser():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    # Matches the layout of blueprints.yaml, so that a round-trip changes nothing but the
    # entry asked for.
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--platform", required=True, choices=PLATFORMS)
    parser.add_argument("--status", required=True, choices=("available", "planned"))
    parser.add_argument("--index", default=None)
    args = parser.parse_args()

    index_file = Path(args.index or Path(__file__).resolve().parent.parent / "blueprints.yaml")
    yaml = yaml_parser()
    index = yaml.load(index_file.read_text(encoding="utf-8"))

    blueprint = next(
        (entry for entry in index["blueprints"] if entry["id"] == args.id),
        None,
    )
    if blueprint is None:
        print(
            f"'{args.id}' is not a blueprint of {index_file.name}."
            " Add its entry before splitting it.",
            file=sys.stderr,
        )
        sys.exit(1)

    entry = blueprint["platforms"][args.platform]

    if entry.get("status") == "not-applicable":
        print(
            f"{args.id}/{args.platform} is marked 'not-applicable'"
            f" ({entry.get('reason', 'no reason given')})."
            " Edit blueprints.yaml by hand if that is no longer true.",
            file=sys.stderr,
        )
        sys.exit(1)

    wanted = {"status": args.status}
    if args.status == "available":
        wanted["repo"] = REPO_URL.format(org=ORG, id=args.id, platform=args.platform)
        wanted["agents_md"] = AGENTS_MD_URL.format(
            org=ORG, id=args.id, platform=args.platform
        )

    if dict(entry) == wanted:
        print(f"{args.id}/{args.platform}: unchanged ({args.status})")
        return

    previous_last = list(entry.keys())[-1]
    for key in ("repo", "agents_md"):
        if key in entry and key not in wanted:
            del entry[key]
    for key, value in wanted.items():
        entry[key] = value
    keep_comment_last(entry, previous_last, list(entry.keys())[-1])

    buffer = io.StringIO()
    yaml.dump(index, buffer)
    index_file.write_text(buffer.getvalue(), encoding="utf-8")

    print(f"{args.id}/{args.platform}: {args.status}")


if __name__ == "__main__":
    main()
