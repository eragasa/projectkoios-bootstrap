import type { ValidationFinding, ValidationResult } from "../contracts";
import { HtmlRenderer } from "./html";

export class ValidationSummaryRenderer {
  constructor(private readonly html: HtmlRenderer) {}

  render(validations: readonly ValidationResult[]): string {
    const validationBlocks: string = validations
      .map((validation: ValidationResult) => this.renderValidation(validation))
      .join("");
    return `<section class="validation-summary"><h3>Validation evidence</h3>${validationBlocks}</section>`;
  }

  private renderValidation(validation: ValidationResult): string {
    const findingMessages: readonly string[] = validation.findings.map(
      (finding: ValidationFinding) => `${finding.level}: ${finding.message}`
    );
    return [
      '<article class="validation-result">',
      `<h4>${this.html.escape(validation.id)}</h4>`,
      `<p>Status: <strong>${this.html.escape(validation.status)}</strong>; category: ${this.html.escape(validation.category)}</p>`,
      `<p>${this.html.escape(validation.commandSummary)}</p>`,
      '<p class="meta">Console reran commands: false. Outcomes are copied fixture evidence.</p>',
      this.html.renderList(findingMessages),
      "</article>"
    ].join("");
  }
}
