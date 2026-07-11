import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { OperatorConsoleApplicationFactory } from "../app";

const packageRoot = new URL("../..", import.meta.url).pathname;
const contractPath = join(packageRoot, "src", "contracts", "index.ts");
const forbiddenOperationWords: readonly RegExp[] = [
  /\bactivate\b/i,
  /\bapply\b/i,
  /\bsave\b/i,
  /\bsend\b/i,
  /\breply\b/i,
  /\bask\b/i
];
const forbiddenInteractiveControlWords: readonly RegExp[] = [
  ...forbiddenOperationWords,
  /\bapprove\b/i,
  /\breject\b/i,
  /\bmutate\b/i
];
const interactiveControlPattern = /<(button|form|input|select|textarea)\b[^>]*>[\s\S]*?<\/(button|form|select|textarea)>|<(input)\b[^>]*>|role="button"[^>]*>/gi;

class InteractiveControlScanner {
  findControls(html: string): readonly string[] {
    return html.match(interactiveControlPattern) ?? [];
  }

  findForbiddenWords(controls: readonly string[]): readonly string[] {
    return controls.flatMap((control: string) =>
      forbiddenInteractiveControlWords
        .filter((pattern: RegExp) => pattern.test(control))
        .map((pattern: RegExp) => String(pattern))
    );
  }
}

describe("operator console mutation-control boundary", () => {
  it("renders no interactive mutation or messaging controls", () => {
    const html: string = new OperatorConsoleApplicationFactory().build().render();
    const scanner: InteractiveControlScanner = new InteractiveControlScanner();
    const controls: readonly string[] = scanner.findControls(html);

    expect(scanner.findForbiddenWords(controls)).toEqual([]);
  });

  it("exposes no send/reply/ask/activate/apply/save operation surfaces in contracts", () => {
    const contractSource: string = readFileSync(contractPath, "utf8");
    const matchedWords: string[] = forbiddenOperationWords
      .filter((pattern: RegExp) => pattern.test(contractSource))
      .map((pattern: RegExp) => String(pattern));

    expect(matchedWords).toEqual([]);
  });
});
