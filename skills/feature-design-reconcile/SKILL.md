---
name: Feature Design Reconcile
description: Reconcile new constraints or implementation evidence with accepted feature decisions while preserving rationale and history.
---

# Reconcile

Follow the [shared agreement and persistence rules](../../workflows/feature-design.md#shared-agreement-and-persistence-rules). This skill grants no permissions or role changes.

1. Cite the new evidence. Separate observed implementation, documented intent, user facts, and unknowns.
2. Identify affected choices, diagrams, slices, contracts, risk findings, and acceptance checks.
3. Explain the conflict and recommend a replacement without silently changing accepted intent.
4. Apply the shared change-control rule before superseding accepted choices or saving changes.
5. After authorization and agreement, update affected artifacts, retaining superseded rationale and linking replacement IDs.
6. Revisit relevant [risk findings](../design-risk-review/SKILL.md) and verify consistency and readiness under the workflow.

Flag implementation conflicts for the receiving implementation agent; do not fix application code in this role.
