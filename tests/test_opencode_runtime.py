"""Opt-in OpenCode V2 discovery test with an isolated, temporary local server."""

import contextlib
import io
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path
from urllib.parse import urlencode

from scripts.install_opencode import ROOT, install


@unittest.skipUnless(
    os.environ.get("RUN_OPENCODE_RUNTIME_TESTS") == "1" and shutil.which("opencode") and shutil.which("rtk"),
    "Set RUN_OPENCODE_RUNTIME_TESTS=1 with OpenCode V2 and RTK installed",
)
class OpenCodeRuntimeTests(unittest.TestCase):
    def test_linked_agents_commands_and_skills(self):
        with tempfile.TemporaryDirectory(prefix="framework-runtime-") as temporary:
            home = Path(temporary)
            config = home / "config/opencode"
            target = home / "target"
            target.mkdir()
            with contextlib.redirect_stdout(io.StringIO()):
                install(config)
            (config / "opencode.jsonc").write_text(json.dumps({
                "skills": [str(config / "frameworks/my-ai-framework/skills")],
            }))
            env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home / "config"),
                       XDG_DATA_HOME=str(home / "data"), XDG_STATE_HOME=str(home / "state"),
                       XDG_CACHE_HOME=str(home / "cache"), OPENCODE_PASSWORD=uuid.uuid4().hex)
            # Do not inherit alternate config/server overrides from the user's session.
            for key in list(env):
                if key.startswith("OPENCODE_CONFIG") or key in ("OPENCODE_DB", "OPENCODE_USERNAME"):
                    env.pop(key)
            server = subprocess.Popen(
                ["rtk", "proxy", "opencode", "serve", "--hostname", "127.0.0.1", "--port", "0"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                env=env, cwd=target, start_new_session=True,
            )
            try:
                url = None
                for line in server.stdout:
                    match = re.search(r"http://[^\s]+", line)
                    if match:
                        url = match.group(0)
                        break
                self.assertIsNotNone(url, "Server did not report its listening URL")

                def call(method, path):
                    result = subprocess.run(
                        ["rtk", "proxy", "opencode", "api", "--server", url, method, path],
                        capture_output=True, text=True, env=env, cwd=target, timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    return json.loads(result.stdout) if result.stdout.strip() else None

                query = urlencode({"location[directory]": str(target)})
                call("get", "/api/config?" + query)
                # First discovery can be asynchronous. Reload awaits replacement location builds.
                call("post", "/api/location/reload")
                agents = call("get", "/api/agent?" + query)["data"]
                selected = [a for a in agents if a["id"] in ("feature-design", "feature-implementor")]
                self.assertEqual(len(selected), 2)
                for agent in selected:
                    self.assertEqual(agent["mode"], "primary")
                    self.assertFalse(agent["hidden"])
                commands = call("get", "/api/command?" + query)["data"]
                self.assertTrue({"feature-design", "feature-implementation"} <= {c["name"] for c in commands})
                skills = call("get", "/api/skill?" + query)["data"]
                linked = [s for s in skills if "frameworks/my-ai-framework/skills/" in s["path"]]
                expected = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
                self.assertEqual({s["id"] for s in linked}, expected)
                for skill in linked:
                    self.assertTrue((Path(skill["path"]).parent / "../../workflows/feature-design.md").is_file())
                framework_query = urlencode({"location[directory]": str(ROOT)})
                framework_agents = call("get", "/api/agent?" + framework_query)["data"]
                for agent in framework_agents:
                    if agent["id"] in ("feature-design", "feature-implementor"):
                        edit_rules = [r for r in agent["permissions"] if r["action"] in ("*", "edit")]
                        self.assertEqual(edit_rules[-1], {"action": "edit", "resource": "*", "effect": "deny"})
            finally:
                if server.poll() is None:
                    os.killpg(server.pid, signal.SIGTERM)
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(server.pid, signal.SIGKILL)
                    server.wait()
                server.stdout.close()


if __name__ == "__main__":
    unittest.main()
