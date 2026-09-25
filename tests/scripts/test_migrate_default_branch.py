from __future__ import annotations

import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Any

_REPOSITORY = Path(__file__).parents[2]
_SCRIPT = _REPOSITORY / "scripts/migrate-default-branch"
_EXPECTED_COMMIT = "a" * 40
_GITHUB_REPOSITORY = "test-owner/test-repository"
_SOURCE_BRANCH = "master"
_TARGET_BRANCH = "main"

_FAKE_COMMAND = r"""#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

state_path = Path(os.environ["MIGRATION_TEST_STATE"])
state: dict[str, Any] = json.loads(state_path.read_text(encoding="utf-8"))
program = Path(sys.argv[0]).name
arguments = sys.argv[1:]
original_arguments = arguments.copy()


def save() -> None:
    state_path.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")


def fail(message: str = "") -> None:
    if message:
        print(message, file=sys.stderr)
    raise SystemExit(1)


def emit_ref(branch: str) -> None:
    if branch == state["source"]:
        print(f"{state['expected']}\trefs/heads/{branch}")
    elif branch == state["target"] and state["target_remote"]:
        print(f"{state['expected']}\trefs/heads/{branch}")


if program == "gh":
    if arguments[:2] == ["repo", "view"]:
        fields = arguments[arguments.index("--json") + 1].split(",")
        payload = {}
        if "nameWithOwner" in fields:
            payload["nameWithOwner"] = state["github_repo"]
        if "defaultBranchRef" in fields:
            payload["defaultBranchRef"] = {"name": state["default"]}
        print(json.dumps(payload))
        raise SystemExit(0)
    if arguments[:2] == ["repo", "edit"]:
        index = arguments.index("--default-branch")
        state["default"] = arguments[index + 1]
        save()
        raise SystemExit(0)
    if arguments[:2] == ["pr", "list"]:
        print('[{"number": 1}]' if state["open_pr"] else "[]")
        raise SystemExit(0)
    fail(f"unsupported gh command: {arguments!r}")

while arguments[:1] in (["-c"], ["-C"]):
    arguments = arguments[2:]
if not arguments:
    fail("missing git command")
command, *rest = arguments

if command == "check-ref-format":
    raise SystemExit(0)
if command == "rev-parse":
    if rest == ["--path-format=absolute", "--git-path", "hooks/pre-push"]:
        print(f"{state['repo_path']}/.git/hooks/pre-push")
        raise SystemExit(0)
    if rest == ["--show-toplevel"]:
        print(state["repo_path"])
        raise SystemExit(0)
    reference = rest[-1]
    if reference in {"HEAD", f"refs/heads/{state['source']}",
                     f"refs/remotes/{state['remote']}/{state['source']}",
                     state["expected"] + "^{commit}"}:
        print(state["expected"])
        raise SystemExit(0)
    if reference == f"refs/heads/{state['target']}" and state["target_local"]:
        print(state["expected"])
        raise SystemExit(0)
    if (reference == f"refs/remotes/{state['remote']}/{state['target']}"
            and state["target_tracking"]):
        print(state["expected"])
        raise SystemExit(0)
    fail()
if command == "remote" and rest[:1] == ["get-url"]:
    print(f"https://github.com/{state['github_repo']}.git")
    raise SystemExit(0)
if command == "status":
    if "--short" in rest and "--branch" in rest:
        print(f"## {state['source']}...{state['remote']}/{state['source']}")
    elif state["dirty"]:
        print(" M tracked-file")
    raise SystemExit(0)
if command == "ls-files":
    if "-v" in rest and "-z" in rest:
        tag = state["index_tag"]
        sys.stdout.buffer.write(f"{tag} tracked-file\0".encode())
    else:
        print("tracked-file")
    raise SystemExit(0)
if command == "worktree" and rest == ["list", "--porcelain", "-z"]:
    records = [
        (
            f"worktree {state['repo_path']}\0"
            f"HEAD {state['expected']}\0"
            f"branch refs/heads/{state['source']}\0\0"
        )
    ]
    for number in range(1, state["extra_worktrees"] + 1):
        records.append(
            f"worktree /test/extra-{number}\0"
            f"HEAD {state['expected']}\0"
            f"branch refs/heads/extra-{number}\0\0"
        )
    sys.stdout.buffer.write("".join(records).encode())
    raise SystemExit(0)
if command == "symbolic-ref" and rest == ["-q", "HEAD"]:
    print(f"refs/heads/{state['source']}")
    raise SystemExit(0)
if command == "ls-remote":
    if "--symref" in rest:
        print(f"ref: refs/heads/{state['default']}\tHEAD")
        print(f"{state['expected']}\tHEAD")
        raise SystemExit(0)
    references = [value for value in rest if value.startswith("refs/heads/")]
    for reference in references:
        emit_ref(reference.removeprefix("refs/heads/"))
    raise SystemExit(0)
if command == "show-ref":
    reference = rest[-1]
    exists = (
        reference == f"refs/heads/{state['target']}" and state["target_local"]
    ) or (
        reference == f"refs/remotes/{state['remote']}/{state['target']}"
        and state["target_tracking"]
    )
    raise SystemExit(0 if exists else 1)
if command == "cat-file":
    raise SystemExit(0)
if command == "branch":
    state["target_local"] = True
    save()
    raise SystemExit(0)
if command == "push":
    required = {
        "push.followTags=false",
        "push.pushOption=",
    }
    if not required.issubset(original_arguments):
        fail("missing bounded push configuration")
    if "--no-verify" not in rest or "--recurse-submodules=no" not in rest:
        fail("missing bounded push flags")
    state["target_remote"] = True
    state["target_tracking"] = True
    save()
    print("push accepted")
    raise SystemExit(0)
fail(f"unsupported git command: {command} {rest!r}")
"""


class MigrateDefaultBranchScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name).resolve()
        self.repository = self.root / "repository"
        self.repository.mkdir()
        self.binary_directory = self.root / "bin"
        self.binary_directory.mkdir()
        self.state_path = self.root / "state.json"
        command = self.binary_directory / "command.py"
        command.write_text(textwrap.dedent(_FAKE_COMMAND), encoding="utf-8")
        command.chmod(0o755)
        (self.binary_directory / "git").symlink_to(command)
        (self.binary_directory / "gh").symlink_to(command)
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "MIGRATION_TEST_STATE": str(self.state_path),
                "PATH": (
                    f"{self.binary_directory}{os.pathsep}"
                    f"{self.environment['PATH']}"
                ),
            }
        )
        self.write_state()

    def write_state(self, **overrides: Any) -> None:
        state: dict[str, Any] = {
            "default": _SOURCE_BRANCH,
            "dirty": False,
            "expected": _EXPECTED_COMMIT,
            "extra_worktrees": 0,
            "github_repo": _GITHUB_REPOSITORY,
            "index_tag": "H",
            "open_pr": False,
            "remote": "origin",
            "repo_path": str(self.repository),
            "source": _SOURCE_BRANCH,
            "target": _TARGET_BRANCH,
            "target_local": False,
            "target_remote": False,
            "target_tracking": False,
        }
        state.update(overrides)
        self.state_path.write_text(
            json.dumps(state, sort_keys=True),
            encoding="utf-8",
        )

    def read_state(self) -> dict[str, Any]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def run_script(
        self,
        *extra_arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(_SCRIPT),
                "--repo-path",
                str(self.repository),
                "--github-repo",
                _GITHUB_REPOSITORY,
                "--remote",
                "origin",
                "--source",
                _SOURCE_BRANCH,
                "--target",
                _TARGET_BRANCH,
                "--expected-commit",
                _EXPECTED_COMMIT,
                *extra_arguments,
            ],
            capture_output=True,
            check=False,
            env=self.environment,
            text=True,
            timeout=10,
        )

    def test_dry_run_exercises_absent_target_without_mutation(self) -> None:
        result = self.run_script()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY RUN ONLY", result.stdout)
        state = self.read_state()
        self.assertFalse(state["target_local"])
        self.assertFalse(state["target_remote"])
        self.assertEqual(state["default"], _SOURCE_BRANCH)

    def test_apply_creates_target_and_changes_only_default(self) -> None:
        result = self.run_script("--apply")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SUCCESS", result.stdout)
        state = self.read_state()
        self.assertTrue(state["target_local"])
        self.assertTrue(state["target_remote"])
        self.assertTrue(state["target_tracking"])
        self.assertEqual(state["default"], _TARGET_BRANCH)

    def test_dirty_checkout_stops_before_mutation(self) -> None:
        self.write_state(dirty=True)

        result = self.run_script("--apply")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checkout is dirty", result.stderr)
        self.assertFalse(self.read_state()["target_local"])

    def test_multiple_worktrees_stop_before_mutation(self) -> None:
        self.write_state(extra_worktrees=1)

        result = self.run_script("--apply")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected exactly one registered worktree", result.stderr)
        self.assertFalse(self.read_state()["target_local"])

    def test_executable_pre_push_hook_stops_before_mutation(self) -> None:
        hook = self.repository / ".git" / "hooks" / "pre-push"
        hook.parent.mkdir(parents=True)
        hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        hook.chmod(0o755)

        result = self.run_script("--apply")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("executable pre-push hook", result.stderr)
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertFalse(state["target_local"])
        self.assertFalse(state["target_remote"])

    def test_hidden_index_flag_stops_before_mutation(self) -> None:
        self.write_state(index_tag="S")

        result = self.run_script("--apply")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skip-worktree or assume-unchanged", result.stderr)
        self.assertFalse(self.read_state()["target_local"])


if __name__ == "__main__":
    unittest.main()
