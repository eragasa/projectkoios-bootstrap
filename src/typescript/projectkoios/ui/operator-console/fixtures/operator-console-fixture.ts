import {
  AgentState,
  AuthorityBoundary,
  ContentKind,
  EvidenceKind,
  FixtureStatus,
  HashLabel,
  ProposalKind,
  SourceArtifactType,
  StatusClass,
  ValidationCategory,
  ValidationFindingLevel,
  ValidationStatus
} from "../src/contracts";
import type {
  AgentStatus,
  ChangeProposal,
  ContentRef,
  EvidenceRef,
  ExternalSystemStatus,
  FixtureMetadata,
  ValidationResult
} from "../src/contracts";

const fixtureTimestamp = "20260711.074650Z";

class FixtureMetadataFactory {
  build(
    fixtureId: string,
    fixtureStatus: FixtureStatus,
    sourceLocator: string,
    sourceArtifactType: SourceArtifactType,
    sourceHash: string,
    transformationNotes: string,
    trustExplanation: string
  ): FixtureMetadata {
    return {
      fixtureId,
      fixtureStatus,
      sourceLocator,
      sourceArtifactType,
      sourceHash,
      capturedAt: fixtureTimestamp,
      freshness: "stale-by-design fixture snapshot; not a live status check",
      authorityBoundary: [
        AuthorityBoundary.FixtureOnly,
        AuthorityBoundary.NonLive,
        AuthorityBoundary.NonProduction,
        AuthorityBoundary.NonAuthoritative
      ],
      provenanceSummary: "Bootstrap-derived deterministic fixture for the Operator Console P0 review flow.",
      transformationNotes,
      trustExplanation
    };
  }
}

const metadataFactory: FixtureMetadataFactory = new FixtureMetadataFactory();

export const currentAdrMarkdownRef: ContentRef = {
  id: "content.current.adr-json-schemas-draft",
  title: "Current source ADR-shaped Markdown",
  kind: ContentKind.SourceMarkdown,
  locator: "docs/adr/adr.json-schemas.draft.md",
  contentHash: "c95dfb0928ba1398eb058a7bb16b21f2dad77f4116169cbcc8075fb5186c2df5",
  hashLabel: HashLabel.FixtureSourceIdentityHash,
  metadata: metadataFactory.build(
    "fixture.current.adr-json-schemas-draft",
    FixtureStatus.TransformedFromBootstrap,
    "docs/adr/adr.json-schemas.draft.md",
    SourceArtifactType.SourceFile,
    "c95dfb0928ba1398eb058a7bb16b21f2dad77f4116169cbcc8075fb5186c2df5",
    "Excerpted and summarized before browser runtime; the browser does not read the repository source file.",
    "The hash identifies the source fixture used for review, not canonical product authority."
  )
};

export const proposedAdrJsonRef: ContentRef = {
  id: "content.proposed.adr-json-schemas-json",
  title: "Proposed active conformed JSON checkpoint",
  kind: ContentKind.ConformedJsonCheckpoint,
  locator: "dev/adr-json-schemas-conformance/adr.json-schemas.json",
  contentHash: "e5f8c6729ee120ae4a266e6d5d575df3b9ae6f9fb86158c92a29995386a89bfb",
  hashLabel: HashLabel.FixtureSourceIdentityHash,
  metadata: metadataFactory.build(
    "fixture.proposed.adr-json-schemas-json",
    FixtureStatus.TransformedFromBootstrap,
    "dev/adr-json-schemas-conformance/adr.json-schemas.json",
    SourceArtifactType.ConformanceArtifact,
    "e5f8c6729ee120ae4a266e6d5d575df3b9ae6f9fb86158c92a29995386a89bfb",
    "Excerpted and summarized before browser runtime; the browser does not read the repository JSON file.",
    "The hash identifies the proposed fixture used for review, not canonical product authority."
  )
};

export const contentBodies: Readonly<Record<string, string>> = {
  [currentAdrMarkdownRef.id]: [
    "# ADR 20260702.213000Z: JSON Schemas Namespace",
    "Status: draft",
    "Current source is Markdown-shaped ADR text under docs/adr/.",
    "It contains source-only routing owner/next phase/notes and links.related material.",
    "The conformance slice records this source as unmutated."
  ].join("\n"),
  [proposedAdrJsonRef.id]: [
    "{",
    "  \"id\": \"adr.json-schemas\",",
    "  \"slug\": \"json-schemas\",",
    "  \"status\": \"draft\",",
    "  \"title\": \"JSON Schemas Namespace\"",
    "}",
    "The proposed checkpoint is schema-shaped JSON. It omits routing and links.related from the record while sidecars preserve that provenance."
  ].join("\n")
};

