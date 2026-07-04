from enum import Enum


class ArchitectureDocumentStatus(str, Enum):
    """Lifecycle status values for architecture documents."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"
