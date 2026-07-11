import type { AgentStatus } from "../contracts";
import { HtmlRenderer } from "./html";

export class AgentSummaryRenderer {
  constructor(private readonly html: HtmlRenderer) {}

  render(agent: AgentStatus): string {
    return [
      '<section class="summary-card" aria-labelledby="agent-summary-title">',
      '<h2 id="agent-summary-title">Agent fixture snapshot</h2>',
      `<p><strong>${this.html.escape(agent.displayName)}</strong> (${this.html.escape(agent.representedRole)})</p>`,
      `<p>Workspace: <code>${this.html.escape(agent.workspace)}</code></p>`,
      `<p>Status: ${this.html.escape(agent.state)}; stale-by-design, not live monitoring.</p>`,
      `<p>${this.html.escape(agent.activitySummary)}</p>`,
      `<p class="meta">Evidence ref: ${this.html.escape(agent.evidenceRefId)}</p>`,
      "</section>"
    ].join("");
  }
}
