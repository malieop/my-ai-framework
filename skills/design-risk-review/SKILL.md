---
name: Design Risk Review
description: Review relevant security, privacy, migration, rollout, observability, accessibility, and reliability risks during feature design and before slice readiness.
---

# Design risk review

Follow the [shared agreement and persistence rules](../../workflows/feature-design.md#shared-agreement-and-persistence-rules). This skill grants no permissions or role changes.

Review only concerns that affect the next useful slice. Reuse current findings and revisit them when constraints, evidence, or scope change. Do not require empty sections, speculative infrastructure, a separate report, or an approval gate for every category.

| Concern | Questions when relevant |
| --- | --- |
| Authorization and sensitive data | Who may perform or observe this action? Which data crosses trust boundaries? Are retention, redaction, or audit requirements affected? |
| Compatibility and migrations | Which clients, contracts, events, or stored data change? Can old and new versions coexist? Is migration or recovery required? |
| Rollout and rollback | How can exposure be controlled and regressions detected? Can the change be reversed safely, including data effects? |
| Observability | What evidence will show success or failure? Are logs, metrics, traces, or alerts needed without exposing sensitive data? |
| Accessibility | Can affected users complete the flow with keyboard and assistive technology? Are labels, focus, errors, and contrast appropriate? |
| Reliability and failure behavior | What happens on timeout, retry, duplicate delivery, partial failure, or unavailable dependency? Which guarantees are actually agreed? |

1. Inspect relevant evidence; do not invent compliance duties, operational capabilities, or numerical targets.
2. For each material finding, state the evidence or assumption, consequence, and proposed mitigation or open question.
3. Classify findings as blocking the next slice or explicitly deferred with a reason; record an owner when known.
4. Put architecture-level findings in the proposal and slice-specific behavior or checks in the slice. Link instead of duplicating.
5. Convert applicable mitigations into observable acceptance criteria. Apply the workflow's acceptance and save rules.

Return a short relevant-findings summary, including blockers and deferrals. If none are material, say so briefly; do not fabricate risks to fill the checklist.
