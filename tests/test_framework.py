"""Structural checks only; agent behavior requires the conversational pilot."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    "README.md",
    "agents/feature-design-partner.md",
    "agents/feature-implementor.md",
    "workflows/feature-design.md",
    "workflows/feature-implementation.md",
    "templates/implementation/plan.md",
    "skills/implementation-planning/SKILL.md",
    "templates/feature/overview.md",
    "templates/feature/proposal.md",
    "templates/feature/slice.md",
    "tests/feature-design-pilot.md",
    "tests/feature-design-pilot-results.md",
    "tests/feature-implementation-pilot.md",
    "adapters/opencode/README.md",
    "adapters/opencode/agents/feature-design.md",
    "adapters/opencode/agents/feature-implementor.md",
    "adapters/opencode/commands/feature-design.md",
    "adapters/opencode/commands/feature-implementation.md",
]
SKILLS = (
    "feature-design-frame",
    "feature-design-explore",
    "feature-design-agree",
    "feature-design-slice",
    "feature-design-reconcile",
    "design-risk-review",
)
DOCUMENTS += [f"skills/{skill}/SKILL.md" for skill in SKILLS]


class FrameworkTests(unittest.TestCase):
    def test_documents_exist_and_are_nonempty(self):
        for name in DOCUMENTS:
            with self.subTest(document=name):
                self.assertTrue((ROOT / name).read_text().strip())

    def test_local_document_links_resolve(self):
        # Template links describe future feature artifacts, not template files.
        for name in DOCUMENTS:
            if name.startswith("templates/"):
                continue
            document = ROOT / name
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                with self.subTest(document=name, target=target):
                    self.assertTrue((document.parent / path).exists())

    def test_slice_template_is_under_150_lines(self):
        template = ROOT / "templates/feature/slice.md"
        self.assertLess(len(template.read_text().splitlines()), 150)

    def test_proposal_has_traceability_sections(self):
        proposal = (ROOT / "templates/feature/proposal.md").read_text()
        for section in (
            "## Status",
            "## Proposed approach",
            "## C4 architecture",
            "## Sequence flows",
            "## Open questions and assumptions",
            "## Agreement and change history",
            "## Implementation evidence",
        ):
            with self.subTest(section=section):
                self.assertIn(section, proposal)

    def test_diagram_guidance_lives_in_explore_skill(self):
        # Instruction coverage only, not a Mermaid syntax/rendering check.
        text = (ROOT / "skills/feature-design-explore/SKILL.md").read_text()
        for term in (
            "C4 Model", "System Context", "Container", "Component",
            "sequence diagrams", "Mermaid", "unconfirmed dependencies",
            "Never require a diagram or an explanation for its omission",
        ):
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_skills_have_discovery_metadata_and_shared_rules_link(self):
        for skill in SKILLS:
            text = (ROOT / f"skills/{skill}/SKILL.md").read_text()
            with self.subTest(skill=skill):
                self.assertTrue(text.startswith("---\nname: "))
                self.assertIn("\ndescription: ", text)
                self.assertIn("../../workflows/feature-design.md#shared-agreement-and-persistence-rules", text)

    def test_workflow_routes_to_every_skill(self):
        workflow = (ROOT / "workflows/feature-design.md").read_text()
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"../skills/{skill}/SKILL.md", workflow)
        self.assertIn("not sequential approval gates or separate workers", workflow)
        self.assertIn("during exploration and before declaring slice readiness", workflow)

    def test_design_only_and_readiness_boundaries_remain(self):
        agent = (ROOT / "agents/feature-design-partner.md").read_text()
        workflow = (ROOT / "workflows/feature-design.md").read_text()
        self.assertIn("Stay strictly design-only", agent)
        self.assertIn("framework", agent)
        self.assertIn("read-only", agent)
        for term in (
            "Architectural acceptance and write authorization are separate",
            "Design ready, documentation pending",
            "Ready for handoff",
            "read the saved slice and relevant linked artifacts",
            "mark the old item superseded",
        ):
            with self.subTest(term=term):
                self.assertIn(term, workflow)

    def test_design_default_saves_and_writing_rules(self):
        agent = (ROOT / "agents/feature-design-partner.md").read_text()
        workflow = (ROOT / "workflows/feature-design.md").read_text()
        pilot = (ROOT / "tests/feature-design-pilot.md").read_text()
        self.assertIn("../workflows/feature-design.md#ste100-inspired-writing-rules", agent)
        for term in (
            "### STE100-inspired writing rules",
            "feature-design replies, drafts, and saved Markdown",
            "including direct skill use",
            "not full ASD-STE100 compliance",
            "15 words", "20 words", "active voice", "preambles and postscripts",
            "`use`, not `utilize`", "`show`, not `display`", "`start`, not `initiate`",
            "Keep technical names, code identifiers, and quoted source text unchanged",
            "Do not impose the plan agent's output template",
        ):
            with self.subTest(term=term):
                self.assertIn(term, workflow)
        self.assertIn("## Writing-standard follow-up", pilot)
        self.assertIn("without the design-agent instructions", pilot)
        self.assertIn("Markdown under the target project's `docs/features/`", workflow)
        self.assertIn("Respect a user's request not to save", workflow)
        self.assertIn("only explicit confirmation", workflow)
        self.assertIn("without another permission request", pilot)
        self.assertIn("non-Markdown edit", pilot)

    def test_risk_review_is_conditional_and_covers_relevant_concerns(self):
        text = (ROOT / "skills/design-risk-review/SKILL.md").read_text()
        for term in (
            "Authorization and sensitive data", "Compatibility and migrations",
            "Rollout and rollback", "Observability", "Accessibility",
            "Reliability and failure behavior", "blocking", "deferred",
            "Do not require empty sections", "observable acceptance criteria",
        ):
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_removed_role_switch_and_diagram_omission_requirements(self):
        for name in DOCUMENTS:
            if name.startswith("tests/"):
                continue
            text = (ROOT / name).read_text()
            with self.subTest(document=name):
                self.assertNotIn("explicitly confirm a role change", text)
                self.assertNotIn("explain why no new diagram is needed", text)
                self.assertNotIn("explain why no new view is needed", text)

    def test_pilot_covers_diagram_updates_and_small_change_exception(self):
        pilot = (ROOT / "tests/feature-design-pilot.md").read_text()
        for term in (
            "revise the diagrams and slice",
            "proposed-versus-verified",
            "## Small-change follow-up",
        ):
            with self.subTest(term=term):
                self.assertIn(term, pilot)

    def test_no_separate_decision_ledger_template(self):
        names = {path.name for path in (ROOT / "templates/feature").iterdir()}
        self.assertEqual(names, {"overview.md", "proposal.md", "slice.md"})

    def test_implementation_skill_metadata_and_routing(self):
        skill = (ROOT / "skills/implementation-planning/SKILL.md").read_text()
        workflow = (ROOT / "workflows/feature-implementation.md").read_text()
        self.assertTrue(skill.startswith("---\nname: Implementation Planning\n"))
        self.assertIn("\ndescription: ", skill)
        self.assertIn("../../workflows/feature-design.md#shared-agreement-and-persistence-rules", skill)
        self.assertIn("../skills/implementation-planning/SKILL.md", workflow)
        self.assertIn("Map each slice acceptance criterion", skill)
        self.assertIn("Planning ends without code changes", skill)

    def test_implementation_authorization_and_reconciliation_boundaries(self):
        agent = (ROOT / "agents/feature-implementor.md").read_text()
        workflow = (ROOT / "workflows/feature-implementation.md").read_text()
        for term in (
            "an accepted design slice and an approved implementation plan",
            "before execution authorization",
            "read-only during feature implementation",
            "Do not commit, push, publish, deploy",
        ):
            with self.subTest(term=term):
                self.assertIn(term, agent)
        for term in (
            "Plan approval is not execution authorization",
            "Permission to save does not approve the plan",
            "Do not supersede accepted decisions yourself",
            "Reconfirm material changes",
            "Do not mark a slice complete",
            "Never invent commits, PRs, or test results",
        ):
            with self.subTest(term=term):
                self.assertIn(term, workflow)

    def test_implementation_plan_preserves_traceability(self):
        plan = (ROOT / "templates/implementation/plan.md").read_text()
        for section in (
            "## Source and status", "## Code evidence and assumptions",
            "## Ordered steps", "## Acceptance verification",
            "## Blockers and deferred work", "## Execution evidence",
        ):
            with self.subTest(section=section):
                self.assertIn(section, plan)
        self.assertIn("Plan approval:", plan)
        self.assertIn("Execution authorization:", plan)

    def test_implementation_pilot_covers_behavioral_gaps(self):
        pilot = (ROOT / "tests/feature-implementation-pilot.md").read_text()
        for term in (
            "Approve the plan without authorizing execution",
            "Authorize saving only", "decision remains proposed",
            "conflicting with an accepted contract", "required check unavailable",
            "fresh session", "tiny slice",
        ):
            with self.subTest(term=term):
                self.assertIn(term, pilot)

    def test_opencode_entry_points_load_portable_roles(self):
        for agent, role in (
            ("feature-design", "feature-design-partner"),
            ("feature-implementor", "feature-implementor"),
        ):
            text = (ROOT / f"adapters/opencode/agents/{agent}.md").read_text()
            with self.subTest(agent=agent):
                self.assertTrue(text.startswith("---\ndescription: "))
                self.assertIn("\nmode: primary\npermissions:\n", text)
                self.assertIn(f"<framework-root>/agents/{role}.md", text)
                self.assertIn("follow its linked workflow", text)
                self.assertIn('action: edit, resource: "**/my-ai-framework/**", effect: deny', text)
                self.assertNotIn("/Users/", text)
        for command, agent in (
            ("feature-design", "feature-design"),
            ("feature-implementation", "feature-implementor"),
        ):
            text = (ROOT / f"adapters/opencode/commands/{command}.md").read_text()
            with self.subTest(command=command):
                self.assertIn(f"\nagent: {agent}\nsubagent: false\n", text)
                self.assertIn("$ARGUMENTS", text)
                self.assertNotIn("!`", text)

    def test_framework_project_denies_role_edits(self):
        config = json.loads((ROOT / ".opencode/opencode.jsonc").read_text())
        self.assertEqual(set(config["agents"]), {"feature-design", "feature-implementor"})
        for agent in config["agents"].values():
            self.assertEqual(agent["permissions"], [{"action": "edit", "resource": "*", "effect": "deny"}])


if __name__ == "__main__":
    unittest.main()
