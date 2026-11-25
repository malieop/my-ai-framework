---
name: Feature Design Slice
description: Define the smallest useful end-to-end implementation slice with contracts, accepted decisions, and observable acceptance criteria.
---

# Slice

Follow the [shared agreement and persistence rules](../../workflows/feature-design.md#shared-agreement-and-persistence-rules). This skill grants no permissions or role changes.

1. Identify one useful end-to-end outcome and explicit exclusions, not just a technical layer.
2. Link required accepted proposal IDs and shared context instead of copying the proposal.
3. Specify only the behavior, API/event/data contracts, and failure handling needed for this increment.
4. Write observable happy-path and failure acceptance criteria. Identify dependencies, blockers, and deferred questions.
5. Apply [design-risk-review](../design-risk-review/SKILL.md), reusing current findings where sufficient.
6. Draft from the [slice template](../../templates/feature/slice.md) when needed. Keep the slice under 150 lines and future slices as short outlines.
7. Follow shared persistence and readiness checks before claiming readiness or handing off. Do not implement the slice in this role.
