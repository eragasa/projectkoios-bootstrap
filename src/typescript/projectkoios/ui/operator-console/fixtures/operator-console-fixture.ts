import {
  AgentState,
  AuthorityBoundary,
  ContentKind,
  DeliveryStatus,
  EvidenceKind,
  FixtureStatus,
  HashLabel,
  ImplementationReviewStatus,
  InteractionDirection,
  InteractionSurface,
  OwnerDomain,
  ProposalKind,
  SourceArtifactType,
  StatusClass,
  ValidationCategory,
  ValidationFindingLevel,
  ValidationStatus
} from "../src/contracts";
import type {
  AgentInteraction,
  AgentMessage,
  AgentStatus,
  AgentThread,
  ChangeProposal,
  ContentRef,
  EvidenceRef,
  ExternalSystemStatus,
  FixtureMetadata,
  ImplementationReviewItem,
  ValidationResult,
  WorkflowObjectSummaryFixture
} from "../src/contracts";

const fixtureTimestamp = "20260711.074650Z";
const currentImplementationSnapshotTimestamp = "20260711.111457Z";

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

export const terminalInteractionEvidence: EvidenceRef = {
  id: "evidence.interaction-terminal-vulcan",
  title: "Terminal-originated VULCAN interaction fixture",
  kind: EvidenceKind.AgentInteraction,
  locator: "fixture://operator-console/interactions/terminal-vulcan-plan-summary",
  contentHash: "synthetic-terminal-interaction-fixture-hash",
  summary: "Synthetic terminal-originated fixture showing a local agent terminal update surfaced in the console.",
  displayedAs: FixtureStatus.Synthetic,
  metadata: metadataFactory.build(
    "fixture.evidence.interaction-terminal-vulcan",
    FixtureStatus.Synthetic,
    "fixtures/operator-console-fixture.ts",
    SourceArtifactType.AgentInteractionFixture,
    "synthetic-terminal-interaction-fixture-hash",
    "Synthetic interaction evidence created before browser runtime; no terminal transcript is read.",
    "Trust is limited to fixture layout validation; this is not live terminal state."
  )
};

export const consoleInteractionEvidence: EvidenceRef = {
  id: "evidence.interaction-console-example",
  title: "Console-originated example interaction fixture",
  kind: EvidenceKind.AgentInteraction,
  locator: "fixture://operator-console/interactions/console-example-acknowledgement",
  contentHash: "synthetic-console-interaction-fixture-hash",
  summary: "Synthetic console-originated fixture showing how a future console message could be displayed without enabling outbound messaging.",
  displayedAs: FixtureStatus.Synthetic,
  metadata: metadataFactory.build(
    "fixture.evidence.interaction-console-example",
    FixtureStatus.Synthetic,
    "fixtures/operator-console-fixture.ts",
    SourceArtifactType.AgentInteractionFixture,
    "synthetic-console-interaction-fixture-hash",
    "Synthetic interaction evidence created before browser runtime; outbound console messaging is unavailable.",
    "Trust is limited to fixture layout validation; this is not live console messaging."
  )
};

