from enum import Enum


class ArchitectureDocumentStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    archived = "archived"
    superseded = "superseded"
