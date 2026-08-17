# Building a VanillaBP application from blueprints

Rules valid for **all** blueprints of this organisation. Each blueprint repository carries an
`AGENTS.md` of its own describing only what is specific to it.

Read this file together with
[`blueprints.yaml`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/blueprints.yaml),
the machine readable catalogue.

## What VanillaBP is

VanillaBP decouples business code from the business process engine (BPMS). A BPMN model
drives the process; your code implements the tasks it contains and knows nothing about the
engine executing it. Switching the BPMS is a Maven profile, not a code change, which is why
no blueprint contains BPMS-specific code.

Two terms are used throughout:

- A *workflow module* bundles BPMN models and the code implementing them. It is usually a
  JAR pulled in by an application; the application decides which BPMS adapter is loaded.
- A *workflow aggregate* is one persistent entity per workflow instance holding all state
  the process needs. There are no process variables.

## Procedure

1. Determine the platform, Spring Boot or Quarkus. Every blueprint exists per platform as a
   repository of its own; never mix them.
2. Parse the BPMN. Collect the element types occurring in it (`bpmn:UserTask`,
   `bpmn:BoundaryEvent`, …) and the attributes used on them.
3. Match against `blueprints.yaml`. Compare the element types with `covers.bpmn` and pick
   for the target platform:
   - one workflow module structure (`module-*`, start with `module-single`),
   - one persistence (`persistence-*`, JPA unless told otherwise),
   - the BPMN scenarios (`bpmn-*`) the model requires.

   Only an entry whose `platforms.<platform>.status` is `available` can be used. `planned`
   means it is being worked on, `not-applicable` means the platform does not know the
   subject at all and names the reason - do not try to port such a blueprint to the other
   platform, pick a different one.
4. Read the `AGENTS.md` of every blueprint chosen (`platforms.<platform>.agents_md`).
5. Apply the deltas. `module-single` is the base; every `bpmn-*` blueprint is a delta on top
   of it and they are structurally identical, so several deltas can be applied to one
   application.
6. Verify with `mvn verify`. Each blueprint ships an integration test playing through its
   aspect; keep it and adapt it. Generated code that was never executed is a guess.
7. Fix what startup validation reports. VanillaBP validates the wiring between BPMN and code
   while the application boots and names the remedy in its messages. Never work around such
   a message, it describes a real inconsistency.

Do not skip steps 6 and 7. They are the only reason to trust the result.

## Reference structure

Every blueprint uses the same structure. Keep it: an application assembled from several
blueprints stays readable only if they agree.

```
<base-package>.<usecase>
├── ApiController.java               <- driving adapter: HTTP calls in
├── Service.java                     <- business code, never touches VanillaBP
├── Workflow.java                    <- outgoing: the application tells the process
├── WorkflowTaskHandler.java         <- incoming: the process tells the application
├── config/<UseCase>Properties.java
└── model/
    ├── Aggregate.java
    └── AggregateRepository.java
```

### One class per direction

Talking to a BPMS happens in both directions, and the two are different architectural
things. Keep them apart:

```
ApiController ──────────┐
                        ├──→ Service ──→ Workflow ──→ ProcessService     outgoing
BPMS ──→ WorkflowTaskHandler ──┘                                         incoming
```

`Workflow` is the outgoing half. `ProcessService` is injected here and nowhere else.
`Service` calls in, naming what happened **in business terms**, and this class translates it
into what the process needs.

`WorkflowTaskHandler` is the incoming half. It carries `@WorkflowService` and every
`@WorkflowTask` method, and it calls `Service`. It is a driving adapter, the same kind of
thing as `ApiController`: that the caller is a BPMS rather than a browser changes nothing.

```java
// Service.java - what happened
public void submitRiskAssessment(final String id, final boolean acceptable) {
  final var loanApproval = loanApprovals.findById(id).orElseThrow();
  loanApproval.setRiskAcceptable(acceptable);
  workflow.riskAssessmentSubmitted(loanApproval);
}

// Workflow.java - what it means for the process
public void riskAssessmentSubmitted(final Aggregate loanApproval) {
  processService.correlateMessage(loanApproval, "RiskAssessed");
}

// WorkflowTaskHandler.java - what the process wants from the application
@WorkflowTask
public void assessRisk(final Aggregate loanApproval, @TaskId final String taskId) {
  service.riskAssessmentRequested(loanApproval, taskId);
}
```

Name the methods of `Workflow` after the business event (`riskAssessmentSubmitted`), never
after the BPMN element (`correlateRiskAssessedMessage`). The BPMN may be remodelled, a
message may become a timer and a task a call activity, without the business code noticing,
and that is the whole point.

