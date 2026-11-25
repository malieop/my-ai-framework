---
name: Jira Story Writing
description: Write clear, well-structured Jira stories with an explicit "What we really want" section and testable acceptance criteria. Use when creating, rewriting, or improving a Jira story/ticket description, adding acceptance criteria, or fixing a ticket that is a wall of text.
---

# Jira story writing

Pattern for writing Jira stories that state plainly what we want and how we know it is done.
Canonical examples: VCI-6581 and VCI-6582 (Talkdesk VCI project, 2026-11-13).

## Description structure (required sections, in order)

1. **Context** — Why the work exists. Link the design doc/TDD (with version if relevant), the parent epic/feature, and sibling tickets it depends on or feeds. Two to four sentences. Assume the reader has no prior context.
2. **What we really want** — The plain-language goal. No implementation jargon. Answer: "when this is done, what is true that is not true today?" State the consumer benefit. This is the section most tickets lack — write it first.
3. **In scope** — Bulleted. Concrete, verifiable items only. Reference exact files, classes, or events when known.
4. **Out of scope** — Bulleted. Each excluded item names the ticket that owns it, if one exists. Explicit exclusions prevent scope creep and duplicate work.
5. **Open design points (if any)** — Each marked with its blast radius (e.g. "blocks sizing"). Name the teams or tickets that must resolve it. Never bury a blocking unknown in prose.
6. **Acceptance criteria** — Numbered list, one behavior per criterion, Given/When/Then phrasing.

## Acceptance criteria rules

- One verifiable behavior per criterion. No "and" chains — split them.
- Given/When/Then form: *Given \<precondition\>, when \<action\>, then \<observable result\>.*
- Always include the negative/baseline case: what happens on the default path (e.g. field absent or default value, no regression).
- Always include backward compatibility when changing a contract: existing consumers behave unchanged; name the consumer ticket that handles the new field.
- Include the end-to-end proof when the story feeds a downstream consumer (e.g. verified in staging with the consumer's ticket).
- Avoid implementation instructions in ACs — they belong in In scope.

## Cross-linking rules

- Link dependencies both ways in the text: the story names what it needs and what it feeds.
- Use plain issue keys — Jira auto-creates smart links.
- Keep summaries in the `[Component]: what` style when the project uses it.

## Anti-patterns (do not write these)

- Wall-of-text single paragraphs mixing context, scope, and rationale.
- Descriptions that only describe *how* (implementation) without *why* or *what done means*.
- ACs like "it works" / "code is deployed" / "tests pass" — not observable behaviors.
- Stale contradictions: if the architecture changed (design doc version bump), say so explicitly and name what was dropped.
- Hidden blockers: an unresolved cross-team question must be a named section, not a footnote.

## Workflow

1. Draft the description following the section order above.
2. Confirm ambiguous scope or intent with the requester before writing to Jira (e.g. rejection style, ownership, event coverage).
3. Write through the available Jira integration (MCP tools or the delegated Atlassian agent), with full section content spelled out. Never paste unformatted wall-of-text — Jira renders headings, bullets, and numbered lists; use them.
4. Verify rendering (e.g. via `renderedFields`): headings, lists, and line breaks must be present.
5. Record created or updated issue keys in the relevant plan document.
