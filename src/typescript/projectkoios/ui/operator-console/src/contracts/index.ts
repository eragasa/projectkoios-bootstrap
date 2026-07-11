export enum FixtureStatus {
  Synthetic = "synthetic",
  CopiedFromBootstrap = "copied-from-bootstrap",
  TransformedFromBootstrap = "transformed-from-bootstrap"
}

export enum AuthorityBoundary {
  FixtureOnly = "fixture-only",
  NonLive = "non-live",
  NonProduction = "non-production",
  NonAuthoritative = "non-authoritative"
}

export enum StatusClass {
  Healthy = "healthy",
  Degraded = "degraded",
  Down = "down",
  Unknown = "unknown"
}

export enum ValidationStatus {
  Pending = "pending",
  Passed = "passed",
  Failed = "failed",
  Warning = "warning"
}

export enum ValidationCategory {
  Syntax = "syntax",
  Semantic = "semantic",
  OperationalSafety = "operational-safety",
  Policy = "policy",
  Build = "build",
  Test = "test"
}

export enum InteractionSurface {
  Terminal = "terminal",
  Console = "console",
  Automation = "automation",
  ImportedTranscript = "imported-transcript"
}

export enum InteractionDirection {
  TerminalOriginated = "terminal-originated",
  ConsoleOriginated = "console-originated",
  AutomationOriginated = "automation-originated",
  Imported = "imported"
}

export enum ContentKind {
  SourceMarkdown = "source-markdown",
  ConformedJsonCheckpoint = "conformed-json-checkpoint"
}

export enum EvidenceKind {
  ImplementationReport = "implementation-report",
  Sidecar = "sidecar",
  Manifest = "manifest",
  AgentInteraction = "agent-interaction"
}

export enum ProposalKind {
  AdrConformanceReview = "adr-conformance-review"
}

export enum SourceArtifactType {
  SourceFile = "source-file",
  ConformanceArtifact = "conformance-artifact",
  ImplementationReport = "implementation-report",
  Sidecar = "sidecar",
  Manifest = "manifest",
  ValidationOutputSummary = "validation-output-summary",
  SyntheticFixture = "synthetic-fixture",
  ChangeProposalFixture = "change-proposal-fixture",
  AgentInteractionFixture = "agent-interaction-fixture"
}

export enum HashLabel {
  FixtureSourceIdentityHash = "fixture/source identity hash"
}

export enum ValidationFindingLevel {
  Info = "info",
  Warning = "warning",
  Error = "error"
}

export enum AgentState {
  FixtureStatic = "fixture-static",
  Unknown = "unknown"
}

export enum DeliveryStatus {
  Observed = "observed",
  Sent = "sent",
  Received = "received",
  Pending = "pending",
  Answered = "answered",
  Failed = "failed"
}

export enum WorkflowStatus {
  Active = "active",
  Draft = "draft",
  Archived = "archived",
  Unknown = "unknown"
}

export enum ApprovalState {
  NotStarted = "not-started",
  Reviewing = "reviewing",
  Approved = "approved",
  Rejected = "rejected"
}

export enum ImplementationReviewStatus {
  AcceptedStaticSnapshot = "accepted-static-snapshot"
}

export enum OwnerDomain {
  Architecture = "architecture",
  Implementation = "implementation",
  Review = "review",
  Provenance = "provenance",
  Source = "source"
}

export interface FixtureMetadata {
  readonly fixtureId: string;
  readonly fixtureStatus: FixtureStatus;
  readonly sourceLocator: string;
  readonly sourceArtifactType: SourceArtifactType;
  readonly sourceHash: string;
  readonly capturedAt: string;
  readonly freshness: string;
  readonly authorityBoundary: readonly AuthorityBoundary[];
  readonly provenanceSummary: string;
  readonly transformationNotes: string;
  readonly trustExplanation: string;
}

export interface ContentRef {
  readonly id: string;
  readonly title: string;
  readonly kind: ContentKind;
  readonly locator: string;
  readonly contentHash: string;
  readonly hashLabel: HashLabel;
  readonly metadata: FixtureMetadata;
}

export interface EvidenceRef {
  readonly id: string;
  readonly title: string;
  readonly kind: EvidenceKind;
  readonly locator: string;
  readonly contentHash: string;
  readonly summary: string;
  readonly displayedAs: FixtureStatus;
  readonly metadata: FixtureMetadata;
}

export interface ValidationFinding {
  readonly level: ValidationFindingLevel;
  readonly message: string;
}

export interface ValidationResult {
  readonly id: string;
  readonly targetProposalId: string;
  readonly status: ValidationStatus;
  readonly category: ValidationCategory;
  readonly commandSummary: string;
  readonly consoleReranCommand: false;
  readonly findings: readonly ValidationFinding[];
  readonly evidenceRefIds: readonly string[];
  readonly metadata: FixtureMetadata;
}

export interface AgentStatus {
  readonly id: string;
  readonly displayName: string;
  readonly representedRole: string;
  readonly workspace: string;
  readonly state: AgentState;
  readonly lastSeen: string;
  readonly activitySummary: string;
  readonly evidenceRefId: string;
  readonly staleByDesign: true;
  readonly metadata: FixtureMetadata;
}

