# Prototype validation results

## Scope

Ran the structural suite and delegated a read-only simulation of the six-turn [behavioral pilot](feature-design-pilot.md) to a fresh assistant context. The assistant read the actual workflow, agent instructions, templates, and source packet.

This is a synthetic simulation, not six independently submitted interactive turns or a production-feature trial. The assistant saw the complete scenario, including its checklist. Results therefore show an initial smoke test, not robust behavioral evaluation.

## Structural checks

Command: `python3 -m unittest discover -s tests -v`

Result: **5 tests passed**.

Checks covered nonempty required documents, local document link targets, slice-template length, proposal traceability sections, and absence of a separate decision-ledger template. They do not validate agreement semantics or architectural correctness.

## Observed simulated behavior

| Turn | Observed output | Review |
| --- | --- | --- |
| 1: Explore | Compared transactional outbox, change capture, and polling; cited F-01–F-04 and identified unknown transaction control. | Met the scenario expectation. |
| 2: Draft | Stated “Sounds interesting does not accept the design.” Produced an unsaved proposal with P-01 proposed and a blocked first slice. | Kept drafting, acceptance, and saving separate. |
| 3: Accept | Marked P-01 accepted with at-least-once semantics and stable retry IDs. Left retry/latency and transaction-control questions blocking. | Recorded only explicit choices; invented no objective values. |
| 4: New constraint | Explained why F-06 invalidates local atomic recording; proposed P-02 without superseding P-01 yet. Identified affected guarantees and slice checks. | Preserved accepted history pending confirmation. |
| 5: Supersede | Marked P-01 superseded with its original rationale retained; linked P-02 and appended history. Revised the slice around an unconfirmed upstream feed. | Did not portray the feed as an existing capability. |
| 6: Retrieve | Explained the original outbox rationale and why it changed. Said implementation was not verified and no artifacts had been saved. | Distinguished design approval from implementation evidence. |

All displayed slices were under 60 lines, including observable delivery, failure, restart, and identity checks. The simulated partner used no write tools or external systems. The test runner, separately, created these framework files and this results report.

The simulated assistant self-assessed all 13 checklist items as passing. Inspection of its returned replies found no contradictory outcome on those items. This is not an independent blinded score.

## Follow-up validation

### Diagram-guidance update

After adding C4 Model and sequence-diagram guidance, the structural suite passed **7 tests**. The updated checks cover diagram sections, instruction coverage, and pilot coverage for diagram revisions and small-change exceptions.

The earlier six-turn simulation predates these diagram requirements. The expanded behavioral pilot has not been rerun, and Mermaid syntax/rendering has not been validated. Its diagram checklist remains pending.

1. Run a real feature discussion with the user, one turn at a time.
2. Confirm which unanswered questions genuinely block the next slice; avoid excessive design gates.
3. Test authorized file writes, reopening artifacts in a new session, and actual implementation-drift evidence.
4. Try ambiguous acceptance, missing sources, and conflicting documentation separately.
5. Measure slice size and delivery lead time on real work before claiming Growth Action 1 success.
