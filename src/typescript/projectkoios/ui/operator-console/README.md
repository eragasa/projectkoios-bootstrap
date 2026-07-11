# Project Koios Operator Console incubation

This package is a bootstrap-incubated P0 browser/TypeScript slice for the future Project Koios Operator Console.

Canonical architecture/spec authority lives at:

- `docs/architecture/architecture.operator-console.md`

This package is not product UI authority and is not a production backend. The extraction target remains:

- `projectkoios/ui/operator-console/`

## P0 scope

P0 is `operator-console-review-one-proposal-fixture`:

- Vite + vanilla TypeScript + Vitest;
- deterministic fixture provider/resolver;
- one fixture-backed proposal review for the completed `adr.json-schemas` conformance slice;
- user-facing panels: `What changed?`, `What is proposed?`, `Why trust this evidence?`;
- visible incubation/static/stale-by-design warning;
- no live intercom/session/network/repo-state reads;
- no backend service;
- no workflow mutation or Petri-net graph editor.

## Commands

Run from this package directory:

```bash
npm install
npm run typecheck
npm test
npm run build
```

## Fixture policy

Fixtures are copied or transformed from bootstrap artifacts before browser runtime. Browser/provider code imports fixture data and does not read repository files at runtime.

Every fixture source records:

- locator/path;
- artifact type;
- source/content hash;
- captured/generated timestamp;
- transformation or excerpt notes;
- authority boundary.

Current/proposed hashes are fixture/source identity hashes, not canonical product authority.

## Build output policy

Do not commit:

- `node_modules/`
- `dist/`
- `coverage/`
- Vite local cache or preview state
- local sessions, live snapshots, secrets, or screenshots unless explicitly approved
