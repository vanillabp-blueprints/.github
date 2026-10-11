# Building a VanillaBP application from blueprints

Rules for **all** blueprints of this organisation. Each blueprint repository has an `AGENTS.md`
of its own, which describes only what is specific to that blueprint.

Read this file together with
[`blueprints.yaml`](https://raw.githubusercontent.com/vanillabp-blueprints/.github/main/blueprints.yaml),
the catalogue for machines.

## What VanillaBP is

VanillaBP separates business code from the business process engine (BPMS, business process
management system). A BPMN (Business Process Model and Notation) model drives the process. Your
code implements the tasks in it and knows nothing about the engine which runs it. Switching the
BPMS is a Maven profile, not a code change. That is why no blueprint contains code specific to
a BPMS.

Two terms appear everywhere:

- A *workflow module* bundles BPMN models and the code which implements them. It is usually a
  JAR which an application pulls in. The application decides which BPMS adapter is loaded.
- A *workflow aggregate* is one stored entity per workflow instance. It holds all state the
  process needs. There are no process variables.

## Procedure

1. Find out the platform, Spring Boot or Quarkus. Every blueprint exists per platform, as a
   repository of its own. Never mix them.
2. Parse the BPMN. Collect the element types which occur in it (`bpmn:UserTask`,
   `bpmn:BoundaryEvent`, …) and the attributes used on them.
3. Match against `blueprints.yaml`. Compare the element types with `covers.bpmn`, and pick for
   the target platform:
   - one workflow module structure (`module-*`, start with `module-single`),
   - one persistence (`persistence-*`, JPA unless told otherwise),
   - the BPMN scenarios (`bpmn-*`) the model requires.

   You can only use an entry whose `platforms.<platform>.status` is `available`. `planned`
   means somebody works on it. `not-applicable` means the platform does not know the subject at
   all, and the entry names the reason. Do not try to port such a blueprint to the other
   platform. Pick a different one.
4. Read the `AGENTS.md` of every blueprint chosen (`platforms.<platform>.agents_md`).
5. Apply the deltas. `module-single` is the base. Every `bpmn-*` blueprint is a delta on top of
   it, and they all have the same structure. So you can apply several deltas to one
   application.
6. Check with `mvn verify`. Each blueprint ships an integration test which plays through its
   aspect. Keep it and adapt it. Generated code which never ran is a guess.
7. Fix what the checks at startup report. VanillaBP checks the wiring between BPMN and code
   while the application boots, and its messages name the fix. Never work around such a
   message. It describes a real inconsistency.

Do not skip steps 6 and 7. They are the only reason to trust the result.

## Reference structure

Every blueprint uses the same structure. Keep it. An application built from several blueprints
stays readable only if they agree.

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

Talking to a BPMS goes in both directions, and the two are different things in the
architecture. Keep them apart:

```
ApiController ──────────┐
                        ├──→ Service ──→ Workflow ──→ ProcessService     outgoing
BPMS ──→ WorkflowTaskHandler ──┘                                         incoming
```

`Workflow` is the outgoing half. `ProcessService` is injected here and nowhere else. `Service`
calls in and names what happened **in business terms**. This class translates it into what the
process needs.

`WorkflowTaskHandler` is the incoming half. It carries `@WorkflowService` and every
`@WorkflowTask` method, and it calls `Service`. It is a driving adapter, the same kind of thing
as `ApiController`. That the caller is a BPMS and not a browser changes nothing.

```java
// Service.java - what happened
public void submitRiskAssessment(final String id, final boolean acceptable) {
  final var loanApproval = loanApprovals.findById(id).orElseThrow();
  loanApproval.setRiskAcceptable(acceptable);
  workflow.riskAssessmentSubmitted(loanApproval);
}

// Workflow.java - what it means for the process
public void riskAssessmentSubmitted(final Aggregate loanApproval) {
  bpms.correlateMessage(loanApproval, "RiskAssessed");
}

// WorkflowTaskHandler.java - what the process wants from the application
@WorkflowTask
public void assessRisk(final Aggregate loanRequest, @TaskId final String taskId) {
  loanApproval.riskAssessmentRequested(loanRequest, taskId);
}
```

Name the methods of `Workflow` after the business event (`riskAssessmentSubmitted`), never
after the BPMN element (`correlateRiskAssessedMessage`). The BPMN may be remodelled. A message
may become a timer, and a task a call activity, and the business code does not notice. That is
the whole point.

Name an injected bean after the role it plays in the class, not after its type. The `Service`
of a loan approval is `loanApproval`, `ProcessService` is `bpms`, `Workflow` is `workflow`, and
a repository is named after what it stores, `loanApprovals`. A call then reads like a sentence
about the business case. Where a parameter would hide the field, give it a name from the
domain, as `loanRequest` above.

**Do not merge the two classes.** If you put both directions into one class, it depends on
`Service` while `Service` depends on it. Spring Boot rejects such a circular bean reference at
startup, unless you work around it with `@Lazy`. An interface which `Service` implements does
not help either. The cycle is between beans, not between types. Splitting by direction removes
the cycle instead of hiding it.

Keep both classes even where the translation is a single line. The seam costs nothing while a
process is simple. It keeps the business code readable once the process is not simple any more.
And an agent can extend a structure which is the same in every blueprint, instead of having to
rebuild it.

If you want to unit-test the business service without a BPMS, let `Workflow` implement an
interface which the application owns, and inject that. Do it on the **outgoing** side only. The
incoming adapter may depend on the application directly, exactly as `ApiController` does.

### A `@WorkflowTask` method contains no business logic

It translates, and that is all. It turns what the BPMS delivers (the aggregate, `@TaskId`,
`@TaskEvent`, the multi-instance element and its index) into a call to `Service`. With a single
service task that leaves one line. That is honest, because there is nothing to translate. In a
multi-instance task or a user task it is real work: pick the element this call is about, keep
the task ID, react when the task was canceled. That work belongs there, not in the business
code.

The work behind a task is business code and lives in `Service`. The handler may call it,
because the directions are split (see above). Logic about the business object itself may of
course sit on the aggregate, which is a normal entity. But that is a matter of taste, not a
rule. The rule is that nothing computes inside a `@WorkflowTask` method.

### Splitting a large workflow

The structure above is one use case of medium size. A large process would make both `Service`
and `WorkflowTaskHandler` huge. One pair of classes for thirty tasks helps nobody.

Large processes have sections, and the model usually says where they are: an embedded
subprocess, a group, or the status changes the process goes through. Give each section a
package of its own, with its own `Service` and its own `WorkflowTaskHandler`. All of those
handler classes declare the same `bpmnProcess`. So it stays one workflow with one
`ProcessService`, while the code follows the structure of the model.

```
<base-package>.<usecase>
├── model/                       the aggregate, shared by all sections
├── application/                 section: the application is filled in
│   ├── Service.java
│   └── WorkflowTaskHandler.java
└── assessment/                  section: the application is assessed
    ├── Service.java
    └── WorkflowTaskHandler.java
```

A user task gets a package of its own as well. It is more than a `@WorkflowTask` method. A user
has to see the task and has to complete it, so it has an API of its own. Many user tasks also
carry state which lives until the task is completed, and which belongs to nobody else. Put the
classes which serve only that task into that package, its `ApiController` among them.

No blueprint shows this yet. The one which will show it comes with the Business Cockpit. So
treat this section as guidance, not as something to copy from a repository.

### Two namespaces per workflow module

**Workflow modules are not isolated by classloaders.** They end up in one runtime, on one
classpath. So two modules have to differ in two namespaces. Both are derived from the same
identifier:

| | Rule | Example |
|---|---|---|
| Classes | a unique Java package for the whole module | `com.acme.orders.shipment` |
| Resources | **every** resource in one subdirectory named after the workflow module ID | `src/main/resources/shipment/…` |

"Every resource" means every one: BPMN models (`<module-id>/processes/<adapter-id>/`), the
module's configuration file (`<module-id>/<module-id>.yaml`), templates, documents, schemas. A
resource at the classpath root works fine until a second workflow module ships a file of the
same name. Then one of them wins, without a word.

The single exception is the marker file `META-INF/workflow-module`, which contains the module
ID. It has to sit at that exact path, because that is how the module is recognised at all.

### Configuration per BPMS goes into a profile file

`application.yaml` of the application module holds what every engine needs. Everything which
belongs to one engine goes into the profile file of that engine, `application-camunda7.yaml`
and `application-camunda8.yaml`. Where a test needs it, it also goes into the workflow module's
test resources. Never mix the two. A reader has to be able to see what changes when the engine
changes. And an application which will migrate from one BPMS to another runs with both profiles
side by side.

The BPMS is named once, on the Maven command line. Every BPMS profile of a blueprint sets the
property `bpms`. The build filters it into `application.yaml` (`spring.profiles.active` or
`quarkus.config.profile.parent`), and surefire and failsafe pass it to the tests. Keep that
wiring when you copy a blueprint. Otherwise the engine has to be named twice, and the two will
drift apart.

If you name an adapter id whose adapter is not on the classpath, VanillaBP refuses to start,
because that is a configuration error. So a profile file never applies to the wrong engine.

## Placeholders

Identical in every blueprint. Replace all four consistently:

| Placeholder | Meaning | Example replacement |
|---|---|---|
| `blueprint.workflowmodule` | base package | `com.acme.orders` |
| `loanapproval` | use case identifier, Java package | `shipment` |
| `loan-approval` | use case identifier, kebab case: workflow module ID, resource directory, REST path | `shipment` |
| `loan_approval` | BPMN process ID | `shipment` |

The BPMN process ID in the model has to match the one used in the code. The resource directory
has to match the workflow module ID. Most startup errors of generated applications come from
replacing one of the four and forgetting another.

## Operating an application in a browser

Blueprints offer GET requests only, so you can walk through a process in a browser without any
tooling. Keep that property. At every wait state, log one complete, clickable URL for each
possible next step.

```
Accept -> http://localhost:8080/api/loan-approval/{id}/assess-risk/{taskId}?riskIsAcceptable=true
Deny   -> http://localhost:8080/api/loan-approval/{id}/assess-risk/{taskId}?riskIsAcceptable=false
```

Those logged URLs are also the cheapest way for you to see which state a workflow reached.

## Never do this

1. **No process variables.** All state lives in the workflow aggregate. Sequence flow
   conditions call methods on the aggregate instead.
2. **No BPMS API in application code**, so no `RuntimeService`, `ZeebeClient`, `CamundaClient`
   or any other engine class. The only compile-time dependency on the BPMS is the VanillaBP SPI
   (service provider interface). If you use an engine API, the hexagonal architecture is
   broken, and the application can no longer change its BPMS.
3. **No BPMS dependency in a workflow module.** A pure workflow module depends on
   `io.vanillabp:vanillabp-spring-boot-support` or `io.vanillabp:vanillabp-quarkus-support`,
   never on an adapter. Those modules do not expose BPMS APIs, on purpose. The adapter
   dependency belongs in the application module.
4. **No business state in the BPMN.** The model expresses the flow, not the data. Nothing an
   auditor would want to read belongs in the diagram.
5. **One aggregate per workflow.** Do not share an aggregate between two processes, unless the
   blueprint `bpmn-call-activity-decomposition` shows it explicitly. Do not store two business
   objects in one aggregate.
6. **No direct message exchange between workflow modules.** A process must never send a message
   to a process of another workflow module, because that couples them. Use the way
   `module-interaction` shows: an outgoing message becomes an internal API call, and the
   receiving module delivers a message through its own API.
7. **Do not let two branches of one workflow write the aggregate carelessly.** A parallel
   gateway, a non-interrupting boundary event and a multi-instance task each add a token. A
   token marks where a process instance currently is. So a second writer exists next to
   whatever the application writes from its API. JPA (Jakarta Persistence) saves the whole row.
   So the branch which commits second puts back what it read at its start, and the other
   branch's work is gone, without an exception and without a log line. Pick a strategy and say
   which one: an entity per phase in a 1:1 relation to the aggregate, `@DynamicUpdate` while
   the branches write different attributes, `@Version` plus a retry, or a relation of its own
   which is only ever added to. The blueprint `persistence-parallel-branches` shows the first,
   and explains when the others fit.
8. **One primary BPMN process per workflow aggregate.** VanillaBP builds one `ProcessService`
   per aggregate class, and that is what `ProcessService<Ride>` injects. So exactly one BPMN
   process is the one `startWorkflow` starts. If two classes declared a DIFFERENT `bpmnProcess`
   for that aggregate, the choice would be a coin flip. So the boot fails and names both
   classes and both processes. Declare the second process in `secondaryBpmnProcesses` of the
   class which carries the primary one. A process called by a call activity is the typical
   case. Several classes annotated with `@WorkflowService` for one aggregate are allowed, as
   long as each of them declares the SAME `bpmnProcess`. That makes
   [splitting a large workflow](#splitting-a-large-workflow) possible. This breaks easily when
   you combine two blueprints, because each brings a handler class which declares a
   `bpmnProcess` of its own.
9. **Do not copy reference documentation into the generated project.** Link it.
10. **Do not invent configuration specific to a BPMS.** If something seems to need it, it
    belongs in the adapter's wiki, not in the application.

## Where the documentation is

| Topic | Where |
|---|---|
| Using the SPI: annotations, aggregates, multi-instance, call activities | [spi-for-java](https://github.com/vanillabp/spi-for-java) |
| Concepts, workflow modules, platform integration, configuration | [adapter-platform-integration wiki](https://github.com/vanillabp/adapter-platform-integration/wiki) |
| Everything specific to one BPMS | the wiki of the respective [BPMS adapter](https://github.com/vanillabp/adapter-platform-integration/wiki/BPMS-adapters) |

Blueprints cover only what the first two provide, on purpose. If a task cannot be solved
without details of a BPMS, say so instead of inventing them.

## How we write

This section is about the texts of this repository, not about the application you build. It is
here because this file is the one an agent reads.

Most people who read this repository read English as a second language, and so does the
maintainer. Long sentences, rare words and stacked nouns slow them down. Write so that
nobody has to read a sentence twice.

Short main sentences, one thought each. One subordinate clause is enough. Active voice.
The common word instead of the rare one: `use` instead of `leverage`, `about` instead of
`regarding`, `so` instead of `consequently`, `has` instead of `possesses`. A technical term
stays a technical term, but say what it means the first time it turns up, and write an
abbreviation out once. If a sentence trips you up when you read it aloud, rewrite it.

This holds for every English text here: this file, [`README.md`](./README.md),
[`CONTRIBUTING.md`](./CONTRIBUTING.md), the summaries and reasons in `blueprints.yaml`, the
organisation page, and the texts of commits and pull requests. This repository has no wiki of its
own. If it gets one, the rule holds there as well, because a wiki clone has no `AGENTS.md` of its
own.

Nothing a program reads is renamed for the sake of language. The id of a blueprint, the keys of
the catalogue and the names of the BPMN element types stay as they are, because the schema, the
split job and the skills point at them.

Before and after, from this repository:

> Keep both classes even where the translation is a single line. The seam costs nothing while a
> process is trivial and is what keeps the business code readable once it is not; and a structure
> which is the same in every blueprint is one an agent can extend instead of having to rebuild.

becomes

> Keep both classes even where the translation is a single line. The seam costs nothing while a
> process is simple. It keeps the business code readable once the process is not simple any more.
> And an agent can extend a structure which is the same in every blueprint, instead of having to
> rebuild it.

That one is from this file. The next is the summary of `bpmn-async-task` in `blueprints.yaml`:

> Tasks which are not user tasks but still complete asynchronously - the handler returns
> immediately and the task is completed once the surrounding system answers.

becomes

> Tasks which are not user tasks but still complete later. The handler returns at once, and the
> task is completed once the surrounding system answers.
