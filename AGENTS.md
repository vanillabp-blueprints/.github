# Building a VanillaBP application from blueprints

Rules valid for **all** blueprints of this organisation. Each blueprint repository carries an
`AGENTS.md` of its own describing only what is specific to it.

Read this file together with
[`blueprints.yaml`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/blueprints.yaml),
the machine readable catalogue.

## What VanillaBP is

VanillaBP decouples business code from the business process engine (BPMS). A BPMN model
drives the process; your code implements the tasks it contains and knows nothing about the
engine executing it. Switching the BPMS is a Maven profile, not a code change — which is why
no blueprint contains BPMS-specific code.

Two terms are used throughout:

- **Workflow module** — the unit bundling BPMN models and the code implementing them. It is
  usually a JAR pulled in by an application; the application decides which BPMS adapter is
  loaded.
- **Workflow aggregate** — one persistent entity per workflow instance holding all state the
  process needs. There are no process variables.

## Procedure

1. **Determine the platform** — Spring Boot or Quarkus. Every blueprint exists per platform
   as a repository of its own; never mix them.
2. **Parse the BPMN.** Collect the element types occurring in it (`bpmn:UserTask`,
   `bpmn:BoundaryEvent`, …) and the attributes used on them.
3. **Match against `blueprints.yaml`.** Compare the element types with `covers.bpmn` and pick
   for the target platform:
   - one workflow module structure (`module-*`, start with `module-single`),
   - one persistence (`persistence-*`, JPA unless told otherwise),
   - the BPMN scenarios (`bpmn-*`) the model requires.
4. **Read the `AGENTS.md` of every blueprint chosen** (`platforms.<platform>.agents_md`).
5. **Apply the deltas.** `module-single` is the base; every `bpmn-*` blueprint is a delta on
   top of it and they are structurally identical, so several deltas can be applied to one
   application.
6. **Verify with `mvn verify`.** Each blueprint ships an integration test playing through its
   aspect; keep it and adapt it. Generated code that was never executed is a guess.
7. **Fix what startup validation reports.** VanillaBP validates the wiring between BPMN and
   code while the application boots and names the remedy in its messages. Do not work around
   such a message — it describes a real inconsistency.

Do not skip steps 6 and 7. They are the only reason to trust the result.

## Reference structure

Every blueprint uses the same structure. Keep it — an application assembled from several
blueprints stays readable only if they agree.

```
<base-package>.<usecase>
├── ApiController.java
├── Service.java                     <- @WorkflowService
├── config/<UseCase>Properties.java
└── model/
    ├── Aggregate.java
    └── AggregateRepository.java
```

### Two namespaces per workflow module

There is **no classloader isolation between workflow modules** — they end up in one runtime,
on one classpath. Two modules therefore have to differ in two namespaces, and both are
derived from the same identifier:

| | Rule | Example |
|---|---|---|
| Classes | a unique Java package for the whole module | `com.acme.orders.shipment` |
| Resources | **every** resource in one subdirectory named after the workflow module ID | `src/main/resources/shipment/…` |

"Every resource" means every one: BPMN models (`<module-id>/processes/<adapter-id>/`), the
module's configuration file (`<module-id>/<module-id>.yaml`), templates, documents, schemas.
A resource placed at the classpath root works fine until a second workflow module ships a
file of the same name — then one of them silently wins.

The single exception is the marker file `META-INF/workflow-module` containing the module ID.
It has to sit at that exact path, which is how the module is recognised at all.

## Placeholders

Identical in every blueprint. Replace all four consistently:

| Placeholder | Meaning | Example replacement |
|---|---|---|
| `blueprint.workflowmodule` | base package | `com.acme.orders` |
| `loanapproval` | use case identifier, Java package | `shipment` |
| `loan-approval` | use case identifier, kebab case: workflow module ID, resource directory, REST path | `shipment` |
| `loan_approval` | BPMN process ID | `shipment` |

The BPMN process ID in the model has to match the one used in the code, and the resource
directory has to match the workflow module ID. Most startup errors of generated applications
come from replacing one of the four and forgetting another.

## Operating an application in a browser

Blueprints expose GET requests only, so a process can be walked through in a browser without
any tooling. Keep that property: at every wait state, log one fully populated, clickable URL
per possible continuation.

```
Accept -> http://localhost:8080/api/loan-approval/{id}/assess-risk/{taskId}?riskIsAcceptable=true
Deny   -> http://localhost:8080/api/loan-approval/{id}/assess-risk/{taskId}?riskIsAcceptable=false
```

Those logged URLs are also the cheapest way for you to see which state a workflow reached.

## Never do this

1. **No process variables.** All state lives in the workflow aggregate. Sequence flow
   conditions call methods on the aggregate instead.
2. **No BPMS API in application code** — no `RuntimeService`, `ZeebeClient`, `CamundaClient`
   or any other engine class. The only compile-time dependency towards the BPMS is the
   VanillaBP SPI. Reaching for an engine API means the hexagonal architecture is broken and
   the application can no longer change its BPMS.
3. **No BPMS dependency in a workflow module.** A pure workflow module depends on
   `io.vanillabp:vanillabp-spring-boot-support` respectively
   `io.vanillabp:vanillabp-quarkus-support`, never on an adapter. Those modules deliberately
   do not expose BPMS APIs. The adapter dependency belongs into the application module.
4. **No business state in the BPMN.** The model expresses the flow, not the data. Nothing an
   auditor would want to read belongs into the diagram.
5. **One aggregate per workflow.** Do not share an aggregate between two processes unless the
   blueprint `bpmn-call-activity-decomposition` explicitly shows it, and do not persist two
   business objects into one aggregate.
6. **No direct message exchange between workflow modules.** A process must never send a
   message to a process of another workflow module — that couples them. Use the way
   `module-interaction` shows: an outgoing message becomes an internal API call, and the
   receiving module delivers a message through its own API.
7. **Do not copy reference documentation into the generated project.** Link it.
8. **Do not invent BPMS-specific configuration.** If something appears to need it, it belongs
   into the adapter's wiki, not into the application.

## Where the documentation is

| Topic | Where |
|---|---|
| Using the SPI: annotations, aggregates, multi-instance, call activities | [spi-for-java](https://github.com/vanillabp/spi-for-java) |
| Concepts, workflow modules, platform integration, configuration | [adapter-platform-integration wiki](https://github.com/vanillabp/adapter-platform-integration/wiki) |
| Everything specific to one BPMS | the wiki of the respective [BPMS adapter](https://github.com/vanillabp/adapter-platform-integration/wiki/BPMS-adapters) |

Blueprints deliberately cover only what the first two provide. If a task cannot be solved
without BPMS specifics, say so instead of inventing them.
