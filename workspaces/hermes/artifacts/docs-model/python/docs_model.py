from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class DocKind(str, Enum):
    collection = "collection"
    architecture = "architecture"
    adr = "adr"
    spec = "spec"
    brief = "brief"
    workflow = "workflow"
    runbook = "runbook"
    policy = "policy"
    role = "role"
    decision = "decision"
    handoff = "handoff"
    archive = "archive"
    aar = "aar"
    note = "note"


class Lifecycle(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    archived = "archived"
    superseded = "superseded"


class Authority(str, Enum):
    normative = "normative"
    advisory = "advisory"
    historical = "historical"


@dataclass(slots=True)
class DocNode:
    name: str
    path: str
    kind: DocKind
    lifecycle: Lifecycle
    authority: Authority
    children: List[DocNode] = field(default_factory=list)
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
