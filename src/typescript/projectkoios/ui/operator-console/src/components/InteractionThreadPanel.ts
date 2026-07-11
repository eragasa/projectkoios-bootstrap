import type { ResolvedAgentInteraction, ResolvedAgentThread } from "../contracts";
import { HtmlRenderer } from "./html";

export class InteractionThreadPanelRenderer {
  constructor(private readonly html: HtmlRenderer) {}

  render(threads: readonly ResolvedAgentThread[]): string {
    const threadPanels: string = threads.map((thread: ResolvedAgentThread) => this.renderThread(thread)).join("");
    return [
      '<section class="interaction-panel" aria-labelledby="interaction-panel-title">',
      '<h2 id="interaction-panel-title">Interaction visibility fixture</h2>',
      '<p class="notice">Display-only fixture interactions. Static, stale-by-design, non-live, and outbound messaging features are absent.</p>',
      '<p class="notice">Expandable interaction cards are local readability-only UI for inspection; highlighted cards are fixture visual emphasis only.</p>',
      threadPanels,
      "</section>"
    ].join("");
  }

  private renderThread(thread: ResolvedAgentThread): string {
    const interactions: string = thread.interactions
      .map((interaction: ResolvedAgentInteraction) => this.renderInteraction(interaction))
      .join("");
    return [
      '<article class="interaction-thread">',
      `<h3>${this.html.escape(thread.thread.title)}</h3>`,
      `<p>${this.html.escape(thread.thread.summary)}</p>`,
      `<p>Session id: <code>${this.html.escape(thread.thread.sessionId)}</code>; role: ${this.html.escape(thread.thread.representedRole)}</p>`,
      `<p>Authority boundary: ${this.html.escape(thread.thread.metadata.authorityBoundary.join(", "))}</p>`,
      interactions,
      "</article>"
    ].join("");
  }

  private renderInteraction(resolved: ResolvedAgentInteraction): string {
    return [
      `<details class="interaction-card readable-card interaction-card--${this.html.escape(resolved.interaction.direction)}" open>`,
      `<summary>${this.html.escape(resolved.interaction.direction)} interaction <span>local readability-only UI</span></summary>`,
      '<div class="scroll-region interaction-scroll" tabindex="0" aria-label="Scrollable fixture interaction content">',
      `<p>Source surface: ${this.html.escape(resolved.interaction.surface)}</p>`,
      `<p>Session id: <code>${this.html.escape(resolved.interaction.sessionId)}</code></p>`,
      `<p>Role identity: ${this.html.escape(resolved.interaction.representedRole)}</p>`,
      `<p>Timestamp: ${this.html.escape(resolved.interaction.timestamp)}</p>`,
      `<p>Delivery/status: ${this.html.escape(resolved.interaction.deliveryStatus)}</p>`,
      `<p>Summary: ${this.html.escape(resolved.interaction.summary)}</p>`,
      `<p>Body: ${this.html.escape(resolved.message.body)}</p>`,
      `<p>Transcript/read-model locator: <code>${this.html.escape(resolved.interaction.transcriptLocator)}</code></p>`,
      `<p>Evidence: ${this.html.escape(resolved.evidence.title)} (${this.html.escape(resolved.evidence.displayedAs)})</p>`,
      `<p>Provenance: ${this.html.escape(resolved.interaction.metadata.provenanceSummary)}</p>`,
      `<p>Freshness: ${this.html.escape(resolved.interaction.metadata.freshness)}</p>`,
      "</div>",
      "</details>"
    ].join("");
  }
}
