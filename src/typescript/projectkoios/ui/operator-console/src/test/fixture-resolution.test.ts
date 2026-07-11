import { describe, expect, it } from "vitest";
import { HashLabel } from "../contracts";
import { InMemoryFixtureProvider } from "../fixtures/provider";
import { FixtureGraphResolver } from "../fixtures/resolver";

const provider: InMemoryFixtureProvider = new InMemoryFixtureProvider(new FixtureGraphResolver());

describe("operator console fixture resolution", () => {
  it("resolves the first proposal current, proposed, evidence, and validation refs", () => {
    const problems: readonly string[] = provider.validateFixtures();
    const readModel = provider.readDashboard();

    expect(problems).toEqual([]);
    expect(readModel.primaryProposal.current.ref.id).toBe("content.current.adr-json-schemas-draft");
    expect(readModel.primaryProposal.proposed.ref.id).toBe("content.proposed.adr-json-schemas-json");
    expect(readModel.primaryProposal.evidence.length).toBeGreaterThanOrEqual(4);
    expect(readModel.primaryProposal.validations).toHaveLength(1);
    expect(readModel.primaryProposal.current.ref.hashLabel).toBe(HashLabel.FixtureSourceIdentityHash);
    expect(readModel.primaryProposal.proposed.ref.hashLabel).toBe(HashLabel.FixtureSourceIdentityHash);
  });
});
