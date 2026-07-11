import { describe, expect, it } from "vitest";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const packageRoot = new URL("../..", import.meta.url).pathname;
const sourceRoot = join(packageRoot, "src");
const fixtureRoot = join(packageRoot, "fixtures");
const forbiddenPatterns: readonly RegExp[] = [
  /\bfetch\s*\(/,
  /\bWebSocket\b/,
  /from\s+["']node:fs["']/,
  /from\s+["']fs["']/,
  /from\s+["']node:child_process["']/,
  /from\s+["']child_process["']/,
  /intercom/i,
  /session\s*import/i
];

class SourceFileCollector {
  collect(directory: string): readonly string[] {
    const entries: string[] = [];
    for (const entryName of readdirSync(directory)) {
      const entryPath: string = join(directory, entryName);
      const entryStatus = statSync(entryPath);
      if (entryStatus.isDirectory()) {
        entries.push(...this.collect(entryPath));
      } else if (entryPath.endsWith(".ts") && !entryPath.includes(`${join("src", "test")}${"/"}`)) {
        entries.push(entryPath);
      }
    }
    return entries;
  }
}

class ForbiddenLivePrimitiveScanner {
  constructor(private readonly collector: SourceFileCollector) {}

  scan(directories: readonly string[]): readonly string[] {
    const scannedFiles: readonly string[] = directories.flatMap((directory: string) => this.collector.collect(directory));
    const violations: string[] = [];
    for (const filePath of scannedFiles) {
      const content: string = readFileSync(filePath, "utf8");
      for (const pattern of forbiddenPatterns) {
        if (pattern.test(content)) {
          violations.push(`${relative(packageRoot, filePath)} matched ${pattern}`);
        }
      }
    }
    return violations;
  }
}

describe("operator console fixture provider live dependency boundary", () => {
  it("keeps browser, provider, and fixture code free of forbidden live primitives", () => {
    const scanner: ForbiddenLivePrimitiveScanner = new ForbiddenLivePrimitiveScanner(new SourceFileCollector());
    const violations: readonly string[] = scanner.scan([sourceRoot, fixtureRoot]);

    expect(violations).toEqual([]);
  });
});
