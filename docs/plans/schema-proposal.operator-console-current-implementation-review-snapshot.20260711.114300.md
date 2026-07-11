```json
{
  "title": "Operator Console current implementation review snapshot schema proposal",
  "artifact_type": "schema-proposal",
  "status": "candidate-0-athena-promoted-from-koios-input",
  "datetime": "20260711.114300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_input": "KOIOS concrete schema/provenance-shape input via intercom",
  "scope": "candidate fixture/read-model shape for Operator Console current implementation review and orientation surface",
  "authority": "proposal only; not docs/schemas authority"
}
```

# Schema proposal 20260711.114300: Operator Console current implementation review snapshot

## Status

Candidate-0 proposal promoted by ATHENA from KOIOS provenance-shape input.

This document is not a `docs/schemas/` authority file. It is candidate architecture/brief input for a bounded follow-up such as `operator-console-review-orientation-copy-fixture`.

## Candidate record

`CurrentImplementationReviewSnapshot`

Purpose: one static UI/read-model snapshot that orients a user to the accepted implementation bundle and cites evidence. It is not live status and not product authority.

## TypeScript shape

```ts
interface CurrentImplementationReviewSnapshot {
  recordType: "current-implementation-review-snapshot";
  recordShapeVersion: "candidate-0";
  snapshotId: string;
  title: string;
  generatedAt: string;
  sourceHashObservedAt: string;
  status: ReviewSnapshotStatus;
  authorityBoundary: AuthorityBoundary;
  orientation: OrientationBlock;
  bundleItems: ImplementationBundleItem[];
  workflowObjectSummary: WorkflowObjectSummaryRef;
  nonAuthorityMarkers: NonAuthorityMarker[];
  staleness: StalenessBlock;
  provenanceRefs: ProvenanceRef[];
}

interface OrientationBlock {
  whatThisIs: string;
  whyItExists: string;
  howToReadIt: string;
  whatItIsNot: string;
  whatToDoNext: string;
}

interface ImplementationBundleItem {
  itemId: string;
  sliceName: string;
  displayName: string;
  status: BundleItemStatus;
  statusSource: StatusSource;
  fixtureDerivedStatus: true;
  ownerDomain: OwnerDomain;
  implementationReportRef: string;
  acceptanceReviewRef: string;
  validationSourceRef: string;
  evidenceRefs: string[];
  validationSummary: string;
  authorityBoundary: ItemAuthorityBoundary;
  sourceHashLabel: HashLabel;
  snapshotGeneratedAt: string;
}

interface WorkflowObjectSummaryRef {
  recordId: string;
  status: "accepted-static-projection";
  recordLocator: string;
  packageSourceRef: string;
  artifactRecordCount: number;
  gateEvaluationCount: number;
  validationEvidenceCount: number;
  previewEvidenceCount: number;
  nonAuthorityMarkers: NonAuthorityMarker[];
  hashCaveat: string;
  refreshProtocolStatement: string;
  staleHashPackagingRule: string;
}

interface ProvenanceRef {
  refId: string;
  locator: string;
  artifactType: ArtifactType;
  ownerRole: OwnerRole;
  ownerDomain: OwnerDomain;
  contentHash?: string;
  hashKind?: "sha256" | "working-tree-sha256" | "not-recorded";
  hashObservedAt?: string;
  authorityBoundary: RefAuthorityBoundary;
}

interface StalenessBlock {
  mode: "static-snapshot";
  freshness: "stale-by-design";
  refreshProtocol: "not-defined" | "manual-validator-rerun-required";
  hashMeaning: "working-tree-content-hash-not-commit-id";
  ifSourceChanges: "rerun-workflow-object-validator-or-record-intentional-staleness";
}
```

## Orientation semantics

The rendered orientation block should plainly state:

1. **What this is**: a static snapshot of accepted bootstrap Operator Console implementation evidence.
2. **Why it exists**: it helps a human inspect which slices are accepted and what evidence supports them.
3. **How to read it**: each card is one accepted slice; paths are evidence sources; workflow-object counts summarize one static projection record.
4. **What it is not**: not live status, not product acceptance, not a control surface, not complete history.
5. **What to do next**: use it to decide whether the review surface is understandable and whether follow-up evidence orientation is needed.

## Controlled values

```ts
type ReviewSnapshotStatus = "accepted-static-snapshot";
type BundleItemStatus = "accepted-static-snapshot";
type StatusSource =
  | "copied-from-implementation-report"
  | "copied-from-architecture-review"
  | "copied-from-hermes-user-acceptance";
type OwnerRole = "ATHENA" | "VULCAN" | "KOIOS" | "HERMES" | "USER" | "MIXED";
type OwnerDomain = "architecture" | "implementation" | "review" | "provenance" | "orchestration" | "source";
type ArtifactType =
  | "architecture-note"
  | "implementation-report"
  | "architecture-review"
  | "implementation-review"
  | "workflow-object-record"
  | "test-validator"
  | "package-manifest"
  | "aar";
type AuthorityBoundary = "fixture-read-model-only";
type ItemAuthorityBoundary =
  | "static-snapshot-fixture-only-not-live-not-product-authority"
  | "projection-index-only-not-schema-authority";
type RefAuthorityBoundary =
  | "source-authority"
  | "evidence-authority"
  | "provenance-only"
  | "projection-index-only"
  | "test-only-validator";
type HashLabel = "working-tree-content-hash-not-commit-id" | "fixture-generation-source-snapshot";
type NonAuthorityMarker =
  | "static-snapshot"
  | "fixture-only"
  | "not-live"
  | "stale-by-design"
  | "not-product-authority"
  | "not-source-authority"
  | "not-completion-authority"
  | "not-schema-authority"
  | "not-storage-authority"
  | "projection-index-only";
```

