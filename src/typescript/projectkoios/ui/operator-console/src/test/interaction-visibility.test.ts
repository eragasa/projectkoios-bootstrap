import { describe, expect, it } from "vitest";
import { InteractionDirection } from "../contracts";
import { OperatorConsoleApplicationFactory } from "../app";
import { InMemoryFixtureProvider } from "../fixtures/provider";
import { FixtureGraphResolver } from "../fixtures/resolver";

const provider: InMemoryFixtureProvider = new InMemoryFixtureProvider(new FixtureGraphResolver());

describe("operator console interaction visibility fixtures", () => {
  it("resolves terminal-originated and console-originated example interactions", () => {
    const readModel = provider.readDashboard();
    const directions: readonly InteractionDirection[] = readModel.interactionThreads.flatMap((thread) =>
      thread.interactions.map((resolved) => resolved.interaction.direction)
    );

    expect(directions).toContain(InteractionDirection.TerminalOriginated);
    expect(directions).toContain(InteractionDirection.ConsoleOriginated);
    expect(readModel.interactionThreads[0]?.interactions).toHaveLength(2);
  });

  it("renders display-only interaction details for user inspection", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();

    expect(html).toContain("Interaction visibility fixture");
    expect(html).toContain(InteractionDirection.TerminalOriginated);
    expect(html).toContain(InteractionDirection.ConsoleOriginated);
    expect(html).toContain("Transcript/read-model locator");
    expect(html).toContain("stale-by-design");
    expect(html).toContain("non-live");
  });
});
