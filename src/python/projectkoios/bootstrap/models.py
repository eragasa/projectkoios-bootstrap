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


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
GLOBAL_DIR = REPO_ROOT / "agents" / "global"
