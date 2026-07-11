import type { ResolvedChangeProposal } from "../contracts";
import { EvidencePanelRenderer } from "./EvidencePanel";
import { HtmlRenderer } from "./html";

export class ChangeReviewRenderer {
  constructor(
    private readonly html: HtmlRenderer,
    private readonly evidencePanelRenderer: EvidencePanelRenderer
  ) {}

  render(resolved: ResolvedChangeProposal): string {
    return [
      '<section class="change-review" aria-labelledby="change-review-title">',
      '<div class="proposal-heading">',
      '<h2 id="change-review-title">Primary proposal review</h2>',
      `<h3>${this.html.escape(resolved.proposal.title)}</h3>`,
      `<p>${this.html.escape(resolved.proposal.summary)}</p>`,
      `<p class="notice">Review-only fixture: ${this.html.escape(resolved.proposal.mutationUnavailableReason)}</p>`,
      "</div>",
      '<div class="review-grid">',
      this.renderContentPanel(
        "review-current",
        "What changed?",
        resolved.current.body,
        resolved.current.ref.locator,
        resolved.current.ref.contentHash
      ),
      this.renderContentPanel(
        "review-proposed",
        "What is proposed?",
        resolved.proposed.body,
        resolved.proposed.ref.locator,
        resolved.proposed.ref.contentHash
      ),
      this.evidencePanelRenderer.render(resolved.evidence, resolved.validations),
      "</div>",
      "</section>"
    ].join("");
  }

  private renderContentPanel(sectionId: string, heading: string, body: string, locator: string, hash: string): string {
    return [
      `<section class="review-panel" id="${this.html.escape(sectionId)}">`,
      `<h3>${this.html.escape(heading)}</h3>`,
      `<p>Source locator: <code>${this.html.escape(locator)}</code></p>`,
      `<p>Fixture/source identity hash: <code>${this.html.escape(hash)}</code></p>`,
      '<div class="scroll-region" tabindex="0" aria-label="Scrollable fixture review content">',
      `<pre>${this.html.escape(body)}</pre>`,
      "</div>",
      "</section>"
    ].join("");
  }
}
