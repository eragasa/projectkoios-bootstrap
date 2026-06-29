from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Harness:
    name: str
    display_name: str
    role: str
    config_dir: Path


HARNESSES: list[Harness] = [
    Harness("pi", "pi", "Agent runtime — executes Archon workflows", Path.home() / ".pi"),
    Harness("archon", "Athena", "Architecture design, ADRs, planning", Path.home() / ".archon"),
    Harness("opencode", "Vulcan", "Code writing, tests, validation", Path.home() / ".opencode"),
    Harness("goose", "Koios", "Knowledge management, vault ops", Path.home() / ".local/share/goose"),
]


GLOBAL_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "agents" / "global"
REPO_ROOT = GLOBAL_DIR.parent
