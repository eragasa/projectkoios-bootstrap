import type { DashboardReadModel } from "./contracts";
import { AgentSummaryRenderer } from "./components/AgentSummary";
import { ChangeReviewRenderer } from "./components/ChangeReview";
import { EvidencePanelRenderer } from "./components/EvidencePanel";
import { ExternalStatusCardRenderer } from "./components/ExternalStatusCard";
import { HtmlRenderer } from "./components/html";
import { ValidationSummaryRenderer } from "./components/ValidationSummary";
import { InMemoryFixtureProvider } from "./fixtures/provider";
import { FixtureGraphResolver } from "./fixtures/resolver";

export class OperatorConsoleRenderer {
  constructor(
    private readonly agentSummaryRenderer: AgentSummaryRenderer,
    private readonly externalStatusCardRenderer: ExternalStatusCardRenderer,
    private readonly changeReviewRenderer: ChangeReviewRenderer
  ) {}

  render(readModel: DashboardReadModel): string {
    const agentCards: string = readModel.agentStatuses.map((agent) => this.agentSummaryRenderer.render(agent)).join("");
    const externalCards: string = readModel.externalStatuses
      .map((status) => this.externalStatusCardRenderer.render(status))
      .join("");
    return [
      '<div class="operator-console">',
      '<header class="banner">',
      '<p class="eyebrow">Project Koios Operator Console incubation</p>',
      '<h1>Review one proposal fixture</h1>',
      '<p>This browser surface is fixture-backed, static, stale-by-design, and non-authoritative. It is not live Project Koios operational state.</p>',
      "</header>",
      '<section class="summary-grid" aria-label="Fixture context summaries">',
      agentCards,
      externalCards,
      "</section>",
      this.changeReviewRenderer.render(readModel.primaryProposal),
      "</div>"
    ].join("");
  }
}

export class OperatorConsoleApplication {
  constructor(
    private readonly provider: InMemoryFixtureProvider,
    private readonly renderer: OperatorConsoleRenderer
  ) {}

  render(): string {
    const fixtureProblems: readonly string[] = this.provider.validateFixtures();
    if (fixtureProblems.length > 0) {
      throw new Error(`Invalid operator console fixtures: ${fixtureProblems.join("; ")}`);
    }
    return this.renderer.render(this.provider.readDashboard());
  }
}

export class OperatorConsoleApplicationFactory {
  build(): OperatorConsoleApplication {
    const htmlRenderer: HtmlRenderer = new HtmlRenderer();
    const validationSummaryRenderer: ValidationSummaryRenderer = new ValidationSummaryRenderer(htmlRenderer);
    const evidencePanelRenderer: EvidencePanelRenderer = new EvidencePanelRenderer(
      htmlRenderer,
      validationSummaryRenderer
    );
    const renderer: OperatorConsoleRenderer = new OperatorConsoleRenderer(
      new AgentSummaryRenderer(htmlRenderer),
      new ExternalStatusCardRenderer(htmlRenderer),
      new ChangeReviewRenderer(htmlRenderer, evidencePanelRenderer)
    );
    const provider: InMemoryFixtureProvider = new InMemoryFixtureProvider(new FixtureGraphResolver());
    return new OperatorConsoleApplication(provider, renderer);
  }
}
