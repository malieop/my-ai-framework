# Feature Design and Implementation

A portable, conversational framework for designing features through small proposals and implementing accepted slices with explicit authorization.

This implements the first prototype for [Growth Action 1](ai-capabilities-growth-actions.md#growth-action-1-de-waterfalling-architecture--iterative-ai-navigated-decision-making--traceability).

## Start a session

1. Give your assistant [the agent instructions](agents/feature-design-partner.md).
2. Give it [the workflow](workflows/feature-design.md), access to its linked skills, and the target repository.
3. Say: “Let's design `<feature>`. Start by understanding the problem; don't write files yet.”
4. Discuss the proposal, confirm choices, then request the documentation updates you want.

For an assistant without file access, paste those documents, the relevant skill instructions, and source excerpts into its conversation. Ask for proposed Markdown rather than filesystem edits.

These instructions are portable. Optional [OpenCode adapters](adapters/opencode/README.md) expose them as selectable agents and commands.

## Agent, workflow, and skills

- The agent owns role boundaries and conversational behavior. It is strictly design-only, with authorized spec writes; implementation requires another agent.
- The workflow owns shared agreement, persistence, artifact, and readiness rules.
- [Skills](skills/) own the Frame, Explore, Agree, Slice, Reconcile, and cross-cutting risk-review procedures. Load them on demand, not as mandatory sequential gates.
- Templates provide artifact structure; they are not independent copies of the workflow.

## Implement an accepted slice

1. Plan the slice in a planning session: a plan agent or a coding assistant in read-only mode using the [implementation-planning skill](skills/implementation-planning/SKILL.md). Say: "Plan implementation of this slice. Inspect code, but do not change files yet."
2. Review and approve the plan. Authorize saving separately if you want a durable plan.
3. Give your coding assistant the [Feature Implementor instructions](agents/feature-implementor.md), the [implementation workflow](workflows/feature-implementation.md), the target repository, the saved design slice, and the approved plan.
4. Say: "Implement this approved plan" when ready to authorize code changes.

The planning session uses the skill to identify code changes, dependencies, execution order, and acceptance checks. The implementor requires that approved plan, verifies it against current code, executes within scope, and returns design conflicts for reconciliation instead of silently redesigning.

An existing Build agent can use the same workflow; a dedicated agent is optional. These documents remain portable instructions, not installed agents or tool permissions. Plans can stay as short checklists. Optional saved plans follow project conventions or use `docs/features/<feature-name>/implementation/01-<slice-name>-plan.md` and the [plan template](templates/implementation/plan.md).

The framework remains read-only during implementation sessions. Execution authorization does not authorize commits, publishing, deployments, or external changes.

For OpenCode V2, [install repository links](adapters/opencode/README.md) and register the linked skill source once. This repository remains the source of truth; routine updates need no copied definitions or global configuration edits.

The framework must remain read-only during feature-design sessions. Shell access is for research, not a way to bypass edit restrictions. A narrow inspection-command allowlist reduces prompts but is not a filesystem sandbox.

## Feature artifacts

Use the target project's existing conventions when available. Otherwise:

```text
docs/features/<feature-name>/
├── overview.md
├── proposal.md
└── slices/
    └── 01-<slice-name>.md
```

Copy the [templates](templates/feature/) only when an artifact is useful. Don't create a complete documentation bundle before the discussion starts.

- **Overview:** problem, outcomes, scope, constraints, and source links.
- **Proposal:** evolving architecture, alternatives, rationale, open questions, and agreement history.
- **Slices:** small, testable increments based on explicitly accepted choices.

There is no separate decision ledger. The proposal preserves architectural choices and their history.

## Example prompts

- “Challenge this proposal against our existing architecture.”
- “Which parts are accepted, proposed, assumed, or unknown?”
- “What can we defer until the next slice?”
- “Define the smallest useful end-to-end slice.”
- “Implementation exposed this constraint. What needs to change?”
- “Why did we choose this approach? Show the source.”

## Validate the prototype

Run the structural checks with Python 3 from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Then run the [behavioral pilot](tests/feature-design-pilot.md) in a fresh assistant session. Structural checks validate artifacts, not agent judgment or production effectiveness.

See the [initial validation results](tests/feature-design-pilot-results.md) for the structural test run and synthetic conversation smoke test.

Success means a sourced, explicit agreement; one useful slice under 150 lines; and a constraint change handled without silently changing accepted history. Validate production outcomes separately using the growth action's metrics.
