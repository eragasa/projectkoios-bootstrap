import { basename, isAbsolute } from "node:path";

const SESSION_NAME = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}:[a-z0-9][a-z0-9-]{0,63}$/;

function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

export function coordinationViolation(input) {
  if (!input || typeof input !== "object") return undefined;
  if (input.action !== "send" && input.action !== "ask") return undefined;

  if (input.openProjectPaneIfMissing === true) {
    return "Automatic project-pane spawning is disabled; use scripts/open-repository-session so Herdr launches a named Pi session in a labeled tab";
  }
  if (!nonEmptyString(input.cwd) || !isAbsolute(input.cwd.trim())) {
    return "Intercom send/ask requires an explicit absolute repository cwd";
  }
  if (!nonEmptyString(input.to) || !SESSION_NAME.test(input.to.trim())) {
    return "Intercom send/ask requires an exact <repository>:<task> session name";
  }
  const repositoryName = input.to.trim().split(":", 1)[0];
  if (basename(input.cwd.trim()) !== repositoryName) {
    return "Intercom session name and repository cwd do not identify the same repository";
  }
  return undefined;
}

export default function coordinationGuard(pi) {
  pi.on("tool_call", async (event) => {
    if (event.toolName !== "intercom") return undefined;
    const reason = coordinationViolation(event.input);
    return reason ? { block: true, reason } : undefined;
  });
}
