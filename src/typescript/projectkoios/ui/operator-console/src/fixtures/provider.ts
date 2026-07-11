import type { DashboardReadModel } from "../contracts";
import { FixtureGraphResolver } from "./resolver";

export interface OperatorConsoleProvider {
  readDashboard(): DashboardReadModel;
  validateFixtures(): readonly string[];
}

export class InMemoryFixtureProvider implements OperatorConsoleProvider {
  constructor(private readonly resolver: FixtureGraphResolver) {}

  readDashboard(): DashboardReadModel {
    return this.resolver.buildDashboardReadModel();
  }

  validateFixtures(): readonly string[] {
    return this.resolver.validateFixtureGraph();
  }
}
