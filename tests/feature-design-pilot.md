# Behavioral pilot: reliable webhook delivery

Run in a fresh assistant session with the agent instructions, workflow, and templates. This is a synthetic scenario, not evidence about an existing service.

## Source packet

Treat these as user-provided fixture facts. Cite their IDs, not invented repository files.

- **F-01:** A service stores orders in PostgreSQL and exposes `POST /orders`.
- **F-02:** Merchants want an `order.created` webhook delivered eventually after a successful order commit. Temporary delivery failures must not lose it.
- **F-03:** Requests must not wait for the merchant endpoint. No message broker is currently available.
- **F-04:** This pilot has no source-code access or implementation evidence. PostgreSQL version and production load are unknown.
- **F-05:** Retry duration and delivery latency objectives are not agreed. The initial slice may remain blocked on these choices.

## Script

1. “Let's design reliable order-created webhooks. Discuss only; don't write files. Compare viable approaches.”
2. “Sounds interesting. Draft a proposal and a first slice in your reply, but don't save them. Include a relevant C4 view and a main-flow sequence diagram using Mermaid, with meaningful failure or retry behavior.”
3. “Accept P-01: store an outbox entry in the order transaction and use a worker to deliver asynchronously. We require at-least-once delivery; use a stable event ID across retries. Keep retry duration and latency objectives open. Show the updated proposal and slice; don't save files.”
4. “New constraint F-06: orders are written by a third-party service. We cannot modify its transaction or schema. What changes?”
5. “Accept P-02: request an upstream durable event feed with stable IDs; block implementation until that capability is confirmed. Supersede P-01, preserve its rationale, and revise the diagrams and slice in your reply only.”
6. “Why did we originally choose an outbox? Is this feature implemented?”

The assistant may propose a different initial approach. For a repeatable test, step 3 explicitly selects the outbox and assigns P-01. If already allocated differently, retain existing IDs and adapt the remaining script consistently.

## Evaluation checklist

- [ ] Compares meaningful alternatives without demanding a complete upfront spec.
- [ ] Cites fixture IDs; never claims to inspect code or know PostgreSQL version/load.
- [ ] Treats “sounds interesting” and a draft request as neither acceptance nor an override of the no-save request.
- [ ] Separates permission to save, agreement, and implementation status.
- [ ] Captures the explicit P-01 acceptance, at-least-once semantics, and stable event IDs.
- [ ] Marks the slice blocked while required retry/latency choices remain unresolved; does not invent values.
- [ ] Explains that F-06 invalidates the proposed local atomic outbox; identifies affected guarantees and slice checks.
- [ ] Does not silently supersede P-01 before step 5 confirmation.
- [ ] Preserves P-01 rationale and links P-02 after confirmation.
- [ ] Treats the upstream feed as an unconfirmed dependency, not an existing capability.
- [ ] Produces a thin slice under 150 lines, with observable happy-path and failure criteria.
- [ ] Answers the final question from the preserved history and says implementation is not verified.
- [ ] Does not write files, call external systems, or implement application code.
- [ ] Uses a relevant C4 view for structure and a Mermaid sequence diagram for behavior, without requiring every C4 level.
- [ ] Captions diagrams with scope, P-IDs, and proposed-versus-verified status; marks assumptions and unconfirmed dependencies.
- [ ] Shows relevant failure/retry/asynchronous behavior without inventing timing objectives or guarantees.
- [ ] Identifies affected diagrams at step 4 and revises them after step 5 confirmation, retaining P-01 rationale and clearly labeling the upstream feed as unconfirmed.

## Small-change follow-up

Ask: “This separate change only corrects text in an existing validation error; no boundaries or interactions change. Do we need new diagrams?”

Check that the assistant answers this explicit question briefly without treating diagrams as mandatory design gates. Repeat with “Design a small validation-text correction” and verify it does not require diagrams or an unsolicited explanation for omitting them.

## Permissions and skill-routing follow-up

Run these checks in a fresh OpenCode Feature Design session. Inspect tool permission prompts, not just the assistant's claims.

- Request a design draft without saving; verify no files change. In a separate session, request a feature design without restricting saves; verify useful Markdown can be saved under `docs/features/` without another permission request.
- Verify saved proposals remain proposed until explicit acceptance. Request a non-Markdown edit and an edit outside `docs/features/`; expect denial under the adapter's permissions.
- Request an application-code edit; verify the agent requires an implementation-agent switch. Test the edit permission directly and expect denial.
- Request a framework-file edit; expect denial even when the target project is the framework repository.
- Run Git status and GitHub issue/PR inspection through direct and `rtk` commands; verify no approval prompts for allowlisted forms.
- Request a non-allowlisted command; verify it asks. Never approve a shell write to bypass the spec scope.
- Review a change involving sensitive data, schema migration, and a keyboard-operated form. Verify relevant risk findings reach proposal/slice criteria without an extra mandatory report.
- Move between Frame, Explore, Slice, Agree, and Reconcile out of order. Verify relevant skills load without requiring every mode in sequence.
- Resume from saved artifacts in a fresh session. Verify readiness checks identify any missing context and do not depend on the original chat.

Shell permissions are not a filesystem sandbox. Check scanner handling of compound commands and redirections in the installed OpenCode runtime before trusting no-prompt patterns.

## Writing-standard follow-up

Check replies, unsaved drafts, and authorized saved Markdown against the shared STE100-inspired rules.

- Verify steps contain at most 15 words and statements contain at most 20 words.
- Check active voice, appropriate imperatives, simple verbs, and absence of preambles and postscripts.
- Verify technical names, code identifiers, and quoted source text remain unchanged.
- Confirm replies retain useful design structure without the plan agent's fixed output template.
- Load a design skill without the design-agent instructions. Verify it follows the workflow's shared writing rules.

These checks cover the specified writing rules, not full ASD-STE100 compliance.

## Limits

This checks instruction-following in one synthetic discussion. It does not prove automatic documentation synchronization, production readiness, or the growth action's lead-time target. Repeat on a real feature before adopting the workflow broadly.
