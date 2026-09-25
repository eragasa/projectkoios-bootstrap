from __future__ import annotations

import os
import shutil
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SESSION_NAME = "projectkoios-coordinator"
STARTUP_PROMPT = """\
Start as the main coordination session for Project Koios software development
across repositories.

Before proposing or assigning work:
1. Read AGENTS.md and maps/repositories.md.
2. Use pi-intercom to list the live Pi sessions.
3. Verify that HERDR_ENV=1.
4. Summarize repository-session availability and ask for the operator's
   objective if none has been provided.

For each objective, classify it as bootstrap-local work, owner-repository work,
or multi-repository coordination. Route product changes to the owning
repository. For multi-repository execution, use one visible Herdr-hosted Pi
session and one writer per active repository. Give every assignment a
repository, objective, constraints, expected output, validation, and stop
conditions. Treat session reports as evidence and verify repository state
before reporting completion.

Before reporting completion, resolve every deferred finding by fixing it,
attaching it to an existing owner issue, requesting authority to create a
justified owner issue, or explicitly closing it untracked. A justified issue
must state the owner repository, evidence, consequence, current default,
revisit trigger, and closure condition. Do not create a local deferred-decision
list or persist runtime task state.

For repeatable operational sequences, prioritize an executable deterministic
script over a pasted command transcript. At closeout, require the owner session
to send the script to this coordinator with its explicit inputs, safety and
stop behavior, validation evidence, and reuse limits. Keep repository-specific
scripts with their owner; assess reusable scripts here before reuse. Scripts
must not embed credentials, machine-specific defaults, or hidden runtime state.

Do not open panes, delegate work, modify files, or create issues without
operator authority."""

_REQUIRED_REPOSITORY_FILES = (Path("AGENTS.md"), Path("maps/repositories.md"))


class CoordinatorStartupError(RuntimeError):
    """A bounded coordinator preflight failure."""

    def __init__(self, message: str, *, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class CoordinatorLaunch:
    """A validated, side-effect-free plan for replacing this process with Pi."""

    repository_root: Path
    executable: str
    argv: tuple[str, ...]


def plan_coordinator_startup(
    repository_root: str | Path,
    pi_arguments: Sequence[str] = (),
    *,
    environ: Mapping[str, str] | None = None,
    find_executable: Callable[[str], str | None] = shutil.which,
) -> CoordinatorLaunch:
    """Validate startup boundaries and return the exact Pi invocation."""
    environment = os.environ if environ is None else environ
    if environment.get("HERDR_ENV") != "1":
        raise CoordinatorStartupError(
            "the multi-repository coordinator must run in a Herdr-managed "
            "pane.\n\nStart or attach to Herdr from this repository, then "
            "run this launcher inside that pane. A Pi process started "
            "outside Herdr cannot acquire pane context later."
        )

    if "--" in pi_arguments:
        raise CoordinatorStartupError(
            "do not pass the Pi option terminator '--'; the coordinator "
            "launcher supplies it after its fixed options"
        )

    root = Path(repository_root).resolve()
    missing = [
        path.as_posix()
        for path in _REQUIRED_REPOSITORY_FILES
        if not (root / path).is_file()
    ]
    if missing:
        raise CoordinatorStartupError(
            "could not identify the projectkoios-bootstrap root; missing: "
            + ", ".join(missing)
        )

    executable = find_executable("pi")
    if executable is None:
        raise CoordinatorStartupError(
            "pi is not available on PATH.",
            exit_code=127,
        )
    executable = str(Path(executable).resolve())

    session_name = (
        environment.get("PROJECTKOIOS_COORDINATOR_NAME") or DEFAULT_SESSION_NAME
    )
    argv = (
        executable,
        *pi_arguments,
        "--name",
        session_name,
        "--",
        STARTUP_PROMPT,
    )
    return CoordinatorLaunch(
        repository_root=root,
        executable=executable,
        argv=argv,
    )


def execute_coordinator_startup(launch: CoordinatorLaunch) -> None:
    """Replace the current process with the validated Pi invocation."""
    os.chdir(launch.repository_root)
    os.execv(launch.executable, launch.argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | Path | None = None,
) -> int:
    """Run the coordinator launcher and return only after a preflight error."""
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    root = Path.cwd() if repository_root is None else Path(repository_root)
    try:
        launch = plan_coordinator_startup(root, arguments)
        execute_coordinator_startup(launch)
    except CoordinatorStartupError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
