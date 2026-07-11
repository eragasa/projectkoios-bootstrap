import { describe, expect, it } from "vitest";
import { OperatorConsoleApplicationFactory } from "../app";

describe("operator console current implementation review fixture", () => {
  it("renders the current implementation review static snapshot panel", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain("Current implementation review static snapshot");
    expect(html).toContain("Static snapshot; not live; stale-by-design until refreshed");
    expect(html).toContain("Operator Console P0 review-one-proposal fixture");
    expect(html).toContain("Operator Console ActionObject/DataObject refactor");
    expect(html).toContain("Operator Console P1 interaction visibility");
    expect(html).toContain("Operator Console P2 readability/navigation fixture");
    expect(html).toContain("Workflow-object Slice 0 static Operator Console record");
  });

  it("renders workflow-object summary counts and the single package source ref", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain("workflow-object.operator-console-bootstrap-bundle.20260711");
    expect(html).toContain("artifact_records=9");
    expect(html).toContain("gate_evaluations=3");
    expect(html).toContain("validation_evidence=1");
    expect(html).toContain("preview_evidence=1");
    expect(html).toContain("src/typescript/projectkoios/ui/operator-console/package.json");
  });

  it("renders static snapshot authority and refresh caveats", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain("Hashes identify the referenced working-tree file contents at fixture generation time");
    expect(html).toContain("This screen is a static snapshot, not live operational truth");
    expect(html).toContain("may be stale until intentionally refreshed");
    expect(html).toContain("Workflow-object refresh protocol is not yet defined");
    expect(html).toContain("static-record");
    expect(html).toContain("not-product-authority");
  });
});