## Validation requirements

Minimum validator/test checks:

1. Required top-level fields exist.
2. Orientation block has all five fields and rendered UI includes them.
3. Every bundle item has implementation report, acceptance/review, validation source, at least one evidence ref, `fixtureDerivedStatus: true`, and authority boundary.
4. No bundle status can be rendered without a visible status source.
5. Required non-authority markers include `static-snapshot`, `fixture-only`, `not-live`, `stale-by-design`, `not-product-authority`, and `not-completion-authority`.
6. Hash caveat includes working-tree hash and not-commit-id semantics.
7. Staleness block includes refresh protocol not defined and validator-rerun/intentional-staleness rule.
8. Workflow-object summary does not claim source/schema/storage/completion authority.
9. No live primitives or mutation controls are introduced.
10. If a workflow-object record hash is displayed, the static-record validator must pass or the snapshot must be explicitly marked intentionally stale.

## Minimal JSON example

```json
{
  "recordType": "current-implementation-review-snapshot",
  "recordShapeVersion": "candidate-0",
  "snapshotId": "current-implementation.operator-console.20260711.112245",
  "title": "Operator Console current implementation review",
  "generatedAt": "20260711.112245Z",
  "sourceHashObservedAt": "20260711.112245Z",
  "status": "accepted-static-snapshot",
  "authorityBoundary": "fixture-read-model-only",
  "orientation": {
    "whatThisIs": "A static snapshot of accepted bootstrap Operator Console implementation evidence.",
    "whyItExists": "It helps a human inspect which slices are accepted and what evidence supports them.",
    "howToReadIt": "Each card is one accepted slice; paths are evidence sources; workflow-object counts summarize one static projection record.",
    "whatItIsNot": "It is not live status, product acceptance, a mutation control surface, or complete project history.",
    "whatToDoNext": "Use this snapshot to decide whether the review surface is understandable and whether more evidence orientation is needed."
  },
  "bundleItems": [
    {
      "itemId": "implementation-review.operator-console-p2",
      "sliceName": "operator-console-readability-navigation-fixture",
      "displayName": "Operator Console P2 readability/navigation fixture",
      "status": "accepted-static-snapshot",
      "statusSource": "copied-from-architecture-review",
      "fixtureDerivedStatus": true,
      "ownerDomain": "implementation",
      "implementationReportRef": "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
      "acceptanceReviewRef": "docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md",
      "validationSourceRef": "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
      "evidenceRefs": [
        "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
        "docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md"
      ],
      "validationSummary": "Static copied summary from cited implementation/review artifacts.",
      "authorityBoundary": "static-snapshot-fixture-only-not-live-not-product-authority",
      "sourceHashLabel": "fixture-generation-source-snapshot",
      "snapshotGeneratedAt": "20260711.112245Z"
    }
  ],
  "workflowObjectSummary": {
    "recordId": "workflow-object.operator-console-bootstrap-bundle.20260711",
    "status": "accepted-static-projection",
    "recordLocator": "dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json",
    "packageSourceRef": "src/typescript/projectkoios/ui/operator-console/package.json",
    "artifactRecordCount": 9,
    "gateEvaluationCount": 3,
    "validationEvidenceCount": 1,
    "previewEvidenceCount": 1,
    "nonAuthorityMarkers": ["projection-index-only", "not-source-authority", "not-completion-authority", "not-schema-authority"],
    "hashCaveat": "Hashes are working-tree content hashes at fixture generation time, not commit IDs or source authority.",
    "refreshProtocolStatement": "Workflow-object refresh protocol is not yet defined.",
    "staleHashPackagingRule": "If referenced sources change, rerun the static-record validator or record intentional staleness."
  },
  "nonAuthorityMarkers": ["static-snapshot", "fixture-only", "not-live", "stale-by-design", "not-product-authority", "not-completion-authority"],
  "staleness": {
    "mode": "static-snapshot",
    "freshness": "stale-by-design",
    "refreshProtocol": "not-defined",
    "hashMeaning": "working-tree-content-hash-not-commit-id",
    "ifSourceChanges": "rerun-workflow-object-validator-or-record-intentional-staleness"
  },
  "provenanceRefs": [
    {
      "refId": "workflow-object-record",
      "locator": "dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json",
      "artifactType": "workflow-object-record",
      "ownerRole": "VULCAN",
      "ownerDomain": "provenance",
      "hashKind": "working-tree-sha256",
      "hashObservedAt": "20260711.112245Z",
      "authorityBoundary": "projection-index-only"
    }
  ]
}
```
