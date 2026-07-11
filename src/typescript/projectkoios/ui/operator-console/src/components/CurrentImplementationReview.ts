import type { CurrentImplementationReviewReadModel, ImplementationReviewItem } from "../contracts";
import { HtmlRenderer } from "./html";

export class CurrentImplementationReviewRenderer {
  constructor(private readonly html: HtmlRenderer) {}

  render(review: CurrentImplementationReviewReadModel): string {
    const items: string = review.items.map((item: ImplementationReviewItem) => this.renderItem(item)).join("");
    return [
      '<section class="current-implementation-review" id="current-implementation-review" aria-labelledby="current-implementation-review-title">',
      `<h2 id="current-implementation-review-title">${this.html.escape(review.panelTitle)}</h2>`,
      `<p class="snapshot-warning">${this.html.escape(review.snapshotLabel)}</p>`,
      `<p>Snapshot generated: <code>${this.html.escape(review.snapshotGeneratedAt)}</code></p>`,
      `<p>${this.html.escape(review.stalenessWarning)}</p>`,
      `<p>${this.html.escape(review.statusSourceStatement)}</p>`,
      '<div class="implementation-review-grid">',
      items,
      "</div>",
      this.renderWorkflowObjectSummary(review),
      "</section>"
    ].join("");
  }

  private renderItem(item: ImplementationReviewItem): string {
    const evidenceLocators: string = item.evidenceLocators
      .map((locator: string) => `<li><code>${this.html.escape(locator)}</code></li>`)
      .join("");
    return [
      '<article class="implementation-review-card">',
      `<h3>${this.html.escape(item.displayName)}</h3>`,
      `<p>Slice: <code>${this.html.escape(item.sliceName)}</code></p>`,
      `<p>Status: ${this.html.escape(item.status)}; fixture-derived: ${String(item.fixtureDerivedStatus)}</p>`,
      `<p>Owner/domain: ${this.html.escape(item.ownerDomain)}</p>`,
      `<p>Implementation report: <code>${this.html.escape(item.implementationReportLocator)}</code></p>`,
      `<p>Review evidence: <code>${this.html.escape(item.acceptanceReviewLocator)}</code></p>`,
      `<p>Validation source: <code>${this.html.escape(item.validationSourceLocator)}</code></p>`,
      `<p>${this.html.escape(item.validationSummary)}</p>`,
      `<p>Authority boundary: ${this.html.escape(item.authorityBoundary)}</p>`,
      `<p>Snapshot/source label: ${this.html.escape(item.sourceHashLabel)} at <code>${this.html.escape(item.snapshotGeneratedAt)}</code></p>`,
      '<p>Display locators only:</p>',
      `<ul>${evidenceLocators}</ul>`,
      "</article>"
    ].join("");
  }

  private renderWorkflowObjectSummary(review: CurrentImplementationReviewReadModel): string {
    const summary = review.workflowObjectSummary;
    const markers: string = summary.nonAuthorityMarkers
      .map((marker: string) => `<li>${this.html.escape(marker)}</li>`)
      .join("");
    return [
      '<article class="workflow-object-summary-card">',
      '<h3>Workflow-object Slice 0 summary</h3>',
      `<p>Record id: <code>${this.html.escape(summary.recordId)}</code></p>`,
      `<p>Status: ${this.html.escape(summary.status)}</p>`,
      `<p>Snapshot generated: <code>${this.html.escape(summary.snapshotGeneratedAt)}</code></p>`,
      `<p>Source-hash label: ${this.html.escape(summary.sourceHashTimestampLabel)}</p>`,
      `<p>Counts: artifact_records=${summary.artifactRecordCount}; gate_evaluations=${summary.gateEvaluationCount}; validation_evidence=${summary.validationEvidenceCount}; preview_evidence=${summary.previewEvidenceCount}</p>`,
      `<p>Package source ref: <code>${this.html.escape(summary.packageSourceRef)}</code></p>`,
      `<p>${this.html.escape(summary.hashCaveat)}</p>`,
      `<p>${this.html.escape(summary.refreshProtocolStatement)}</p>`,
      `<p>${this.html.escape(summary.staleHashPackagingRule)}</p>`,
      '<p>Non-authority markers:</p>',
      `<ul>${markers}</ul>`,
      "</article>"
    ].join("");
  }
}
