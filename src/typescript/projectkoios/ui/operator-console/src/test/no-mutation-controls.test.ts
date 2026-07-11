import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { OperatorConsoleApplicationFactory } from "../app";

const packageRoot = new URL("../..", import.meta.url).pathname;
const contractPath = join(packageRoot, "src", "contracts", "index.ts");
const forbiddenControlWords: readonly RegExp[] = [/\bactivate\b/i, /\bapply\b/i, /\bsave\b/i];

describe("operator console P0 mutation-control boundary", () => {
  it("renders no activate/apply/save controls or availability text", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();
    const matchedWords: string[] = forbiddenControlWords
      .filter((pattern: RegExp) => pattern.test(html))
      .map((pattern: RegExp) => String(pattern));

    expect(matchedWords).toEqual([]);
  });

  it("exposes no activate/apply/save operation surfaces in contracts", () => {
    const contractSource: string = readFileSync(contractPath, "utf8");
    const matchedWords: string[] = forbiddenControlWords
      .filter((pattern: RegExp) => pattern.test(contractSource))
      .map((pattern: RegExp) => String(pattern));

    expect(matchedWords).toEqual([]);
  });
});
