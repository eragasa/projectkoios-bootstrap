# Python intake analysis candidate

## Lifecycle

**Candidate.** One bounded intake motivated this extraction. Independent reuse
has not yet been established.

## Operating context

The operator may drop LLM-generated Python scripts as examples from which Pi
extracts reusable tools. The drop is not assumed to be a complete patch or a
candidate for direct promotion. This analyzer supplies facts for that
extraction workflow; it does not decide that the dropped implementation should
be preserved.

Git patch comparison is optional and applies only when the operator or current
evidence establishes a patch relationship. Companion changes absent from an
observational drop are context, not automatic findings.

## Purpose

This candidate turns a dropped Python source tree into deterministic review
evidence without importing or executing the dropped code. It provides reusable
helpers for:

- bounded file inventory and SHA-256 identity;
- Python syntax, definition, import, and test discovery;
- local, external, optional, and declared dependency reporting, including
  imports not represented inside the drop;
- conservative static capability signals;
- validation-command planning with execution boundaries shown explicitly;
- read-only comparison with a Git patch, including byte matches and companion
  changes absent from the intake; and
- canonical JSON or concise Markdown reporting.

It supports analysis and coordination. It does not own or reproduce any
component behavior found in an intake. Pi uses the resulting facts to define a
separate reusable contract, route that contract, and build a sanitized
candidate.

## Interface

The library entry points are in
`python/projectkoios/bootstrap/harness/python_intake.py`:

- `analyze_python_intake(root, limits=...)`;
- `compare_intake_to_git_patch(root, repository=..., base_ref=...,
  head_ref=..., limits=...)`; and
- `render_markdown(report)`.

The same module has a command-line interface. Static analysis of an intake:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.python_intake \
  --format markdown analyze \
  python/projectkoios/bootstrap/development/ingestion/intake
```

Read-only comparison with an owning-repository patch:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.python_intake \
  --format markdown compare \
  python/projectkoios/bootstrap/development/ingestion/intake \
  --repository ../projectkoios-ingestion \
  --base-ref origin/master \
  --head-ref origin/feature/v0-ingestor-pilot
```

The analyzer writes only to standard output. Callers decide whether and where to
persist a report.

## Safety and authority

The default limits are:

- 1,000 regular files and 1,000 directories;
- directory depth 64;
- 5,000,000 bytes per file;
- 50,000,000 bytes in total;
- 10,000,000 captured output bytes per read-only Git command; and
- 15 seconds per read-only Git command.

The analyzer rejects symlinked roots, symlinked entries, non-regular entries,
and bound violations. It parses Python with the standard-library AST and does
not import intake modules. Git comparison resolves commits and reads diff and
blob data without checking out, modifying, fetching, or publishing anything.

A generated validation plan is descriptive. The candidate selects pytest only
when it is imported; otherwise it proposes standard-library unittest discovery.
Every test command is marked as executing intake code and is never launched by
this candidate. Running tests or behavioral probes remains a separate, explicit
operation after reviewing trust, dependencies, and isolation.

Reports contain relative intake paths, content hashes, structural metadata, and
Git commit identities. They omit the absolute intake and repository paths. A
caller must still inspect filenames and dependency names before putting a
report in a public record.

Static capability signals are review leads, not security findings. Missing
manifests or companion changes are facts, not automatic defects: an intake may
intentionally be observational rather than a complete patch.

Repository ownership and finding dispositions remain architectural and review
judgments. The helper must not infer authority, move source, open sessions,
modify issues, or classify a component as accepted.

## Determinism and replay

For unchanged files, limits, Python runtime, and Git commits, the returned data
is ordered and deterministic. Reports use relative POSIX paths and SHA-256
identities. The analyzer has no cache, checkpoint, transcript, telemetry, or
persistent runtime state.

## Fixtures and validation

Synthetic fixtures cover a complete package-shaped intake, an optional missing
dependency, a network-capable import signal, and malformed Python. Tests also
construct a temporary Git history to cover an exact copied file, an absent
manifest change, and an absent module-to-package rename.

Run:

```bash
PYTHONPATH=python python3.14 -m unittest discover -s tests -p 'test_*.py'
```

Optional style checks, when Ruff and Mypy are available:

```bash
ruff check python tests
ruff format --check python tests
PYTHONPATH=python mypy python/projectkoios/bootstrap/harness tests/harness
```

## Limitations

- Import-to-distribution matching is name-normalized and cannot resolve every
  packaging alias.
- Static analysis cannot establish runtime behavior, safety, or correctness.
- Capability signals are deliberately conservative and may be incomplete or
  overinclusive.
- Test targets are inferred only from the repository naming convention
  `test__Target__behavior`.
- Git comparison requires explicit base and head references already present in
  the local owning repository. The output-size limit is checked after each Git
  command completes; the timeout does not impose a child-process memory limit.
- The candidate does not construct an isolated execution environment or run
  arbitrary behavioral probes.
- Semantic owner routing and actionable review still require Pi to consult the
  repository map, owner contracts, and current evidence.

## Revisit and extraction criteria

The next lifecycle transition requires an independent intake with materially
different layout or dependencies. Revisit the contract if that use reveals a
recurring need for another bounded static fact. Do not add automatic execution,
dependency installation, workflow state, or semantic owner decisions to solve a
single occurrence.

If independent projects reuse the mechanics without Project Koios policy, the
stable generic analyzer belongs in an explicitly accepted generic Pi-extension
or tooling owner. Project-specific review guidance may remain here.
