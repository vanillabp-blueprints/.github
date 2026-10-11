# vanillabp-blueprints/.github

The files of the VanillaBP blueprints which apply to the whole organisation. Contributors read
this page. Users and AI agents read the files it describes.

| File | Purpose |
|---|---|
| `blueprints.yaml` | **The single source of truth.** Every blueprint with the BPMN elements it covers, the SPI it uses, and its repository per platform. |
| `blueprints.schema.json` | The JSON schema `blueprints.yaml` is checked against. |
| `AGENTS.md` | The rules for all blueprints, so that the `AGENTS.md` of a single blueprint stays short. |
| `CLAUDE.md` | Points an agent of Claude Code to `AGENTS.md`, whose section "How we write" holds for every text of this repository. |
| `profile/README.md` | The organisation page. Everything between the `BEGIN GENERATED` and `END GENERATED` markers is rendered from `blueprints.yaml`, so edit the index and not the page. One table per category, with a column which links the repository of each platform. |

## Changing the catalogue

Edit `blueprints.yaml`, then render and validate locally:

```bash
pip install pyyaml jsonschema
bin/validate_index.py
bin/render_index.py
```

On a push to `main`, `render-index.yaml` renders the page and commits it. Pull requests have to
bring the rendered page along themselves. `validate-index.yaml` checks that with
`bin/render_index.py --check`.

[`CONTRIBUTING.md`](./CONTRIBUTING.md) says what else a pull request needs, and where a change
to a blueprint itself goes.

Nobody maintains the status of a platform by hand. The split job of the monorepo switches
`platforms.<platform>.status` to `available` once a blueprint has been pushed into its own
repository. A `planned` entry must not carry a repository URL, and an `available` one must. The
schema enforces both, so the page can never advertise a repository which does not exist.

A person writes the third status. `not-applicable` says that a platform does not know what the
blueprint is about, so this variant will never exist. It needs a one-sentence `reason`. The
page shows the reason where the other platforms show their link. `bin/set_platform_status.py`
neither writes it nor overwrites it. `planned` is a gap which closes, and it stays a promise.
This one is an answer.

## The blueprints themselves

They are developed in [`blueprints`](https://github.com/vanillabp-blueprints/blueprints) and
delivered as one repository per blueprint and platform.