export const implementationReportEvidence: EvidenceRef = {
  id: "evidence.vulcan-json-schemas-report",
  title: "VULCAN implementation and validation report",
  kind: EvidenceKind.ImplementationReport,
  locator: "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
  contentHash: "8fea236558950935e9f76e754c62bea8d12b8b8c62a932d45cca4d9b1350c340",
  summary: "Reports source non-mutation, schema validation, sidecar preservation, and validation outcomes for the conformance slice.",
  displayedAs: FixtureStatus.TransformedFromBootstrap,
  metadata: metadataFactory.build(
    "fixture.evidence.vulcan-json-schemas-report",
    FixtureStatus.TransformedFromBootstrap,
    "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
    SourceArtifactType.ImplementationReport,
    "8fea236558950935e9f76e754c62bea8d12b8b8c62a932d45cca4d9b1350c340",
    "Summarized for the evidence panel; command outcomes are copied as reported evidence and are not rerun by the console.",
    "Trust comes from cited validation outputs and explicit source/sidecar boundaries in the report."
  )
};

export const conversionEvidence: EvidenceRef = {
  id: "evidence.conversion-sidecar",
  title: "Conversion evidence sidecar",
  kind: EvidenceKind.Sidecar,
  locator: "dev/adr-json-schemas-conformance/conversion-evidence.json",
  contentHash: "4d25dc685d0adef7af824389e2b20b9d1dceb38a519afe0ea5ceb47997f98012",
  summary: "Preserves source hash/date/status, schema hash, record hash, projection hash, and omitted routing/related-link provenance.",
  displayedAs: FixtureStatus.TransformedFromBootstrap,
  metadata: metadataFactory.build(
    "fixture.evidence.conversion-sidecar",
    FixtureStatus.TransformedFromBootstrap,
    "dev/adr-json-schemas-conformance/conversion-evidence.json",
    SourceArtifactType.Sidecar,
    "4d25dc685d0adef7af824389e2b20b9d1dceb38a519afe0ea5ceb47997f98012",
    "Selected fields summarized for the evidence panel; the fixture imports copied values rather than reading the sidecar at runtime.",
    "Trust comes from explicit hashes and omitted-field provenance captured by the conformance run."
  )
};

export const mappingEvidence: EvidenceRef = {
  id: "evidence.mapping-sidecar",
  title: "Field mapping sidecar",
  kind: EvidenceKind.Sidecar,
  locator: "dev/adr-json-schemas-conformance/mapping.json",
  contentHash: "55078b3d4c2b36007e77afe3feec34c987f49d03123f636dfdf07995431d6298",
  summary: "Lists copied fields, normalized values, omitted fields, and generated hashes for the conformed record.",
  displayedAs: FixtureStatus.TransformedFromBootstrap,
  metadata: metadataFactory.build(
    "fixture.evidence.mapping-sidecar",
    FixtureStatus.TransformedFromBootstrap,
    "dev/adr-json-schemas-conformance/mapping.json",
    SourceArtifactType.Sidecar,
    "55078b3d4c2b36007e77afe3feec34c987f49d03123f636dfdf07995431d6298",
    "Summarized mapping categories for review; the browser does not read repository sidecars.",
    "Trust comes from inspectable copied/normalized/omitted field treatment."
  )
};

export const manifestEvidence: EvidenceRef = {
  id: "evidence.conformance-manifest",
  title: "Conformance manifest",
  kind: EvidenceKind.Manifest,
  locator: "dev/adr-json-schemas-conformance/manifest.json",
  contentHash: "678e5aa1dcd6c12bbe378316a19830521ccc86b8945bba853c8a9bc608ca79b1",
  summary: "Records active conformance status, authority mode, document-store evidence, and no-source-mutation/no-committed-DB watchpoints.",
  displayedAs: FixtureStatus.TransformedFromBootstrap,
  metadata: metadataFactory.build(
    "fixture.evidence.conformance-manifest",
    FixtureStatus.TransformedFromBootstrap,
    "dev/adr-json-schemas-conformance/manifest.json",
    SourceArtifactType.Manifest,
    "678e5aa1dcd6c12bbe378316a19830521ccc86b8945bba853c8a9bc608ca79b1",
    "Summarized authority and watchpoint fields for review.",
    "Trust comes from manifest watchpoints and conformance status metadata."
  )
};

export const evidenceRefs: readonly EvidenceRef[] = [
  implementationReportEvidence,
  conversionEvidence,
  mappingEvidence,
  manifestEvidence
];