export const evidenceRefs: readonly EvidenceRef[] = [
  implementationReportEvidence,
  conversionEvidence,
  mappingEvidence,
  manifestEvidence,
  terminalInteractionEvidence,
  consoleInteractionEvidence
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

export const agentMessages: readonly AgentMessage[] = [
  {
    id: "message.terminal.vulcan-summary",
    threadId: "thread.operator-console-fixture-interactions",
    sessionId: "subagent-chat-fixture-vulcan",
    surface: InteractionSurface.Terminal,
    direction: InteractionDirection.TerminalOriginated,
    senderId: "agent.vulcan",
    recipientId: "operator.console.fixture",
    representedRole: "VULCAN",
    timestamp: fixtureTimestamp,
    summary: "VULCAN terminal fixture reports that the P0 proposal review is implemented and validated.",
    body: "Terminal-originated fixture: VULCAN reports completed P0 validation evidence for the proposal review screen.",
    deliveryStatus: DeliveryStatus.Observed,
    evidenceRefId: terminalInteractionEvidence.id,
    metadata: metadataFactory.build(
      "fixture.message.terminal.vulcan-summary",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.AgentInteractionFixture,
      "synthetic-terminal-message-fixture-hash",
      "Synthetic terminal-originated message fixture; no terminal transcript is read at runtime.",
      "Shows interaction visibility layout only; not live agent communication."
    )
  },
  {
    id: "message.console.example-acknowledgement",
    threadId: "thread.operator-console-fixture-interactions",
    sessionId: "operator-console-fixture-session",
    surface: InteractionSurface.Console,
    direction: InteractionDirection.ConsoleOriginated,
    senderId: "operator.console.fixture",
    recipientId: "agent.vulcan",
    representedRole: "OPERATOR",
    timestamp: fixtureTimestamp,
    summary: "Console-originated example fixture acknowledges the reviewed evidence without enabling outbound messaging.",
    body: "Console-originated example fixture: acknowledged for display only. The P0/P1 console provides no outbound messaging control.",
    deliveryStatus: DeliveryStatus.Observed,
    evidenceRefId: consoleInteractionEvidence.id,
    metadata: metadataFactory.build(
      "fixture.message.console.example-acknowledgement",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.AgentInteractionFixture,
      "synthetic-console-message-fixture-hash",
      "Synthetic console-originated message fixture; no message was sent by the browser.",
      "Shows future-direction distinction only; not live console communication."
    )
  }
];

export const agentInteractions: readonly AgentInteraction[] = [
  {
    id: "interaction.terminal.vulcan-summary",
    threadId: "thread.operator-console-fixture-interactions",
    messageId: "message.terminal.vulcan-summary",
    sessionId: "subagent-chat-fixture-vulcan",
    surface: InteractionSurface.Terminal,
    direction: InteractionDirection.TerminalOriginated,
    representedRole: "VULCAN",
    timestamp: fixtureTimestamp,
    summary: "Terminal-originated VULCAN fixture update.",
    body: "A local VULCAN terminal update would appear here as display-only read-model data.",
    deliveryStatus: DeliveryStatus.Observed,
    transcriptLocator: "fixture://transcripts/subagent-chat-fixture-vulcan#terminal-summary",
    evidenceRefId: terminalInteractionEvidence.id,
    metadata: metadataFactory.build(
      "fixture.interaction.terminal.vulcan-summary",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.AgentInteractionFixture,
      "synthetic-terminal-interaction-read-model-hash",
      "Synthetic terminal-originated interaction fixture; no terminal/session source is read at runtime.",
      "Demonstrates central visibility without replacing terminal interaction surfaces."
    )
  },
  {
    id: "interaction.console.example-acknowledgement",
    threadId: "thread.operator-console-fixture-interactions",
    messageId: "message.console.example-acknowledgement",
    sessionId: "operator-console-fixture-session",
    surface: InteractionSurface.Console,
    direction: InteractionDirection.ConsoleOriginated,
    representedRole: "OPERATOR",
    timestamp: fixtureTimestamp,
    summary: "Console-originated example fixture acknowledgement.",
    body: "A future console-originated message would be displayed here after going through an approved communication substrate.",
    deliveryStatus: DeliveryStatus.Observed,
    transcriptLocator: "fixture://transcripts/operator-console-fixture-session#example-acknowledgement",
    evidenceRefId: consoleInteractionEvidence.id,
    metadata: metadataFactory.build(
      "fixture.interaction.console.example-acknowledgement",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.AgentInteractionFixture,
      "synthetic-console-interaction-read-model-hash",
      "Synthetic console-originated interaction fixture; the browser exposes no outbound messaging action.",
      "Demonstrates direction labeling only; not live console messaging."
    )
  }
];

export const agentThreads: readonly AgentThread[] = [
  {
    id: "thread.operator-console-fixture-interactions",
    title: "Operator Console fixture interaction visibility",
    sessionId: "operator-console-fixture-thread",
    representedRole: "VULCAN / OPERATOR",
    summary: "Static fixture thread showing terminal-originated and console-originated/example interactions in one read model.",
    messageIds: agentMessages.map((message: AgentMessage) => message.id),
    interactionIds: agentInteractions.map((interaction: AgentInteraction) => interaction.id),
    evidenceRefIds: [terminalInteractionEvidence.id, consoleInteractionEvidence.id],
    metadata: metadataFactory.build(
      "fixture.thread.operator-console-fixture-interactions",
      FixtureStatus.Synthetic,
      "fixtures/operator-console-fixture.ts",
      SourceArtifactType.AgentInteractionFixture,
      "synthetic-interaction-thread-fixture-hash",
      "Synthetic thread fixture; no session or transcript is read at runtime.",
      "Shows central visibility over multiple interaction surfaces while remaining static and non-live."
    )
  }
];

export const currentImplementationReviewItems: readonly ImplementationReviewItem[] = [
  {
    id: "implementation-review.operator-console-p0",
    sliceName: "operator-console-review-one-proposal-fixture",
    displayName: "Operator Console P0 review-one-proposal fixture",
    status: ImplementationReviewStatus.AcceptedStaticSnapshot,
    ownerDomain: OwnerDomain.Implementation,
    implementationReportLocator: "docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md",
    acceptanceReviewLocator: "docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md",
    validationSourceLocator: "docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md",
    validationSummary: "Static copied summary: P0 package validation and browser preview evidence accepted by review.",
    authorityBoundary: "static snapshot; fixture-only; not live; not product authority",
    fixtureDerivedStatus: true,
    evidenceLocators: [
      "docs/architecture/architecture.operator-console.md",
      "docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md",
      "docs/reviews/architecture-conformance.20260711.081734_operator-console-review-one-proposal-fixture.md"
    ],
    snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
    sourceHashLabel: "fixture-generation/source-snapshot timestamp; not live freshness"
  },
  {
    id: "implementation-review.operator-console-actionobject-refactor",
    sliceName: "operator-console-actionobject-refactor",
    displayName: "Operator Console ActionObject/DataObject refactor",
    status: ImplementationReviewStatus.AcceptedStaticSnapshot,
    ownerDomain: OwnerDomain.Review,
    implementationReportLocator: "docs/implementation/operator-console-review-one-proposal-fixture.20260711.081405.md",
    acceptanceReviewLocator: "docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md",
    validationSourceLocator: "docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md",
    validationSummary: "Static copied summary: ActionObject/DataObject conformance review accepted the refactor evidence.",
    authorityBoundary: "static snapshot; fixture-only; not live; not product authority",
    fixtureDerivedStatus: true,
    evidenceLocators: [
      "docs/architecture/architecture.operator-console.md",
      "docs/reviews/architecture-conformance.20260711.082740_operator-console-actionobject-refactor.md"
    ],
    snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
    sourceHashLabel: "fixture-generation/source-snapshot timestamp; not live freshness"
  },
  {
    id: "implementation-review.operator-console-p1",
    sliceName: "operator-console-fixture-interaction-visibility",
    displayName: "Operator Console P1 interaction visibility",
    status: ImplementationReviewStatus.AcceptedStaticSnapshot,
    ownerDomain: OwnerDomain.Implementation,
    implementationReportLocator: "docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md",
    acceptanceReviewLocator: "docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md",
    validationSourceLocator: "docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md",
    validationSummary: "Static copied summary: interaction visibility typecheck, tests, build, audit, and preview passed.",
    authorityBoundary: "static snapshot; fixture-only; not live; not product authority",
    fixtureDerivedStatus: true,
    evidenceLocators: [
      "docs/implementation/operator-console-fixture-interaction-visibility.20260711.090601.md",
      "docs/reviews/architecture-conformance.20260711.091137_operator-console-fixture-interaction-visibility.md"
    ],
    snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
    sourceHashLabel: "fixture-generation/source-snapshot timestamp; not live freshness"
  },
  {
    id: "implementation-review.operator-console-p2",
    sliceName: "operator-console-readability-navigation-fixture",
    displayName: "Operator Console P2 readability/navigation fixture",
    status: ImplementationReviewStatus.AcceptedStaticSnapshot,
    ownerDomain: OwnerDomain.Implementation,
    implementationReportLocator: "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
    acceptanceReviewLocator: "docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md",
    validationSourceLocator: "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
    validationSummary: "Static copied summary: readability/navigation typecheck, tests, build, audit, and preview passed.",
    authorityBoundary: "static snapshot; fixture-only; not live; not product authority",
    fixtureDerivedStatus: true,
    evidenceLocators: [
      "docs/implementation/operator-console-readability-navigation-fixture.20260711.092524.md",
      "docs/reviews/architecture-conformance.20260711.093009_operator-console-readability-navigation-fixture.md"
    ],
    snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
    sourceHashLabel: "fixture-generation/source-snapshot timestamp; not live freshness"
  },
  {
    id: "implementation-review.workflow-object-slice-0",
    sliceName: "workflow-object-static-operator-console-record",
    displayName: "Workflow-object Slice 0 static Operator Console record",
    status: ImplementationReviewStatus.AcceptedStaticSnapshot,
    ownerDomain: OwnerDomain.Provenance,
    implementationReportLocator: "docs/implementation/workflow-object-static-operator-console-record.20260711.105117.md",
    acceptanceReviewLocator: "docs/reviews/implementation-review.20260711.105822_workflow-object-static-operator-console-record.md",
    validationSourceLocator: "tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py",
    validationSummary: "Static copied summary: workflow-object static-record validator passed after current hash remediation.",
    authorityBoundary: "static snapshot; projection/index only; not schema authority; not live",
    fixtureDerivedStatus: true,
    evidenceLocators: [
      "dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json",
      "tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py",
      "docs/implementation/workflow-object-static-operator-console-record.20260711.105117.md",
      "docs/reviews/implementation-review.20260711.105822_workflow-object-static-operator-console-record.md"
    ],
    snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
    sourceHashLabel: "fixture-generation/source-snapshot timestamp; not live freshness"
  }
];

export const workflowObjectSummaryFixture: WorkflowObjectSummaryFixture = {
  recordId: "workflow-object.operator-console-bootstrap-bundle.20260711",
  status: ImplementationReviewStatus.AcceptedStaticSnapshot,
  snapshotGeneratedAt: currentImplementationSnapshotTimestamp,
  sourceHashTimestampLabel: "source hashes are working-tree content refs observed at fixture generation time",
  nonAuthorityMarkers: [
    "projection-index-only",
    "not-source-authority",
    "not-completion-authority",
    "not-petri-net-runtime",
    "not-storage-authority",
    "not-schema-authority",
    "static-record",
    "bootstrap-incubation",
    "fixture-only",
    "non-live",
    "stale-by-design",
    "not-product-authority"
  ],
  artifactRecordCount: 9,
  gateEvaluationCount: 3,
  validationEvidenceCount: 1,
  previewEvidenceCount: 1,
  packageSourceRef: "src/typescript/projectkoios/ui/operator-console/package.json",
  hashCaveat:
    "Hashes identify the referenced working-tree file contents at fixture generation time; they are not commit IDs and do not make this UI or workflow object source authority. This screen is a static snapshot, not live operational truth, and may be stale until intentionally refreshed.",
  refreshProtocolStatement: "Workflow-object refresh protocol is not yet defined for this static fixture screen.",
  staleHashPackagingRule:
    "Stale source hashes require workflow-object static-record validator rerun before packaging or explicit intentional-staleness recording."
};

export const contentRefs: readonly ContentRef[] = [currentAdrMarkdownRef, proposedAdrJsonRef];
