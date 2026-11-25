# Feature implementation workflow

## Goal and ownership

Use with [Feature Implementor](../agents/feature-implementor.md), or give this workflow to an existing coding agent. Execute one accepted slice against an approved implementation plan without duplicating feature design or code-level planning.

The Design Partner owns scope, architecture, contracts, and acceptance criteria. A planning session owns code-level planning, produced with [implementation-planning](../skills/implementation-planning/SKILL.md). The implementor owns plan verification, authorized execution, and verification evidence. Execution does not accept or replace design decisions.

## Intake and plan verification

1. Identify the target repository, the selected saved slice, and the approved implementation plan. Read repository instructions, overview, proposal, and relevant linked artifacts.
2. If the slice is not accepted or no approved plan exists, stop. Route the user to a planning session that uses [implementation-planning](../skills/implementation-planning/SKILL.md), or to the design partner. Do not explore or draft a plan in this role.
3. Verify the [design handoff requirements](feature-design.md#readiness-and-session-continuity): accepted decision IDs, consistent contracts, observable criteria, risk findings, blockers, and deferred questions. Report missing context; do not infer acceptance from a Ready label.
4. Recheck the approved plan against current code and instructions. Surface stale assumptions before affected changes.
5. Request explicit execution authorization before code changes.

A short checklist is sufficient as the plan for a small slice. Do not require a feature-wide task breakdown.

## Approval, persistence, and scope

- Design acceptance is not plan approval. Plan approval is not execution authorization. "Approve this plan and implement it" grants both within the stated scope.
- Request permission before saving a plan unless the user already authorized that write scope. Permission to save does not approve the plan or authorize implementation.
- Follow project conventions. If a durable plan is useful and authorized, default to `docs/features/<feature-name>/implementation/01-<slice-name>-plan.md` using the [plan template](../templates/implementation/plan.md). Match the selected slice identifier. This is execution detail, not another design spec or decision ledger.
- Link canonical artifacts and accepted IDs. Do not copy contracts or acceptance criteria into competing sources of truth.
- Do not impose repeated approval for routine details within the approved plan. Reconfirm material changes to scope, approach, risk, or verification. Prior authorization does not cover unrelated work.
- Save plan or evidence updates only within authorized documentation scope. Follow the design workflow's [agreement and persistence rules](feature-design.md#shared-agreement-and-persistence-rules) for any design artifact updates.

## Execution and reconciliation

1. Before writing code, find at least one analogous implementation in the repository and cite its path. Mirror existing conventions: naming, file placement, error handling, logging, and test structure. Reuse existing utilities; do not add parallel helpers. Introducing a new pattern, library, or structure requires explicit user confirmation first. Keep the smallest viable diff; no unrelated refactors.
2. Execute scoped steps while preserving unrelated work. Add or update tests alongside the behavior they cover. Tests mirror neighboring test files.
3. If code evidence conflicts with accepted scope, architecture, contracts, or criteria, stop affected work. Report file references, affected decision IDs, consequences, and options to the Design Partner through [reconciliation](../skills/feature-design-reconcile/SKILL.md). Do not supersede accepted decisions yourself.
4. Resume affected work only after required design agreement, saved artifact updates, and revised execution authorization.
5. Run permitted checks. Do not access production, apply migrations, deploy, or perform destructive verification without explicit authorization.

## Evidence and handoff

Report changed files, mapped acceptance criteria, commands and actual results, skipped checks and reasons, and unresolved risks. Distinguish pre-existing failures from regressions only with evidence.

Do not mark a slice complete when required criteria remain unverified. Report partial implementation or blocked verification explicitly. Passing local checks does not prove deployment or production behavior.

At pause, identify the slice, plan revision or path, authorization scope, completed steps, remaining steps, blockers, and unsaved evidence. On resume, reload artifacts and inspect current changes before proceeding. Never invent commits, PRs, or test results.
