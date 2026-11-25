# AI Capabilities Investigation & Engineering Growth Actions

## 1. Overview & Context

This document outlines an investigation into AI capabilities and tools across the end-to-end Software Development Life Cycle (SDLC) — from requirements investigation and system documentation to coding, testing, deployment, and runtime observability.

It defines **3 actionable, high-impact Growth Actions** tailored for a software developer. These actions tackle real challenges in current practices (such as spec overload and waterfall rigidity) and introduce emerging AI paradigms (such as multi-agent orchestration and autonomous observability).

---

## 2. SDLC AI Capability Map

| SDLC Phase | Current Friction / Challenge | Next-Gen AI Solution | Key Tooling |
|---|---|---|---|
| **Discovery & Requirements** | Large PRDs with scattered context; hidden edge cases in complex domain code | Interactive domain exploration agents and thin-slice decomposition | `codebase-explorer`, `td-jira`, `td-atlassian` |
| **Architecture & Specs** | "Spec overload" and mini-waterfall traps; decisions get buried and hard to follow | Just-In-Time (JIT) decision ledgers, interactive decision navigators, bidirectional spec-code sync | OpenSpec (`openspec-propose`), JIT ADRs, Mermaid sequence tools |
| **Coding & Testing** | Boilerplate domain wiring; complex test setups with brittle mocks | Agentic TDD, test DSL synthesis from real event timelines, and autonomous subagents | Test DSL generators, `Faker`, `unit-test-format`, RTK token killer |
| **Code Review** | Large diffs causing reviewer fatigue; unnoticed domain regressions | Guided visual diff self-review and subagent code audits | `plannotator-review`, `Code Reviewer` |
| **Deploy & Observe** | Manual verification across microservices; slow log parsing during incidents | Autonomous staging deploys, E2E test runs, and DQL event timeline reconstruction | `deploy-stg`, `quality-tester`, `dynatrace` subagent / DQL |
| **Frontier Capabilities** | Repetitive manual chores; siloed external tools | Multi-agent swarms, custom Model Context Protocol (MCP) servers, closed-loop self-healing | Custom MCP, Agent orchestrators, `pr-validation-failures` |

---

## 3. The 3 Growth Actions

### Growth Action 1: De-Waterfalling Architecture — Iterative, AI-Navigated Decision Making & Traceability

#### Problem Statement
Spec-to-Code workflows frequently devolve into a "mini-waterfall" pattern: engineers make dozens of architecture and contract decisions upfront in large specification documents. During implementation, developers become overwhelmed tracking which decisions apply to what, why decisions were made, or how to adapt when implementation realities diverge from the spec.

#### Action Objective
Replace monolithic upfront spec-writing with an iterative, AI-navigated decision workflow. Decompose features into thin vertical slices, maintain lightweight decision ledgers, and use AI agents to retrieve decision context on demand.

#### Core Practices & Tooling
1. **Thin Vertical Slicing:** Use AI agents to break down large feature initiatives into independent, incremental vertical slices (e.g., single API contract + single domain handler + single test slice) instead of full-system upfront specs.
2. **AI Decision Navigator:** Use conversational AI as an interactive decision query companion inside the IDE (e.g., querying *"Why did we choose synchronous ack over async outbox for this flow?"* or *"What error codes did we define for participant timeouts?"*) to eliminate manual document digging.
3. **Just-In-Time (JIT) Decision Ledgers:** Capture bite-sized, contextual ADRs (Architectural Decision Records) at the moment choices occur, linked directly to code commits.
4. **Bidirectional Reality Sync:** When real-world code constraints require diverging from a plan, prompt the AI agent to update the decision ledger and dependent slices immediately, keeping docs fresh without cognitive fatigue.

#### Deliverables & Milestones
- **M1 (Month 1):** Define and document a standardized prompt workflow for thin-slicing initiatives and querying past architectural decisions.
- **M2 (Month 2):** Execute 2 production features using thin vertical slicing with an AI-maintained decision ledger.
- **M3 (Month 3):** Share a team guide on avoiding spec-to-code waterfall traps and navigating decisions with AI copilots.

#### Success Metrics
- Average spec document length reduced to single-slice scopes (< 3 pages / < 150 lines per slice).
- Zero forgotten or contradicted architectural decisions during pull request reviews.
- Lead time per slice reduced by ≥ 35%.

