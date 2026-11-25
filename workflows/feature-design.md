# Feature design workflow

## Goal and use

Design through conversation. Commit only to choices needed for the next useful increment while exploring enough context to avoid obvious mistakes.

Use with [Feature Design Partner](../agents/feature-design-partner.md). The modes below are optional activities, not sequential approval gates or separate workers. Move freely between them; do not require a complete proposal before scoping the first slice.

Identify the feature and target repository. Read its instructions and existing feature docs before proposing new artifacts. Ask for missing access or excerpts rather than pretending to inspect them.

## Skills and routing

Load the relevant skill when its procedure is needed, not every skill at session start. In tools without a skill loader, read the linked `SKILL.md` directly. Resolve links against each document's directory.

| Mode / activity | Skill | Useful output |
| --- | --- | --- |
| Frame | [feature-design-frame](../skills/feature-design-frame/SKILL.md) | Problem, outcome, scope, constraints, unknowns. |
| Explore | [feature-design-explore](../skills/feature-design-explore/SKILL.md) | Alternatives, recommendation, evidence, diagrams when useful. |
| Agree | [feature-design-agree](../skills/feature-design-agree/SKILL.md) | Explicitly accepted choice, rationale, agreement history. |
| Slice | [feature-design-slice](../skills/feature-design-slice/SKILL.md) | Small end-to-end outcome and observable criteria. |
| Reconcile | [feature-design-reconcile](../skills/feature-design-reconcile/SKILL.md) | New evidence, affected decisions, proposed replacement. |
| Cross-cutting risks | [design-risk-review](../skills/design-risk-review/SKILL.md) | Relevant risks and their impact on the next slice. |

Use design-risk-review during exploration and before declaring slice readiness. Reuse a current review; revisit it when scope, evidence, or constraints change. It is not another mandatory report or approval gate.

## Shared agreement and persistence rules

These rules are authoritative for every mode and skill:

- Only explicit user confirmation accepts a significant choice. Use stable IDs such as `P-01`, with proposed, accepted, or superseded status. Assumptions and unknowns are not agreements.
- Overall proposal status does not accept every item. Deferred nonblocking questions may remain open.
- Architectural acceptance and write authorization are separate. Drafting or saving does not accept a choice; only explicit confirmation does.
- By default, save feature-design Markdown under the target project's `docs/features/` when useful and permitted. Respect a user's request not to save or to limit writes. Request permission for other locations or file types; tool permissions still apply.
- At meaningful progress, identify affected artifacts and unsaved changes. These are checkpoints, not writes after every message.
- Save only within the authorized scope and tool permissions. Verify contents and cross-references afterward. If saving is declined, unavailable, or unsuccessful, report documentation pending. Markdown in chat is not saved.
- Preserve accepted choices and rationale. Before changing one, explain new evidence and affected artifacts, obtain explicit agreement, then mark the old item superseded, link its replacement, and append confirmation and rationale to history.
- Cite repository paths with headings or line ranges, URLs for external sources, and labels for user-provided excerpts. Do not infer deployed behavior from source alone.
- Record implementation status separately: not checked, not implemented, partially implemented, or implemented with cited evidence. Never fabricate commit IDs, PRs, or validation.

### STE100-inspired writing rules

Apply these rules to feature-design replies, drafts, and saved Markdown, including direct skill use.
They match the plan agent's explicit writing rules, not full ASD-STE100 compliance.

- Omit preambles and postscripts.
- Limit steps to 15 words and statements to 20 words.
- Use active voice and imperative forms where appropriate.
- Use simple verbs: `use`, not `utilize`; `show`, not `display`; `start`, not `initiate`.

Keep technical names, code identifiers, and quoted source text unchanged. Do not impose the plan agent's output template.

## Artifacts and checkpoints

Use the project's existing Markdown artifacts within `docs/features/` when appropriate; otherwise default to `docs/features/<feature-name>/`. If conventions require another location, request permission and any necessary scoped configuration change rather than bypassing restrictions.

The overview, proposal, and slices together form the durable spec. Do not create a duplicate `spec.md`, separate ADR, or decision ledger by default. Read each template only when drafting its artifact; omit irrelevant sections.

| Artifact | Owns | Updated by |
| --- | --- | --- |
| [Overview](../templates/feature/overview.md) | Shared problem, outcome, scope, constraints, non-goals, sources, unknowns. | Frame |
| [Proposal](../templates/feature/proposal.md) | Architecture, alternatives, rationale, decision IDs, diagrams, agreement history. | Explore, Agree, Reconcile |
| [Slice](../templates/feature/slice.md) | Slice behavior, contracts, linked accepted decisions, criteria, blockers. | Slice, Reconcile |

Link shared context rather than duplicating it. Keep future slices as short outlines until needed; target fewer than 150 lines per detailed slice. Risk findings belong in the relevant proposal or slice, not a separate required document.

## Readiness and session continuity

A slice is design ready when it has a useful outcome, testable criteria, required accepted choices, relevant risk findings addressed or explicitly deferred, and no unresolved blocking questions.

- **Design ready, documentation pending:** design criteria are met, but required context or changes remain unsaved or inconsistent. Identify pending artifacts; do not declare handoff readiness.
- **Ready for handoff:** design criteria are met and all required implementation context is saved in consistent, linked repository artifacts. No required choice, contract, criterion, or rationale depends solely on chat.

Before declaring handoff readiness, read the saved slice and relevant linked artifacts as a receiving agent would, without relying on the original conversation. Verify outcome, scope, accepted decision IDs and rationale, contracts, acceptance criteria, blockers, and deferred questions. Check that paths and IDs resolve and diagrams agree with prose. Report gaps rather than assuming the implementer can infer missing context.

At pause, summarize proposal status, accepted IDs, blockers, deferred questions, next slice, and unsaved changes. On resume, reload artifacts and reconcile with new evidence.

Hand off the target repository, slice path, overview and proposal paths, required accepted IDs, blockers, deferred questions, and evidence-based implementation status. Link rather than repeat the spec. Tell the receiving agent to read repository instructions and linked artifacts first and flag conflicts with observed implementation rather than silently change accepted choices.

This role does not implement code, merge changes, publish documents, or claim production validation. Implementation requests require switching to Build or another implementation agent. The [Feature Implementor](../agents/feature-implementor.md) provides a dedicated role with [implementation planning](feature-implementation.md) and separately authorized execution; design acceptance alone does not authorize coding.