**Do not merge the two classes.** Putting both directions into one makes it depend on
`Service` while `Service` depends on it, a circular bean reference which Spring Boot rejects
at startup unless it is worked around with `@Lazy`. An interface implemented by `Service`
does not help either: the cycle is between beans, not between types. Splitting by direction
removes it instead of hiding it.

Keep both classes even where the translation is a single line. The seam costs nothing while
a process is trivial and is what keeps the business code readable once it is not; and a
structure which is the same in every blueprint is one an agent can extend instead of having
to rebuild.

If the business service is to be unit-testable without a BPMS, let `Workflow` implement an
interface owned by the application and inject that. Do it on the **outgoing** side only. The
incoming adapter may depend on the application directly, exactly as `ApiController` does.

### A `@WorkflowTask` method contains no business logic

It translates, and that is all: it turns what the BPMS delivers (the aggregate, `@TaskId`,
`@TaskEvent`, the multi-instance element and its index) into a call to `Service`. With a
single service task that leaves one line, which is honest, since there is nothing to
translate. In a multi-instance task or a user task it is real work: pick the element this
invocation is about, keep the task ID, react to the task having been canceled. That work
belongs there rather than in the business code.

The work behind a task is business code and lives in `Service`, which the handler may call
because the directions are split (see above). Logic about the business object itself may of
course sit on the aggregate, which is a normal entity, but that is a matter of taste rather
than a rule. The rule is that nothing computes inside a `@WorkflowTask` method.

### Two namespaces per workflow module

There is **no classloader isolation between workflow modules**, they end up in one runtime,
on one classpath. Two modules therefore have to differ in two namespaces, and both are
derived from the same identifier:

| | Rule | Example |
|---|---|---|
| Classes | a unique Java package for the whole module | `com.acme.orders.shipment` |
| Resources | **every** resource in one subdirectory named after the workflow module ID | `src/main/resources/shipment/…` |

"Every resource" means every one: BPMN models (`<module-id>/processes/<adapter-id>/`), the
module's configuration file (`<module-id>/<module-id>.yaml`), templates, documents, schemas.
A resource placed at the classpath root works fine until a second workflow module ships a
file of the same name, and then one of them silently wins.

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
2. **No BPMS API in application code**, so no `RuntimeService`, `ZeebeClient`,
   `CamundaClient` or any other engine class. The only compile-time dependency towards the
   BPMS is the VanillaBP SPI. Reaching for an engine API means the hexagonal architecture is
   broken and the application can no longer change its BPMS.
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
   message to a process of another workflow module, that couples them. Use the way
   `module-interaction` shows: an outgoing message becomes an internal API call, and the
   receiving module delivers a message through its own API.
7. **Do not let two branches of one workflow write the aggregate carelessly.** A parallel
   gateway, a non-interrupting boundary event and a multi-instance task each add a token, so
   a second writer exists next to whatever the application writes from its API. JPA saves the
   whole row, so the branch committing second puts back what it read at its start and the
   other branch's work is gone, without an exception and without a log line. Pick a strategy
   and say which one: an entity per phase in a 1:1 relation to the aggregate, `@DynamicUpdate`
   while the branches write different attributes, `@Version` plus a retry, or a relation of
   its own that is only ever appended to. The blueprint `persistence-parallel-branches` shows
   the first and explains when the others fit.
8. **One `@WorkflowService` class per workflow aggregate class.** When a second process works
   on the same aggregate, name it in `secondaryBpmnProcesses` of the existing class and put
   its `@WorkflowTask` methods there. Do not annotate a second class with `@WorkflowService`
   for that aggregate: VanillaBP builds one `ProcessService` per aggregate class and starts
   the process of whichever class the classpath scan found first, so `startWorkflow` may
   start the wrong process. Nothing says so - the workflow runs, and the aggregate ends up
   half filled. This is easy to walk into when two blueprints are composed, because each
   brings a handler class of its own.
9. **Do not copy reference documentation into the generated project.** Link it.
10. **Do not invent BPMS-specific configuration.** If something appears to need it, it belongs
    into the adapter's wiki, not into the application.

## Where the documentation is

| Topic | Where |
|---|---|
| Using the SPI: annotations, aggregates, multi-instance, call activities | [spi-for-java](https://github.com/vanillabp/spi-for-java) |
| Concepts, workflow modules, platform integration, configuration | [adapter-platform-integration wiki](https://github.com/vanillabp/adapter-platform-integration/wiki) |
| Everything specific to one BPMS | the wiki of the respective [BPMS adapter](https://github.com/vanillabp/adapter-platform-integration/wiki/BPMS-adapters) |

Blueprints deliberately cover only what the first two provide. If a task cannot be solved
without BPMS specifics, say so instead of inventing them.
