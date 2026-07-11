import type { DashboardReadModel } from "./contracts";
import { AgentSummaryRenderer } from "./components/AgentSummary";
import { ChangeReviewRenderer } from "./components/ChangeReview";
import { EvidencePanelRenderer } from "./components/EvidencePanel";
import { ExternalStatusCardRenderer } from "./components/ExternalStatusCard";
import { HtmlRenderer } from "./components/html";
import { InteractionThreadPanelRenderer } from "./components/InteractionThreadPanel";
import { ValidationSummaryRenderer } from "./components/ValidationSummary";
import { InMemoryFixtureProvider } from "./fixtures/provider";
import { FixtureGraphResolver } from "./fixtures/resolver";

export class OperatorConsoleRenderer {
  constructor(
    private readonly agentSummaryRenderer: AgentSummaryRenderer,
    private readonly externalStatusCardRenderer: ExternalStatusCardRenderer,
    private readonly interactionThreadPanelRenderer: InteractionThreadPanelRenderer,
    private readonly changeReviewRenderer: ChangeReviewRenderer
  ) {}

  render(readModel: DashboardReadModel): string {
    const agentCards: string = readModel.agentStatuses.map((agent) => this.agentSummaryRenderer.render(agent)).join("");
    const externalCards: string = readModel.externalStatuses
      .map((status) => this.externalStatusCardRenderer.render(status))
      .join("");
    return [
      '<div class="operator-console">',
      '<header class="banner" id="console-context">',
      '<p class="eyebrow">Project Koios Operator Console incubation</p>',
      '<h1>Review one proposal fixture</h1>',
      '<p>This browser surface is fixture-backed, static, stale-by-design, and non-authoritative. It is not live Project Koios operational state.</p>',
      "</header>",
      '<nav class="console-nav" aria-label="Readability-only local navigation for fixture preview">',
      '<span>Fixture preview navigation:</span>',
      '<a href="#console-context">Context</a>',
      '<a href="#fixture-summaries">Summary</a>',
      '<a href="#interaction-panel-title">Interactions</a>',
      '<a href="#review-current">Current</a>',
      '<a href="#review-proposed">Proposed</a>',
      '<a href="#review-evidence">Evidence</a>',
      "</nav>",
      '<section class="summary-grid" id="fixture-summaries" aria-label="Fixture context summaries">',
      agentCards,
      externalCards,
      "</section>",
      this.interactionThreadPanelRenderer.render(readModel.interactionThreads),
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
      new InteractionThreadPanelRenderer(htmlRenderer),
      new ChangeReviewRenderer(htmlRenderer, evidencePanelRenderer)
    );
    const provider: InMemoryFixtureProvider = new InMemoryFixtureProvider(new FixtureGraphResolver());
    return new OperatorConsoleApplication(provider, renderer);
  }
}
