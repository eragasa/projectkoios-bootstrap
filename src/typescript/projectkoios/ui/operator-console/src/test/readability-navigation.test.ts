import { describe, expect, it } from "vitest";
import { OperatorConsoleApplicationFactory } from "../app";

describe("operator console readability navigation fixture", () => {
  it("renders major-section jump links for fixture inspection", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain('aria-label="Readability-only local navigation for fixture preview"');
    expect(html).toContain('href="#fixture-summaries"');
    expect(html).toContain('href="#interaction-panel-title"');
    expect(html).toContain('href="#review-current"');
    expect(html).toContain('href="#review-proposed"');
    expect(html).toContain('href="#review-evidence"');
  });

  it("renders local-only collapsible and scrollable readability affordances", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain('<details class="interaction-card readable-card');
    expect(html).toContain('<details class="evidence-item readable-card" open>');
    expect(html).toContain('local readability-only UI');
    expect(html).toContain('class="scroll-region"');
    expect(html).toContain('class="scroll-region interaction-scroll"');
    expect(html).toContain('class="scroll-region evidence-scroll"');
  });

  it("keeps highlighted interaction cards as fixture visual emphasis", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain('interaction-card--terminal-originated');
    expect(html).toContain('interaction-card--console-originated');
    expect(html).toContain('highlighted cards are fixture visual emphasis only');
  });
});
