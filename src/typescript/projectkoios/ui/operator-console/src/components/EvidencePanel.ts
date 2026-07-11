import type { EvidenceRef, ValidationResult } from "../contracts";
import { HtmlRenderer } from "./html";
import { ValidationSummaryRenderer } from "./ValidationSummary";

export class EvidencePanelRenderer {
  constructor(
    private readonly html: HtmlRenderer,
    private readonly validationSummaryRenderer: ValidationSummaryRenderer
  ) {}

  render(evidence: readonly EvidenceRef[], validations: readonly ValidationResult[]): string {
    const evidenceItems: string = evidence.map((item: EvidenceRef) => this.renderEvidenceItem(item)).join("");
    return [
      '<section class="evidence-panel">',
      '<h3>Why trust this evidence?</h3>',
      '<p class="notice">This panel displays copied or transformed fixture evidence. The console does not rerun commands or read repository files at runtime.</p>',
      this.validationSummaryRenderer.render(validations),
      evidenceItems,
      "</section>"
    ].join("");
  }

  private renderEvidenceItem(evidence: EvidenceRef): string {
    return [
      '<article class="evidence-item">',
      `<h4>${this.html.escape(evidence.title)}</h4>`,
      `<p>Kind: ${this.html.escape(evidence.kind)}; displayed as: ${this.html.escape(evidence.displayedAs)}</p>`,
      `<p>Source locator: <code>${this.html.escape(evidence.locator)}</code></p>`,
      `<p>Source/content hash: <code>${this.html.escape(evidence.contentHash)}</code></p>`,
      `<p>${this.html.escape(evidence.summary)}</p>`,
      `<p>Captured: ${this.html.escape(evidence.metadata.capturedAt)}; ${this.html.escape(evidence.metadata.freshness)}</p>`,
      `<p>Authority boundary: ${this.html.escape(evidence.metadata.authorityBoundary.join(", "))}</p>`,
      `<p>Transformation notes: ${this.html.escape(evidence.metadata.transformationNotes)}</p>`,
      `<p>Trust explanation: ${this.html.escape(evidence.metadata.trustExplanation)}</p>`,
      "</article>"
    ].join("");
  }
}
