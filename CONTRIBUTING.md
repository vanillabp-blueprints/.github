# Contributing

This repository holds the organisation files of the VanillaBP blueprints:
[`blueprints.yaml`](./blueprints.yaml) with every blueprint and what it covers, the schema it is
validated against, the `AGENTS.md` valid for all blueprints, and the organisation page rendered from
the catalogue. GitHub shows this file on every repository of the organisation which has none of its
own, so it is worth saying first where a change goes.

A blueprint itself is not changed here, and not in the repository you may have arrived from either.
The blueprints are developed in
[`blueprints`](https://github.com/vanillabp-blueprints/blueprints), and the per blueprint
repositories are mirrors written by CI, so a commit pushed into one of them is lost with the next
split. That repository has its own
[`CONTRIBUTING.md`](https://github.com/vanillabp-blueprints/blueprints/blob/main/CONTRIBUTING.md),
which is the handbook for writing a blueprint. Issues and pull requests are handled there as well.

What is changed here is the catalogue: a new blueprint, what an existing one covers, the schema, or
the way the page is rendered. [`README.md`](./README.md) describes the files, and
[`AGENTS.md`](./AGENTS.md) is the reading an agent gets before it assembles an application out of
blueprints.

## Building and testing

Python, no Maven. The scripts need two packages:

```bash
pip install pyyaml jsonschema
bin/validate_index.py
bin/render_index.py
```

`validate_index.py` checks the catalogue against the schema, `render_index.py` writes everything
between the generated markers of `profile/README.md`. Run both, and commit the rendered page: a push
to `main` renders it again, but a pull request has to bring it along, which `validate-index.yaml`
checks with `bin/render_index.py --check`.

## How we write

Most people who read this repository read English as a second language, and so does the maintainer.
Long sentences, rare words and stacked nouns slow them down. Write so that nobody has to read a
sentence twice.

Short main sentences, one thought each. One subordinate clause is enough. Active voice. The common
word instead of the rare one: `use` instead of `leverage`, `about` instead of `regarding`, `so`
instead of `consequently`. A technical term stays a technical term, but say what it means the first
time it turns up, and write an abbreviation out once. If a sentence trips you up when you read it
aloud, rewrite it.

This holds for every English text here, the reason of a `not-applicable` entry included. Nothing a
program reads is renamed for the sake of language: the id of a blueprint, the keys of the catalogue
and the names of the BPMN element types stay as they are, because the schema and the skills point at
them.

## What is asked before a change

The status of a platform is not written by hand. The split job of the monorepo sets it to
`available` once a blueprint has been pushed into its own repository, and
`bin/set_platform_status.py` is what does it. The one status a person writes is `not-applicable`,
which says a platform does not know what the blueprint is about, and it needs a one sentence reason.
Do not edit a status to make the page show something which does not exist yet.

The schema is the second question. It is what keeps the page from advertising a repository which is
not there, so a rule taken out of it is a promise given up. Ask before you loosen one.

## Opening a pull request

Work on a branch of your own and keep one subject per pull request. The description says what moved
and why it had to.

`validate-index.yaml` checks the catalogue and the rendered page on every pull request. A red check
usually means the page was not rendered again after the catalogue changed, and the log says which of
the two it is.

## License

The blueprints are published under the
[Apache License, Version 2.0](https://github.com/vanillabp-blueprints/blueprints/blob/main/LICENSE),
and by contributing to the catalogue you agree that your contribution is licensed the same way.
