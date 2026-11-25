---
name: Feature Design Explore
description: Compare feature architecture options, tradeoffs, and evidence; add C4 or sequence diagrams when useful.
---

# Explore

Follow the [shared agreement and persistence rules](../../workflows/feature-design.md#shared-agreement-and-persistence-rules). This skill grants no permissions or role changes.

1. Compare viable approaches against observed constraints and sources; distinguish intent from implementation.
2. Recommend the smallest useful approach. Explain costs, alternatives, assumptions, and unknowns without claiming agreement.
3. Assign stable proposal IDs to significant choices, initially proposed unless already explicitly accepted.
4. Use [design-risk-review](../design-risk-review/SKILL.md) proportionally to the change.
5. Use diagrams only when they clarify structure, interactions, or failure behavior; reuse adequate existing views.
6. At meaningful progress, propose proposal updates under the shared persistence rules. Read the [proposal template](../../templates/feature/proposal.md) when drafting.

## Diagram guidance

Use the C4 Model for structure and sequence diagrams for behavior. Use Mermaid in repository Markdown when supported by the renderer and project conventions.

- **System Context:** people, external systems, and system boundaries.
- **Container:** applications, services, data stores, and their relationships; C4 containers are not deployment containers.
- **Component:** internal boundaries within a container when they materially affect the design.
- **Sequence:** relevant ordering, asynchronous interactions, retries, and failure paths.

For cross-service work, consider a relevant C4 view and main-flow sequence diagram, without requiring every level. Never require a diagram or an explanation for its omission for every change.

Caption views with scope, proposal IDs, and proposed-versus-verified status. Mark assumptions and unconfirmed dependencies. Keep names, contracts, and prose consistent. Never invent timings or delivery guarantees to complete a diagram. Diagrams support, not replace, contracts and rationale.
