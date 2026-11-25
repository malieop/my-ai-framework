# Plan: Loop Guardrail + Implementor Role Narrowing

## Goals
1. Stop plan agents from re-exploring the same topic endlessly.
2. Remove overlap: efficient-plan owns planning; feature-implementor owns execution.

## Confirmed Decisions
- Guardrail behavior: report status (Known/Unknown/Tried), then ask user.
- Guardrail scope: per topic; new topic resets counter.
- Implementor without an approved plan: refuse, route to planner (efficient-plan or feature-design).
- efficient-plan stays generic. No coupling to `docs/features/`. User supplies slice paths in prompts.
- feature-implementor stays, narrowed to executor. Its value: authorization gates, restrictive permissions, reconciliation, evidence.

## Target Files

### Personal agents (regular files in `~/.config/opencode/agents/`)
1. `efficient-plan.md` — add Guardrail section.
2. `plan.md` — add identical Guardrail section.

### Framework repo (`/Users/diogocoelho/repos/my-ai-framework/`) — source of truth
3. `agents/feature-implementor.md` — narrow role to executor; add intake gate and how-rules.
4. `workflows/feature-implementation.md` — intake requires pre-existing approved plan; keep skill reference (tests assert it); add execution conventions.
5. `skills/implementation-planning/SKILL.md` — reframe: planning sessions produce the plan; implementor verifies it.
6. `adapters/opencode/agents/feature-implementor.md` — update description and intake note. Symlinked to live config.
7. `README.md` — update "Implement an accepted slice" flow: plan first, then hand off.
8. `tests/feature-implementation-pilot.md` — update scenario: plan exists before implementor starts.

## Change Details

### A. Exploration Loop Guardrail (files 1-2)
Insert after `## Responsibility`, before `## Planning Workflow`:

```markdown
## Exploration Loop Guardrail
- Track exploration rounds per topic (searches, reads, subagent calls on the same question).
- Stop after 2 unproductive rounds on that topic. 3 is the hard maximum.
- A round is unproductive when it returns no new facts or the same results.
- When you stop, post this status before anything else:
  - **Known:** facts confirmed so far, with file paths.
  - **Unknown:** what is still missing.
  - **Tried:** what you already searched or read.
- Then ask the user how to proceed: new direction, more context, or continue with assumptions.
- Do not resume exploring that topic until the user answers.
- A new topic resets the counter.
```

### B. Implementor intake gate (files 3, 4, 6)
- Require two inputs before any work: (a) accepted slice or design artifacts, (b) approved implementation plan.
- Missing either → stop. Tell user to run efficient-plan or feature-design first. Do not explore or draft.
- Keep staleness recheck: verify plan against current code before executing; surface drift.
- Adapter description becomes: "Execute an approved implementation plan for an accepted feature slice after explicit authorization".
- Remove "Use implementation-planning when preparing the plan" from adapter. Skill stays referenced in workflow for planning sessions.

### C. Execution conventions — the "how" rules (files 3, 4)
Add to agent's Working behavior and workflow's Execution section:

```markdown
## Execution conventions
- Before writing code, find at least one analogous implementation in the repository. Cite its path.
- Mirror existing conventions: naming, file placement, error handling, logging, test structure.
- Reuse existing utilities and helpers. Do not add parallel ones.
- Introducing a new pattern, library, or structure requires explicit user confirmation first.
- Tests mirror neighboring test files: same fixtures, style, and assertion patterns.
- Keep the smallest viable diff. No unrelated refactors, renames, or formatting sweeps.
- If no analogous pattern exists, say so and propose one before writing code.
```

### D. Skill + docs reframe (files 5, 7, 8)
- Skill: planning happens in a planning session (plan agent or design handoff); output is the plan the implementor executes and verifies.
- README flow: 1) design slice, 2) plan implementation in a planner agent, 3) approve plan, 4) hand plan to implementor with "implement this plan".
- Pilot test: scenario starts with saved slice + approved plan.

## Verification
1. Run `python3 -m unittest discover -s tests -v` in the framework repo. All pass.
2. Check `test_framework.py` line ~182-192 assertions still hold (workflow references skill; agent files exist).
3. Re-read both personal agents; confirm Guardrail section placement.
4. Confirm symlinks intact: `rtk ls -la ~/.config/opencode/agents/`.
5. Behavioral smoke test: fresh implementor session without plan → expect refusal and routing to planner.
6. Behavioral smoke test: force dead-end search in efficient-plan → expect Known/Unknown/Tried status and question.

## Out of Scope
- No changes to feature-design agent or design workflow.
- No framework-awareness added to efficient-plan or plan.
- build agent unchanged.
