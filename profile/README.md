![VanillaBP](./vanillabp-headline.png)

## What is VanillaBP?

*VanillaBP* is an independent API for business processing engines kept simple, plain and without frills.

For more infos check out [https://www.vanillabp.io](https://www.vanillabp.io).

## Blueprints

A blueprint is a small application you can run. It shows **one** aspect of building business
process software with VanillaBP: how a workflow module is structured, how a user task is
completed, how a message reaches a running workflow. Instead of a few large examples which show
everything and explain nothing, there are many small ones. Each has a README which explains its
aspect. It links the reference documentation instead of repeating it.

Blueprints are meant to be copied. They all use the same package structure, the same
placeholders and the same test setup. So if you understand one, you understand all of them. To
combine two of them, you apply two deltas.

Every blueprint is built and tested on every business process engine it claims. That happens on
each change, and again each night against the current state of VanillaBP:

[![Build](https://github.com/vanillabp-blueprints/blueprints/actions/workflows/build.yaml/badge.svg)](https://github.com/vanillabp-blueprints/blueprints/actions/workflows/build.yaml)
[![Nightly](https://github.com/vanillabp-blueprints/blueprints/actions/workflows/nightly.yaml/badge.svg)](https://github.com/vanillabp-blueprints/blueprints/actions/workflows/nightly.yaml)

### How to use a blueprint

1. Pick the blueprints which match what you build. Start with `module-single`, the base every
   other blueprint is a delta of. Then add the BPMN scenarios your process needs.
2. Follow your platform's link. Every blueprint is a repository of its own per platform, so you
   never see the code of the other one. The *Platforms* column links the repository for Spring
   Boot and for Quarkus separately.
3. Clone and run it. Every blueprint builds with `mvn verify`, and you can operate it with a
   browser alone. Its README names one URL which starts the process. At every wait state the
   application logs the URLs to continue with.
4. Choose the BPMS (business process management system). A Maven profile decides which business
   process engine a blueprint runs on: `-Pcamunda7`, `-Pcamunda8` or `-Pprocess-engine-api`. It
   is never a code change. That is the point VanillaBP makes.

### For AI agents

The catalogue below is generated from an index for machines. An agent which implements a
modelled BPMN reads these two files and needs nothing else:

- [`blueprints.yaml`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/blueprints.yaml):
  every blueprint with the BPMN element types it covers (`covers.bpmn`), the SPI it uses, which
  blueprints it combines with, and the repository per platform.
- [`AGENTS.md`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/AGENTS.md):
  the rules for all blueprints: the reference structure, the placeholders, the procedure and
  the list of things never to do.

Each blueprint repository has an `AGENTS.md` of its own. It describes its placeholders, its
core files, and how to add it to an existing project.

<!-- BEGIN GENERATED - edit blueprints.yaml, not this section -->

36 blueprints, published today: 34 of 35 for Spring Boot, 35 of 36 for Quarkus. If a blueprint has not been published for a platform yet, the platform is listed as planned, not left out. If a blueprint cannot exist for a platform, the platform is listed as not applicable, with the reason.

### Workflow module structure and runtime

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `module-single` | Application plus one workflow module | `bpmn:ServiceTask` | [Spring Boot](https://github.com/vanillabp-blueprints/module-single-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-single-quarkus) |
| `module-multi` | Several workflow modules in one application | — | [Spring Boot](https://github.com/vanillabp-blueprints/module-multi-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-multi-quarkus) |
| `module-standalone` | The application is the workflow module | — | [Spring Boot](https://github.com/vanillabp-blueprints/module-standalone-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-standalone-quarkus) |
| `module-interaction` | Interaction between workflow modules | `bpmn:IntermediateThrowEvent`, `bpmn:IntermediateCatchEvent`, `bpmn:SendTask` | [Spring Boot](https://github.com/vanillabp-blueprints/module-interaction-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-interaction-quarkus) |
| `module-packaging` | Assembling a runtime from workflow modules, and shipping it | — | [Spring Boot](https://github.com/vanillabp-blueprints/module-packaging-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-packaging-quarkus) |
| `module-bpms-migration` | Migrating running workflows to another BPMS | — | [Spring Boot](https://github.com/vanillabp-blueprints/module-bpms-migration-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-bpms-migration-quarkus) |
| `module-idle-application` | An idle application | `bpmn:ServiceTask`, `bpmn:IntermediateCatchEvent`, `bpmn:TimerEventDefinition` | [Spring Boot](https://github.com/vanillabp-blueprints/module-idle-application-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/module-idle-application-quarkus) |

### Persistence of workflow aggregates

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `persistence-mongodb` | Workflow aggregates in MongoDB | — | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-mongodb-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-mongodb-quarkus) |
| `persistence-custom` | A persistence of your own | — | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-custom-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-custom-quarkus) |
| `persistence-parallel-branches` | Two branches writing one aggregate | `bpmn:ParallelGateway`, `bpmn:UserTask` | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-parallel-branches-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-parallel-branches-quarkus) |
| `persistence-liquibase` | The application owns its database schema | — | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-liquibase-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-liquibase-quarkus) |
| `persistence-flyway` | The application owns its database schema, with Flyway | — | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-flyway-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-flyway-quarkus) |
| `persistence-audited-aggregate` | A workflow aggregate which remembers every change | `bpmn:ServiceTask`, `bpmn:UserTask` | [Spring Boot](https://github.com/vanillabp-blueprints/persistence-audited-aggregate-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-audited-aggregate-quarkus) |
| `persistence-active-record` | Aggregates without a repository | — | Spring Boot *(not applicable: Spring Boot has no active record idiom for entities.)*<br>[Quarkus](https://github.com/vanillabp-blueprints/persistence-active-record-quarkus) |

### BPMN scenarios

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `bpmn-service-task` | Service tasks | `bpmn:ServiceTask` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-service-task-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-service-task-quarkus) |
| `bpmn-user-task` | User tasks | `bpmn:UserTask` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-user-task-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-user-task-quarkus) |
| `bpmn-async-task` | Asynchronous tasks | `bpmn:SendTask` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-async-task-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-async-task-quarkus) |
| `bpmn-message-correlation` | Messages for running workflows | `bpmn:IntermediateCatchEvent`, `bpmn:MessageEventDefinition` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-message-correlation-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-message-correlation-quarkus) |
| `bpmn-message-start` | Starting a workflow by message | `bpmn:StartEvent`, `bpmn:MessageEventDefinition` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-message-start-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-message-start-quarkus) |
| `bpmn-bpms-initiated-start` | Workflows the BPMS starts | `bpmn:StartEvent`, `bpmn:TimerEventDefinition`, `bpmn:SignalEventDefinition` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-bpms-initiated-start-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-bpms-initiated-start-quarkus) |
| `bpmn-timer` | Timers | `bpmn:IntermediateCatchEvent`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-timer-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-timer-quarkus) |
| `bpmn-signals` | Signals | `bpmn:SignalEventDefinition`, `bpmn:IntermediateCatchEvent` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-signals-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-signals-quarkus) |
| `bpmn-workflow-ended` | Learning that a workflow ended | `bpmn:EndEvent` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-workflow-ended-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-workflow-ended-quarkus) |
| `bpmn-boundary-events` | Boundary events | `bpmn:BoundaryEvent` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-boundary-events-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-boundary-events-quarkus) |
| `bpmn-error-escalation` | BPMN errors and escalations | `bpmn:ErrorEventDefinition`, `bpmn:EscalationEventDefinition`, `bpmn:BoundaryEvent` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-error-escalation-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-error-escalation-quarkus) |
| `bpmn-gateways` | Gateways and conditional sequence flows | `bpmn:ExclusiveGateway`, `bpmn:SequenceFlow` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-gateways-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-gateways-quarkus) |
| `bpmn-business-rule-task` | Business rule tasks and decision tables | `bpmn:BusinessRuleTask`, `bpmn:ExclusiveGateway` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-business-rule-task-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-business-rule-task-quarkus) |
| `bpmn-call-activity-decomposition` | Call activities to reduce complexity | `bpmn:CallActivity` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-call-activity-decomposition-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-call-activity-decomposition-quarkus) |
| `bpmn-multi-instance-task` | Multi-instance tasks | `bpmn:MultiInstanceLoopCharacteristics`, `bpmn:ServiceTask` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-multi-instance-task-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-multi-instance-task-quarkus) |
| `bpmn-multi-instance-subprocess` | Multi-instance subprocesses | `bpmn:SubProcess`, `bpmn:MultiInstanceLoopCharacteristics` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-multi-instance-subprocess-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-multi-instance-subprocess-quarkus) |
| `bpmn-versioning` | Versioning BPMN processes | — | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-versioning-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-versioning-quarkus) |
| `bpmn-aggregate-decoupling` | Decoupling BPMN from the data model | — | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-aggregate-decoupling-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-aggregate-decoupling-quarkus) |
| `bpmn-history-and-diagram` | Showing BPMN and execution history | — | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-history-and-diagram-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-history-and-diagram-quarkus) |
| `bpmn-adhoc-subprocess` | Ad-hoc subprocesses | `bpmn:AdHocSubProcess`, `bpmn:BusinessRuleTask` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-adhoc-subprocess-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-adhoc-subprocess-quarkus) |
| `bpmn-process-sections` | Sections of a process and their data | `bpmn:SubProcess`, `bpmn:CallActivity`, `bpmn:ExclusiveGateway` | [Spring Boot](https://github.com/vanillabp-blueprints/bpmn-process-sections-springboot)<br>[Quarkus](https://github.com/vanillabp-blueprints/bpmn-process-sections-quarkus) |

### Showcase

| Blueprint | What it shows | BPMN elements | Platforms |
|---|---|---|---|
| `showcase-standalone` | A complete application | `bpmn:ServiceTask`, `bpmn:UserTask`, `bpmn:ExclusiveGateway`, `bpmn:BoundaryEvent`, `bpmn:TimerEventDefinition` | Spring Boot *(planned)*<br>Quarkus *(planned)* |

<!-- END GENERATED -->

## Contributing

Blueprints are developed in the monorepo
[`blueprints`](https://github.com/vanillabp-blueprints/blueprints) and delivered as one
repository per blueprint and platform. Those repositories are read-only mirrors, so **issues
and pull requests belong in the monorepo.**
