![VanillaBP](./vanillabp-headline.png)

## What is VanillaBP?

*VanillaBP* is an independent API for business processing engines kept simple, plain and without frills.

For more infos check out [https://www.vanillabp.io](https://www.vanillabp.io).

## Blueprints

A blueprint is a small, runnable application showing **one** aspect of building business
process software with VanillaBP — how a workflow module is structured, how a user task is
completed, how a message reaches a running workflow. Instead of a few large examples that
show everything and explain nothing, there are many small ones, each with a README
explaining its aspect and linking the reference documentation rather than repeating it.

Blueprints are meant to be copied. They all use the same package structure, the same
placeholders and the same test setup, so understanding one means understanding all of them,
and combining two of them means applying two deltas.

### How to use a blueprint

1. **Pick the blueprints matching what you are building.** Start with `module-single`; it is
   the base every other blueprint is a delta of. Then add the BPMN scenarios your process
   needs.
2. **Follow your platform's link.** Every blueprint is a repository of its own per platform,
   so you never see the code of the other one — the *Platforms* column links the repository
   for Spring Boot and for Quarkus separately.
3. **Clone and run it.** Every blueprint builds with `mvn verify` and is operable in a
   browser alone: its README names one URL to start the process, and at every wait state the
   application logs the URLs to continue with.
4. **Choose the BPMS.** Which business process engine a blueprint runs on is a Maven
   profile — `-Pcamunda7`, `-Pcamunda8` or `-Pprocess-engine-api` — never a code change.
   That is the point VanillaBP is making.

### For AI agents

The catalogue below is generated from a machine readable index. An agent implementing a
modelled BPMN reads these two files and needs nothing else:

- [`blueprints.yaml`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/blueprints.yaml) —
  every blueprint with the BPMN element types it covers (`covers.bpmn`), the SPI it uses,
  which blueprints it composes with and the repository per platform.
- [`AGENTS.md`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/AGENTS.md) —
  the rules valid for all blueprints: reference structure, placeholders, the procedure and
  the list of things never to do.

Each blueprint repository carries an `AGENTS.md` of its own describing its placeholders, its
core files and how to graft it onto an existing project.

<!-- BEGIN GENERATED - edit blueprints.yaml, not this section -->

Available today, of 26 blueprints: 1 for Spring Boot, none for Quarkus. A blueprint which is not published for a platform yet is listed as planned rather than left out.

### Workflow module structure and runtime

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `module-single` | Application plus one workflow module | `bpmn:ServiceTask` | [Spring Boot](https://github.com/vanillabp-blueprints/module-single-springboot)<br>Quarkus *(planned)* |
| `module-multi` | Several workflow modules in one application | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `module-standalone` | The application is the workflow module | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `module-interaction` | Interaction between workflow modules | `bpmn:IntermediateThrowEvent`, `bpmn:IntermediateCatchEvent`, `bpmn:SendTask` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `module-shared-code` | Shared code between workflow modules | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `module-packaging` | Packaging and running the application | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `module-bpms-migration` | Migrating running workflows to another BPMS | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |

### Persistence of workflow aggregates

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `persistence-mongodb` | Workflow aggregates in MongoDB | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `persistence-custom` | A persistence of your own | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |

### BPMN scenarios

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `bpmn-service-task` | Service tasks | `bpmn:ServiceTask` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-user-task` | User tasks | `bpmn:UserTask` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-async-task` | Asynchronous tasks | `bpmn:SendTask`, `bpmn:ReceiveTask` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-message-correlation` | Messages for running workflows | `bpmn:IntermediateCatchEvent`, `bpmn:MessageEventDefinition` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-message-start` | Starting a workflow by message | `bpmn:StartEvent`, `bpmn:MessageEventDefinition` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-timer` | Timers | `bpmn:IntermediateCatchEvent`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-boundary-events` | Boundary events | `bpmn:BoundaryEvent` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-error-escalation` | BPMN errors and escalations | `bpmn:ErrorEventDefinition`, `bpmn:EscalationEventDefinition`, `bpmn:BoundaryEvent` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-gateways` | Gateways and conditional sequence flows | `bpmn:ExclusiveGateway`, `bpmn:SequenceFlow` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-call-activity-decomposition` | Call activities to reduce complexity | `bpmn:CallActivity` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-call-activity-reuse` | Call activities to reuse a process | `bpmn:CallActivity` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-multi-instance-task` | Multi-instance tasks | `bpmn:MultiInstanceLoopCharacteristics`, `bpmn:ServiceTask` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-multi-instance-subprocess` | Multi-instance subprocesses | `bpmn:SubProcess`, `bpmn:MultiInstanceLoopCharacteristics` | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-versioning` | Versioning BPMN processes | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-aggregate-decoupling` | Decoupling BPMN from the data model | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |
| `bpmn-history-and-diagram` | Showing BPMN and execution history | — | Spring Boot *(planned)*<br>Quarkus *(planned)* |

### Showcase

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `showcase-standalone` | A complete application | `bpmn:ServiceTask`, `bpmn:UserTask`, `bpmn:ExclusiveGateway`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` | Spring Boot *(planned)*<br>Quarkus *(planned)* |

<!-- END GENERATED -->

## Contributing

Blueprints are developed in the monorepo
[`blueprints`](https://github.com/vanillabp-blueprints/blueprints) and delivered as one
repository per blueprint and platform. Those repositories are read-only mirrors — **issues
and pull requests belong into the monorepo.**
