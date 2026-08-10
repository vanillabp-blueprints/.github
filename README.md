# vanillabp-blueprints/.github

The organisation-wide files of the VanillaBP blueprints. Contributors read this page; users
and AI agents read the files it describes.

| File | Purpose |
|---|---|
| `blueprints.yaml` | **The single source of truth.** Every blueprint with the BPMN elements it covers, the SPI it uses, and its repository per platform. |
| `blueprints.schema.json` | JSON schema `blueprints.yaml` is validated against. |
| `AGENTS.md` | The rules valid for all blueprints, so that the `AGENTS.md` of a single blueprint stays short. |
| `profile/README.md` | The organisation page. Everything between the `BEGIN GENERATED` and `END GENERATED` markers is rendered from `blueprints.yaml` — edit the index, not the page. One table per category, with a column linking the repository of each platform. |

## Changing the catalogue

Edit `blueprints.yaml`, then render and validate locally:

```bash
pip install pyyaml jsonschema
bin/validate_index.py
bin/render_index.py
```

On a push to `main`, `render-index.yaml` renders the page and commits it. Pull requests have
to bring the rendered page along themselves; `validate-index.yaml` checks that with
`bin/render_index.py --check`.

The status of a platform is not maintained by hand: the split job of the monorepo flips
`platforms.<platform>.status` to `available` once a blueprint has been pushed into its own
repository. A `planned` entry must not carry a repository URL, and an `available` one must —
the schema enforces both, so the page can never advertise a repository which does not exist.

## The blueprints themselves

They are developed in [`blueprints`](https://github.com/vanillabp-blueprints/blueprints) and
delivered as one repository per blueprint and platform.
