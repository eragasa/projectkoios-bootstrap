from enum import Enum


class ArchitectureDocumentStatus(str, Enum):
    draft = "draft"
    active = "active"
    archived = "archived"
    superseded = "superseded"