export interface AgentMessage {
  readonly id: string;
  readonly threadId: string;
  readonly sessionId: string;
  readonly surface: InteractionSurface;
  readonly direction: InteractionDirection;
  readonly senderId: string;
  readonly recipientId: string;
  readonly representedRole: string;
  readonly timestamp: string;
  readonly summary: string;
  readonly body: string;
  readonly deliveryStatus: DeliveryStatus;
  readonly evidenceRefId: string;
  readonly metadata: FixtureMetadata;
}

export interface AgentThread {
  readonly id: string;
  readonly title: string;
  readonly sessionId: string;
  readonly representedRole: string;
  readonly summary: string;
  readonly messageIds: readonly string[];
  readonly interactionIds: readonly string[];
  readonly evidenceRefIds: readonly string[];
  readonly metadata: FixtureMetadata;
}

export interface AgentInteraction {
  readonly id: string;
  readonly threadId: string;
  readonly messageId: string;
  readonly sessionId: string;
  readonly surface: InteractionSurface;
  readonly direction: InteractionDirection;
  readonly representedRole: string;
  readonly timestamp: string;
  readonly summary: string;
  readonly body: string;
  readonly deliveryStatus: DeliveryStatus;
  readonly transcriptLocator: string;
  readonly evidenceRefId: string;
  readonly metadata: FixtureMetadata;
}

export interface ExternalSystemStatus {
  readonly id: string;
  readonly displayName: string;
  readonly statusClass: StatusClass.Unknown;
  readonly lastChecked: string;
  readonly summary: string;
  readonly evidenceRefIds: readonly string[];
  readonly staleByDesign: true;
  readonly metadata: FixtureMetadata;
}

export interface ChangeProposal {
  readonly id: string;
  readonly kind: ProposalKind;
  readonly title: string;
  readonly summary: string;
  readonly currentRefId: string;
  readonly proposedRefId: string;
  readonly evidenceRefIds: readonly string[];
  readonly validationResultIds: readonly string[];
  readonly author: string;
  readonly reviewOnly: true;
  readonly mutationUnavailableReason: string;
  readonly createdAt: string;
  readonly updatedAt: string;
  readonly metadata: FixtureMetadata;
}

export interface WorkflowDefinitionRef {
  readonly id: string;
  readonly version: string;
  readonly contentHash: string;
  readonly status: WorkflowStatus;
  readonly sourceLocator: string;
  readonly summary: string;
  readonly validationState: ValidationStatus;
}

export interface WorkflowDraft {
  readonly id: string;
  readonly baseWorkflowRefId: string;
  readonly proposedContentRefId: string;
  readonly author: string;
  readonly validationResultIds: readonly string[];
  readonly createdAt: string;
  readonly updatedAt: string;
}

export interface WorkflowProposal {
  readonly id: string;
  readonly draftId: string;
  readonly baseWorkflowRefId: string;
  readonly proposedContentRefId: string;
  readonly validationResultIds: readonly string[];
  readonly approvalState: ApprovalState;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export interface ImplementationReviewItem {
  readonly id: string;
  readonly sliceName: string;
  readonly displayName: string;
  readonly status: ImplementationReviewStatus;
  readonly ownerDomain: OwnerDomain;
  readonly implementationReportLocator: string;
  readonly acceptanceReviewLocator: string;
  readonly validationSummary: string;
  readonly validationSourceLocator: string;
  readonly authorityBoundary: string;
  readonly fixtureDerivedStatus: true;
  readonly evidenceLocators: readonly string[];
  readonly snapshotGeneratedAt: string;
  readonly sourceHashLabel: string;
}

export interface WorkflowObjectSummaryFixture {
  readonly recordId: string;
  readonly status: ImplementationReviewStatus;
  readonly snapshotGeneratedAt: string;
  readonly sourceHashTimestampLabel: string;
  readonly nonAuthorityMarkers: readonly string[];
  readonly artifactRecordCount: number;
  readonly gateEvaluationCount: number;
  readonly validationEvidenceCount: number;
  readonly previewEvidenceCount: number;
  readonly packageSourceRef: string;
  readonly hashCaveat: string;
  readonly refreshProtocolStatement: string;
  readonly staleHashPackagingRule: string;
}

export interface CurrentImplementationReviewReadModel {
  readonly panelTitle: string;
  readonly snapshotLabel: string;
  readonly snapshotGeneratedAt: string;
  readonly stalenessWarning: string;
  readonly statusSourceStatement: string;
  readonly items: readonly ImplementationReviewItem[];
  readonly workflowObjectSummary: WorkflowObjectSummaryFixture;
}

export interface ResolvedChangeProposal {
  readonly proposal: ChangeProposal;
  readonly current: ResolvedContent;
  readonly proposed: ResolvedContent;
  readonly evidence: readonly EvidenceRef[];
  readonly validations: readonly ValidationResult[];
}

export interface ResolvedContent {
  readonly ref: ContentRef;
  readonly body: string;
}

export interface ResolvedAgentInteraction {
  readonly interaction: AgentInteraction;
  readonly message: AgentMessage;
  readonly evidence: EvidenceRef;
}

export interface ResolvedAgentThread {
  readonly thread: AgentThread;
  readonly interactions: readonly ResolvedAgentInteraction[];
  readonly evidence: readonly EvidenceRef[];
}

export interface DashboardReadModel {
  readonly agentStatuses: readonly AgentStatus[];
  readonly externalStatuses: readonly ExternalSystemStatus[];
  readonly currentImplementationReview: CurrentImplementationReviewReadModel;
  readonly interactionThreads: readonly ResolvedAgentThread[];
  readonly primaryProposal: ResolvedChangeProposal;
}
