from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Runtime:
    name: str
    config_dir: Path

    @property
    def skills_dir(self) -> Path:
        return GLOBAL_DIR / self.name / "skills"

    @property
    def runtime_skills_dir(self) -> Path:
        if self.name == "pi":
            return Path.home() / ".pi" / "agent" / "skills"
        if self.name == "opencode":
            return Path.home() / ".opencode" / "skills"
        return self.config_dir / "skills"


RUNTIMES: list[Runtime] = [
    Runtime("pi", Path.home() / ".pi"),
    Runtime("archon", Path.home() / ".archon"),
    Runtime("opencode", Path.home() / ".opencode"),
    Runtime("goose", Path.home() / ".local/share/goose"),
]


@dataclass(frozen=True)
class Role:
    name: str
    short_name: str
    responsibilities: str


ROLE_TO_RUNTIME: dict[str, str] = {
    "Hermes": "pi",
    "Athena": "archon",
    "Vulcan": "opencode",
    "Koios": "goose",
}


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
GLOBAL_DIR = REPO_ROOT / "agents" / "global"
