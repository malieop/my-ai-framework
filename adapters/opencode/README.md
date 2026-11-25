# OpenCode V2 integration

This repository owns the OpenCode adapters, permissions, commands, skills, and workflows.
Global agents and commands are symlinks, not copied definitions. Skills use one stable source-directory registration through the framework link.
Portable role instructions remain in the root `agents/` directory.

## Install once

Run from the framework repository:

```sh
rtk python3 -B scripts/install_opencode.py --dry-run
rtk python3 -B scripts/install_opencode.py
```

The installer uses `~/.config/opencode`, or `$XDG_CONFIG_HOME/opencode` when set.
It preserves unrelated agents, commands, skills, and JSON configuration.
Register the linked skill source once in global `opencode.jsonc`, preserving your other settings:

```jsonc
{
  "skills": ["~/.config/opencode/frameworks/my-ai-framework/skills"]
}
```

For an XDG configuration directory, use its absolute `frameworks/my-ai-framework/skills` path instead.
This is only a directory reference; skill contents and future skill additions remain repository-owned.
The installer intentionally does not rewrite your JSONC. The linked source registration preserves each skill's supporting-file paths.
Conflicting entries stop installation before writes. Use `--replace` only when replacing those entries is intended:

```sh
rtk python3 -B scripts/install_opencode.py --replace
```

Replaced entries move to timestamped `framework-backups/` directories outside OpenCode's discovery directories.
Restore a backup by removing its replacement symlink and moving the backup to its original location.
Use `--config-dir` for isolated installation tests; adapters must use that directory as their global configuration directory.

## Installed links

```text
<global-config-dir>/
├── frameworks/my-ai-framework -> <repository>/
├── agents/feature-design.md -> <repository>/adapters/opencode/agents/feature-design.md
├── agents/feature-implementor.md -> <repository>/adapters/opencode/agents/feature-implementor.md
├── commands/feature-design.md -> <repository>/adapters/opencode/commands/feature-design.md
└── commands/feature-implementation.md -> <repository>/adapters/opencode/commands/feature-implementation.md
```

Choose `feature-design` or `feature-implementor` from OpenCode's agent selector.
Alternatively, run `/feature-design <problem>` or `/feature-implementation <saved-slice-path>`.
Commands select their corresponding agents in the current session. Neither command authorizes implementation or file writes.
Agents read the portable role instructions, which link to their workflows. Workflow Markdown is not a separate OpenCode registry.

## Updates and verification

Edit framework files here, not through global links. Existing links read the updated repository files.
Use `/reload` after changes if OpenCode does not refresh linked files automatically; symlink-target watching can vary.
Rerun installation to link newly added agents or commands. Existing correct links remain unchanged.
Obsolete agent and command links targeting this checkout are removed; unrelated entries remain untouched.
The registered skill source passes through the framework link, preserving relative workflow and template paths.
OpenCode discovers new skills beneath it without additional links or JSON edits.
If the checkout moves, rerun with `--replace` to repair links. Do not delete the checkout while using this integration.

Verify discovery with:

```sh
rtk opencode reload
rtk opencode debug agents
rtk opencode api get "/api/command?location[directory]=$PWD"
rtk opencode api get "/api/skill?location[directory]=$PWD"
```

Replace any old checkout-specific skill source with the stable linked path once; routine framework updates need no global edits.

Run the isolated discovery test without using your personal configuration:

```sh
RUN_OPENCODE_RUNTIME_TESTS=1 rtk python3 -B -m unittest discover -s tests -v
```

It starts a temporary authenticated local server, verifies agents, commands, skills, and relative workflow paths, then removes it.
Structural and discovery tests do not prove conversational authorization behavior; run the design and implementation pilots separately.

## Permission boundaries

Design permits only target-project Markdown specs under `docs/features/`; implementation edits ask for tool approval.
Implementation starts read-only and requires explicit conversational execution authorization, independently of tool prompts.
Both roles prohibit framework maintenance and unauthorized external changes.
The framework edit-denial glob covers paths containing `my-ai-framework`, including the installed framework alias.
Keep that checkout directory name for canonical-path coverage. A renamed checkout needs separately reviewed permission rules.
The repository's [project configuration](../../.opencode/opencode.jsonc) denies all edits for these roles inside the framework itself.
This also covers location-relative resources that cannot match the global absolute-path denial glob.
Build remains available for framework maintenance. Do not copy this project-only guard into unrelated target projects.
Shell allowlists are not a sandbox. Verify actual prompts and path handling before relying on permission coverage.
Do not grant shell writes to bypass design restrictions. Use Build for framework maintenance.
