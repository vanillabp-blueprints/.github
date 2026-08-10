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

1. **Pick your platform** — Spring Boot or Quarkus. Each blueprint is a repository of its
   own per platform, so you never see the code of the other one.
2. **Pick the blueprints matching what you are building.** Start with `module-single`; it is
   the base every other blueprint is a delta of. Then add the BPMN scenarios your process
   needs.
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

## Spring Boot

1 of 26 blueprints are available for Spring Boot. Clone the one you need - each is a repository of its own.

### Workflow module structure and runtime

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| [`module-single`](https://github.com/vanillabp-blueprints/module-single-springboot) | Application plus one workflow module | `bpmn:ServiceTask` |
| `module-multi` *(planned)* | Several workflow modules in one application | — |
| `module-standalone` *(planned)* | The application is the workflow module | — |
| `module-interaction` *(planned)* | Interaction between workflow modules | `bpmn:IntermediateThrowEvent`, `bpmn:IntermediateCatchEvent`, `bpmn:SendTask` |
| `module-shared-code` *(planned)* | Shared code between workflow modules | — |
| `module-packaging` *(planned)* | Packaging and running the application | — |
| `module-bpms-migration` *(planned)* | Migrating running workflows to another BPMS | — |

### Persistence of workflow aggregates

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `persistence-mongodb` *(planned)* | Workflow aggregates in MongoDB | — |
| `persistence-custom` *(planned)* | A persistence of your own | — |

### BPMN scenarios

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `bpmn-service-task` *(planned)* | Service tasks | `bpmn:ServiceTask` |
| `bpmn-user-task` *(planned)* | User tasks | `bpmn:UserTask` |
| `bpmn-async-task` *(planned)* | Asynchronous tasks | `bpmn:SendTask`, `bpmn:ReceiveTask` |
| `bpmn-message-correlation` *(planned)* | Messages for running workflows | `bpmn:IntermediateCatchEvent`, `bpmn:MessageEventDefinition` |
| `bpmn-message-start` *(planned)* | Starting a workflow by message | `bpmn:StartEvent`, `bpmn:MessageEventDefinition` |
| `bpmn-timer` *(planned)* | Timers | `bpmn:IntermediateCatchEvent`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` |
| `bpmn-boundary-events` *(planned)* | Boundary events | `bpmn:BoundaryEvent` |
| `bpmn-error-escalation` *(planned)* | BPMN errors and escalations | `bpmn:ErrorEventDefinition`, `bpmn:EscalationEventDefinition`, `bpmn:BoundaryEvent` |
| `bpmn-gateways` *(planned)* | Gateways and conditional sequence flows | `bpmn:ExclusiveGateway`, `bpmn:SequenceFlow` |
| `bpmn-call-activity-decomposition` *(planned)* | Call activities to reduce complexity | `bpmn:CallActivity` |
| `bpmn-call-activity-reuse` *(planned)* | Call activities to reuse a process | `bpmn:CallActivity` |
| `bpmn-multi-instance-task` *(planned)* | Multi-instance tasks | `bpmn:MultiInstanceLoopCharacteristics`, `bpmn:ServiceTask` |
| `bpmn-multi-instance-subprocess` *(planned)* | Multi-instance subprocesses | `bpmn:SubProcess`, `bpmn:MultiInstanceLoopCharacteristics` |
| `bpmn-versioning` *(planned)* | Versioning BPMN processes | — |
| `bpmn-aggregate-decoupling` *(planned)* | Decoupling BPMN from the data model | — |
| `bpmn-history-and-diagram` *(planned)* | Showing BPMN and execution history | — |

### Showcase

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `showcase-standalone` *(planned)* | A complete application | `bpmn:ServiceTask`, `bpmn:UserTask`, `bpmn:ExclusiveGateway`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` |

## Quarkus

No blueprint has been published for Quarkus yet. The catalogue below is what is planned.

### Workflow module structure and runtime

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `module-single` *(planned)* | Application plus one workflow module | `bpmn:ServiceTask` |
| `module-multi` *(planned)* | Several workflow modules in one application | — |
| `module-standalone` *(planned)* | The application is the workflow module | — |
| `module-interaction` *(planned)* | Interaction between workflow modules | `bpmn:IntermediateThrowEvent`, `bpmn:IntermediateCatchEvent`, `bpmn:SendTask` |
| `module-shared-code` *(planned)* | Shared code between workflow modules | — |
| `module-packaging` *(planned)* | Packaging and running the application | — |
| `module-bpms-migration` *(planned)* | Migrating running workflows to another BPMS | — |

### Persistence of workflow aggregates

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `persistence-mongodb` *(planned)* | Workflow aggregates in MongoDB | — |
| `persistence-custom` *(planned)* | A persistence of your own | — |

### BPMN scenarios

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `bpmn-service-task` *(planned)* | Service tasks | `bpmn:ServiceTask` |
| `bpmn-user-task` *(planned)* | User tasks | `bpmn:UserTask` |
| `bpmn-async-task` *(planned)* | Asynchronous tasks | `bpmn:SendTask`, `bpmn:ReceiveTask` |
| `bpmn-message-correlation` *(planned)* | Messages for running workflows | `bpmn:IntermediateCatchEvent`, `bpmn:MessageEventDefinition` |
| `bpmn-message-start` *(planned)* | Starting a workflow by message | `bpmn:StartEvent`, `bpmn:MessageEventDefinition` |
| `bpmn-timer` *(planned)* | Timers | `bpmn:IntermediateCatchEvent`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` |
| `bpmn-boundary-events` *(planned)* | Boundary events | `bpmn:BoundaryEvent` |
| `bpmn-error-escalation` *(planned)* | BPMN errors and escalations | `bpmn:ErrorEventDefinition`, `bpmn:EscalationEventDefinition`, `bpmn:BoundaryEvent` |
| `bpmn-gateways` *(planned)* | Gateways and conditional sequence flows | `bpmn:ExclusiveGateway`, `bpmn:SequenceFlow` |
| `bpmn-call-activity-decomposition` *(planned)* | Call activities to reduce complexity | `bpmn:CallActivity` |
| `bpmn-call-activity-reuse` *(planned)* | Call activities to reuse a process | `bpmn:CallActivity` |
| `bpmn-multi-instance-task` *(planned)* | Multi-instance tasks | `bpmn:MultiInstanceLoopCharacteristics`, `bpmn:ServiceTask` |
| `bpmn-multi-instance-subprocess` *(planned)* | Multi-instance subprocesses | `bpmn:SubProcess`, `bpmn:MultiInstanceLoopCharacteristics` |
| `bpmn-versioning` *(planned)* | Versioning BPMN processes | — |
| `bpmn-aggregate-decoupling` *(planned)* | Decoupling BPMN from the data model | — |
| `bpmn-history-and-diagram` *(planned)* | Showing BPMN and execution history | — |

### Showcase

| Blueprint | What it shows | BPMN elements |
|---|---|---|
| `showcase-standalone` *(planned)* | A complete application | `bpmn:ServiceTask`, `bpmn:UserTask`, `bpmn:ExclusiveGateway`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` |

<!-- END GENERATED -->

## Contributing

Blueprints are developed in the monorepo
[`blueprints`](https://github.com/vanillabp-blueprints/blueprints) and delivered as one
repository per blueprint and platform. Those repositories are read-only mirrors — **issues
and pull requests belong into the monorepo.**