---

### Growth Action 2: Safe Ship & Observe — AI-Driven Deployment, E2E Evidence & Telemetry Feedback Loops

#### Problem Statement
Verifying voice call flows across distributed microservices requires manual staging deployments, manual test calls, and tedious log searching across multiple observability systems to confirm participant states and event sequences.

#### Action Objective
Automate the deployment verification and diagnostic lifecycle. Leverage AI observability agents to trigger staging deployments, execute automated E2E tests, and reconstruct cross-service event timelines directly from logs to attach verified evidence to pull requests.

#### Core Practices & Tooling
1. **Automated Deploy & Test Triggering:** Use deployment skills (`deploy-stg`) and E2E test automation tools (`quality-tester`) to trigger staging runs autonomously from feature branches.
2. **AI-Driven Telemetry Reconstruction:** Delegate log analysis to the Dynatrace subagent using targeted DQL queries to extract interaction IDs, call legs, and participant transitions without manual dashboard hunting.
3. **Automated PR Evidence Bundles:** Generate structured markdown evidence summaries showing chronological timelines of domain events, PAS actions, and state transitions, and post them directly to pull requests.
4. **Accelerated Incident Diagnosis:** Use log-timeline agents (`acceptance-test-events-timeline`) during defect triage to turn production/staging stack traces and log streams into clear fact reports.

#### Deliverables & Milestones
- **M1 (Month 1):** Adopt the Dynatrace DQL and `quality-tester` agent workflow to verify feature branches on staging.
- **M2 (Month 2):** Attach automated, AI-compiled telemetry evidence packages to 100% of major feature pull requests.
- **M3 (Month 3):** Author an engineering runbook demonstrating how to use AI observability agents to triage staging and production call issues in minutes.

#### Success Metrics
- Staging verification and evidence collection time reduced by ≥ 50%.
- Mean Time to Detect / Diagnose (MTTD) interaction defects cut from hours to under 15 minutes.
- 100% of critical PRs verified with attached telemetry evidence before merging.

---

### Growth Action 3: Frontier AI Capabilities & Next-Gen Ways of Working — Research, Prototyping & Enablement

#### Problem Statement
AI tooling evolves at a rapid pace beyond single-prompt coding assistants (e.g., multi-agent coordination, Model Context Protocol, autonomous background workers). Without deliberate exploration and evaluation, engineering workflows remain constrained to basic autocompletion.

#### Action Objective
Actively investigate, prototype, and benchmark emerging AI capabilities and novel ways of working. Identify high-leverage workflows and transition viable experiments into production engineering practices for the team.

#### Core Exploration Areas & Novel Paradigms
1. **Model Context Protocol (MCP) Integration:** Research and build custom MCP servers to connect internal APIs, test runners, or domain state inspection tools directly into AI agents.
2. **Multi-Agent Orchestration & Parallel Swarms:** Experiment with orchestrating specialized worker agents (e.g., running background refactoring, dependency updates, or documentation updates concurrently while the engineer focuses on core business logic).
3. **Closed-Loop Self-Healing Agents:** Prototype agents that observe CI build/test failures (`pr-validation-failures`), parse error logs, hypothesize fixes, apply code patches, and rerun checks autonomously.
4. **Frontier Model & Token-Efficiency Benchmarks:** Evaluate next-generation reasoning models and context-efficiency tools (such as RTK) on complex distributed systems challenges to establish cost-effective, high-accuracy prompting patterns.

#### Deliverables & Milestones
- **M1 (Month 1):** Conduct a proof-of-concept for an internal tool integration via a custom MCP server or multi-agent task runner.
- **M2 (Month 2):** Prototype an autonomous CI/test triage agent that diagnoses build failures and suggests fixes.
- **M3 (Month 3):** Publish an **"AI Developer Capabilities Radar"** document summarizing evaluated tools, ROI metrics, and practical recommendations, accompanied by a team tech talk or demo.

#### Success Metrics
- At least 1 validated novel AI workflow adopted into regular team practice.
- Documented ≥ 2x productivity improvement in targeted automated prototype tasks.
- 1 team demo / knowledge-sharing session delivered.
