from enum import Enum


class ArchitectureDocumentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"
