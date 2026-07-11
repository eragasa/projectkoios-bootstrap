import type { ExternalSystemStatus } from "../contracts";
import { HtmlRenderer } from "./html";

export class ExternalStatusCardRenderer {
  constructor(private readonly html: HtmlRenderer) {}

  render(status: ExternalSystemStatus): string {
    return [
      '<section class="summary-card" aria-labelledby="external-status-title">',
      '<h2 id="external-status-title">External status fixture snapshot</h2>',
      `<p><strong>${this.html.escape(status.displayName)}</strong></p>`,
      `<p>Status class: ${this.html.escape(status.statusClass)}; fixture/static/stale-by-design.</p>`,
      `<p>Last copied into fixture: ${this.html.escape(status.lastChecked)}</p>`,
      `<p>${this.html.escape(status.summary)}</p>`,
      `<p class="meta">Evidence refs: ${this.html.escape(status.evidenceRefIds.join(", "))}</p>`,
      "</section>"
    ].join("");
  }
}
