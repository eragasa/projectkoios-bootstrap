import assert from "node:assert/strict";
import test from "node:test";

import coordinationGuard, {
  coordinationViolation,
} from "../../.pi/extensions/coordination-guard.js";

test("allows exact named and cwd-scoped sends", () => {
  assert.equal(
    coordinationViolation({
      action: "send",
      to: "projectkoios-example:task",
      cwd: "/repos/projectkoios-example",
      message: "work",
    }),
    undefined,
  );
});

test("blocks automatic pane spawning", () => {
  assert.match(
    coordinationViolation({
      action: "send",
      to: "projectkoios-example:task",
      cwd: "/repos/projectkoios-example",
      openProjectPaneIfMissing: true,
    }),
    /Automatic project-pane spawning is disabled/,
  );
});

test("blocks sends and asks without absolute cwd and structured name", () => {
  assert.match(
    coordinationViolation({ action: "send", to: "projectkoios-example:task" }),
    /absolute repository cwd/,
  );
  assert.match(
    coordinationViolation({ action: "ask", cwd: "/repos/projectkoios-example" }),
    /<repository>:<task>/,
  );
  assert.match(
    coordinationViolation({ action: "send", cwd: ".", to: "projectkoios-example:task" }),
    /absolute repository cwd/,
  );
  assert.match(
    coordinationViolation({ action: "ask", cwd: "/repos/projectkoios-example", to: "worker" }),
    /<repository>:<task>/,
  );
});

test("blocks unnamed runtime fallback aliases", () => {
  assert.match(
    coordinationViolation({
      action: "send",
      cwd: "/repos/projectkoios-example",
      to: "subagent-chat-01a0e1ac-f4f6-70e0",
    }),
    /<repository>:<task>/,
  );
});

test("blocks a session name that disagrees with the cwd", () => {
  assert.match(
    coordinationViolation({
      action: "send",
      cwd: "/repos/projectkoios-example",
      to: "projectkoios-other:task",
    }),
    /do not identify the same repository/,
  );
});

test("does not interfere with non-delivery actions or other tools", async () => {
  assert.equal(coordinationViolation({ action: "list-cwd" }), undefined);

  let handler;
  coordinationGuard({
    on(event, callback) {
      assert.equal(event, "tool_call");
      handler = callback;
    },
  });

  assert.equal(await handler({ toolName: "read", input: {} }), undefined);
  assert.equal(
    await handler({ toolName: "intercom", input: { action: "status" } }),
    undefined,
  );
});

test("registered handler blocks invalid intercom delivery", async () => {
  let handler;
  coordinationGuard({
    on(_event, callback) {
      handler = callback;
    },
  });

  assert.deepEqual(
    await handler({
      toolName: "intercom",
      input: { action: "send", to: "projectkoios-example:task" },
    }),
    {
      block: true,
      reason: "Intercom send/ask requires an explicit absolute repository cwd",
    },
  );
});