export const validationResults: readonly ValidationResult[] = [
  {
    id: "validation.adr-json-schemas-conformance",
    targetProposalId: "proposal.adr-json-schemas-conformance",
    status: ValidationStatus.Passed,
    category: ValidationCategory.Test,
    commandSummary:
      "Reported fixture evidence: targeted test 4 passed; focused suite 33 passed; mypy success; ruff passed; python policy zero findings; git diff check clean; docs/adr unchanged; no generated database files.",
    consoleReranCommand: false,
    findings: [
      {
        level: ValidationFindingLevel.Info,
        message: "The console displays copied command outcomes from fixture evidence; it does not rerun validation commands."
      },
      {
        level: ValidationFindingLevel.Info,
        message: "The earlier KOIOS missing-report watchpoint is treated as resolved by the VULCAN implementation report."
      }
    ],
    evidenceRefIds: evidenceRefs.map((evidence: EvidenceRef) => evidence.id),
    metadata: metadataFactory.build(
      "fixture.validation.adr-json-schemas-conformance",
      FixtureStatus.TransformedFromBootstrap,
      "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
      SourceArtifactType.ValidationOutputSummary,
      "8fea236558950935e9f76e754c62bea8d12b8b8c62a932d45cca4d9b1350c340",
      "Validation outcomes copied from the report; no commands are rerun by the browser.",
      "Trust comes from reported validation evidence and hash-linked source artifacts."
    )
  }
];

export const agentStatuses: readonly AgentStatus[] = [
  {
    id: "agent.fixture.vulcan",
    displayName: "VULCAN fixture status",
    representedRole: "VULCAN",
    workspace: "workspaces/vulcan/",
    state: AgentState.FixtureStatic,
    lastSeen: fixtureTimestamp,
    activitySummary: "Static fixture snapshot for the completed adr.json-schemas conformance review. Not a live agent monitor.",
    evidenceRefId: implementationReportEvidence.id,
    staleByDesign: true,
    metadata: metadataFactory.build(
      "fixture.agent.vulcan",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.SyntheticFixture,
      "synthetic-agent-status-no-product-authority",
      "Synthetic status card built for P0 browser layout only.",
      "Do not treat this card as live operational truth."
    )
  }
];

export const externalStatuses: readonly ExternalSystemStatus[] = [
  {
    id: "external.fixture.validation-snapshot",
    displayName: "Validation evidence snapshot",
    statusClass: StatusClass.Unknown,
    lastChecked: fixtureTimestamp,
    summary: "Static fixture card summarizing existing validation evidence. It is stale-by-design and not a live external health check.",
    evidenceRefIds: [implementationReportEvidence.id],
    staleByDesign: true,
    metadata: metadataFactory.build(
      "fixture.external.validation-snapshot",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.SyntheticFixture,
      "synthetic-external-status-no-live-health-claim",
      "Synthetic external status card for P0 layout proof only.",
      "Trust is limited to cited fixture evidence; there is no live status polling."
    )
  }
];

export const changeProposals: readonly ChangeProposal[] = [
  {
    id: "proposal.adr-json-schemas-conformance",
    kind: ProposalKind.AdrConformanceReview,
    title: "Review active conformed JSON checkpoint for adr.json-schemas",
    summary:
      "Compare the current Markdown-shaped ADR source with the proposed active conformed JSON checkpoint and its sidecar evidence.",
    currentRefId: currentAdrMarkdownRef.id,
    proposedRefId: proposedAdrJsonRef.id,
    evidenceRefIds: evidenceRefs.map((evidence: EvidenceRef) => evidence.id),
    validationResultIds: validationResults.map((validation: ValidationResult) => validation.id),
    author: "VULCAN fixture from approved conformance slice",
    reviewOnly: true,
    mutationUnavailableReason: "P0 review is display-only and does not provide mutation controls or workflow changes.",
    createdAt: fixtureTimestamp,
    updatedAt: fixtureTimestamp,
    metadata: metadataFactory.build(
      "fixture.proposal.adr-json-schemas-conformance",
      FixtureStatus.TransformedFromBootstrap,
      "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
      SourceArtifactType.ChangeProposalFixture,
      "8fea236558950935e9f76e754c62bea8d12b8b8c62a932d45cca4d9b1350c340",
      "Proposal assembled from copied and summarized bootstrap conformance evidence.",
      "Trust is bounded to fixture review of source/proposed/evidence refs, not product authority."
    )
  }
];

export const contentRefs: readonly ContentRef[] = [currentAdrMarkdownRef, proposedAdrJsonRef];
