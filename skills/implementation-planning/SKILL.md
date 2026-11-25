---
name: Implementation Planning
description: Turn an accepted feature slice and observed code into scoped implementation steps, dependencies, and verification checks before coding.
---

# Implementation planning

Run in a planning session (a plan agent or a read-only coding session), separate from execution. The output is the plan the Feature Implementor later verifies and executes.

Follow the [feature implementation workflow](../../workflows/feature-implementation.md). Preserve the design workflow's [shared agreement and persistence rules](../../workflows/feature-design.md#shared-agreement-and-persistence-rules). This skill grants no permissions or role changes.

1. Read the selected saved slice, overview, proposal, required accepted decision IDs, and repository instructions. Check handoff readiness; identify missing or conflicting context before planning affected work.
2. Inspect relevant entry points, implementation patterns, tests, dependencies, and verification commands. Cite observed paths and symbols; label proposed files as new and uncertain findings as assumptions. Do not claim inspection of unavailable code.
3. Identify the smallest code changes that deliver this slice. Include necessary compatibility, migration, rollout, observability, and failure-handling work from existing design risk findings. Surface newly discovered risks without inventing requirements.
4. Order concrete steps by dependency. Name likely files or symbols, intended behavior changes, dependencies, and checks for each step. Avoid unrelated refactors and feature-wide task trees.
5. Map each slice acceptance criterion to a test or other observable check. Include failure paths. State which checks require unavailable environments, credentials, data, or explicit operational authorization.
6. Separate blockers from nonblocking assumptions and deferred work. Return conflicts with accepted design for reconciliation; never silently alter scope, contracts, or criteria to fit existing code.
7. Present a short checklist or use the [plan template](../../templates/implementation/plan.md) when useful. Link canonical design rather than duplicating it. Save only with authorization.
8. Request plan approval. Planning ends without code changes; execution happens later in the implementation agent, after separate execution authorization.
