# Implementation plan 20260704.192620: Python policy validator

## Status

Draft implementation plan for VULCAN execution.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Worktree: `/Users/eugene/repos/projectkoios-bootstrap-schema-record-base`
- Source request: user asked for an implementation plan for building a validator for the Python coding/testing rules
- Source policies: `docs/policies/python-coding.md`, `docs/policies/python-testing.md`
- Previous artifact: user discussion about validating local variable annotations, banning local `Any`, and checking declared return types
- Next expected artifact: implementation brief or direct VULCAN implementation if user approves this plan

## Objective

Build a lightweight repository-local validator that checks the enforceable subset of the Python coding/testing policies before implementation closeout.

The first slice should validate changed or explicitly targeted Python files, report actionable file/line findings, and avoid becoming a broad workflow platform.

## Scope

First slice validates:

1. function and method return annotations exist;
2. function and method return values are statically checked by invoking `mypy` on the target surface;
3. local variables introduced inside functions/methods have explicit annotations;
4. local variable annotations inside functions/methods do not use `Any`;
5. focused test/static-validation commands can be run and summarized for implementation reports.

## Non-goals

Do not add in the first slice:

- full CI integration;
- automatic code rewriting;
- whole-repo mandatory enforcement without an explicit `--all` flag;
- architecture or product policy validation;
- non-Python validation;
- type inference beyond Python AST and mypy output;
- historical remediation of all existing violations unless explicitly requested.

## Proposed package boundary

Use bootstrap tooling, not GraphRAG or ingestor modules:

```text
src/python/projectkoios/bootstrap/python_policy/
  __init__.py
  ast_rules.py
  targets.py
  validator.py
  mypy_runner.py
```

Optional CLI integration after core tests pass:

```text
src/python/projectkoios/bootstrap/commands/validate_python_policy.py
```

If the CLI command registry requires a different file shape, document it in the implementation report.

## Rule model

Create small data objects:

- `PolicyFinding`
  - `path: Path`
  - `line: int`
  - `column: int`
  - `rule_id: str`
  - `message: str`
- `ValidationTarget`
  - `path: Path`
  - `source: str` such as `changed`, `explicit`, or `all`
- `ValidationResult`
  - `findings: tuple[PolicyFinding, ...]`
  - `mypy_exit_code: int | None`
  - `mypy_output: str | None`

Suggested rule IDs:

- `PY-POLICY-001`: function or method missing return annotation
- `PY-POLICY-002`: local variable introduced without annotation
- `PY-POLICY-003`: local variable annotation uses `Any`
- `PY-POLICY-004`: static type checker failed

## AST rule behavior

### Return annotations

For every `ast.FunctionDef` and `ast.AsyncFunctionDef` under targeted files:

- require `returns` unless the function is a special case explicitly documented by policy;
- treat methods and nested functions the same in the first slice;
- report the function definition line.

Open implementation choice: whether `__init__` may omit `-> None`. Recommendation for first slice: require `-> None` for `__init__` too, because the policy says function and method return values must be declared and checked.

### Local variable annotations

Inside each function/method body, detect introduced names from:

- `ast.Assign`
- `ast.AnnAssign`
- `ast.AugAssign`
- `ast.For` / `ast.AsyncFor` targets
- `ast.With` / `ast.AsyncWith` optional vars
- `ast.ExceptHandler` exception aliases
- assignment expressions (`ast.NamedExpr`)

First-slice policy:

- `ast.AnnAssign` satisfies the annotation rule for its target name;
- plain `ast.Assign`, loop targets, `with/as`, exception aliases, and assignment expressions are findings unless a prior annotation for the same local name exists earlier in the same function;
- tuple/list destructuring is allowed only when every introduced name already has a prior annotation, or when using separate annotated assignment before destructuring;
- ignore `self` and `cls` parameters because they are parameters, not local variable introductions;
- do not flag function parameters in this rule because parameter annotation policy can be added later.

### Ban local `Any`

For `ast.AnnAssign` inside functions/methods:

- reject annotation name `Any`;
- reject attribute annotation ending in `.Any`, such as `typing.Any`;
- reject string annotations equal to `Any` or containing a simple `typing.Any` reference;
- reject subscript annotations containing `Any`, such as `dict[str, Any]`, `Mapping[str, Any]`, `list[Any]`.

First-slice limitation: implicit Any from third-party stubs is left to mypy and is not an AST finding.

## Target selection

Support target modes:

1. `--paths <path>...`
   - Validate explicit Python files or directories.
2. `--changed`
   - Validate Python files changed relative to `HEAD` by default.
   - Include staged and unstaged changes.
3. `--all`
   - Validate all Python files under `src/python/` and optionally `tests/`.

Default recommendation: `--changed` to avoid noisy historical enforcement.

Target rules:

- Include `.py` files only.
- Exclude virtualenvs, `__pycache__`, build artifacts, and generated files.
- Resolve paths relative to repo root.

## Mypy integration

Add a runner that invokes:

```bash
python -m mypy <targets>
```

or, when using uv:

```bash
uv run mypy <targets>
```

Implementation should prefer `sys.executable -m mypy` inside the active environment when possible, with a clear error if mypy is unavailable.

Behavior:

- AST policy findings and mypy failures should both produce non-zero validation status.
- Capture mypy stdout/stderr for implementation reports.
- Do not parse mypy output into per-rule findings in the first slice unless trivial.

## CLI behavior

Proposed command:

```bash
projectkoios bootstrap validate-python-policy --changed
projectkoios bootstrap validate-python-policy --paths src/python/projectkoios/bootstrap/schemas tests/projectkoios/bootstrap/schemas
projectkoios bootstrap validate-python-policy --all
```

Output should be concise:

```text
PY-POLICY-002 src/python/example.py:12:4 local variable 'result' must have an explicit annotation
PY-POLICY-004 mypy failed with exit code 1
python-policy=False findings=2 mypy_exit=1
```

Exit codes:

- `0`: no findings and mypy passed or was not requested by explicit flag;
- `1`: policy findings or mypy failures;
- `2`: validator configuration/usage error.

## Test plan

Add tests under:

```text
tests/projectkoios/bootstrap/python_policy/
```

Required tests:

### AST rule tests

- accepts function/method with return annotation and annotated locals;
- rejects missing function return annotation;
- rejects plain local assignment without prior annotation;
- accepts plain reassignment after prior local annotation;
- rejects loop target without prior annotation;
- rejects `with/as` target without prior annotation;
- rejects exception alias without prior annotation;
- rejects assignment expression introducing an unannotated name;
- rejects local `Any` as `Any`;
- rejects local `Any` as `typing.Any`;
- rejects nested `Any` such as `Mapping[str, Any]`.

### Target selection tests

- explicit file target includes only `.py` files;
- directory target recurses into Python files;
- generated/cache/venv paths are excluded;
- changed-file mode can be tested through a small fake git adapter or isolated helper rather than depending on repository state.

### Mypy runner tests

- successful command returns exit code 0 and captured output;
- failed command returns non-zero and captured output;
- missing mypy produces actionable validator error.

### CLI tests, if CLI is included

- no findings exits 0;
- policy finding exits 1 and prints file/line/rule;
- bad arguments exit 2.

## Validation commands for implementation report

Minimum:

```bash
uv run pytest tests/projectkoios/bootstrap/python_policy -q
uv run pytest -q
uv run mypy src/python/projectkoios/bootstrap/python_policy
```

If CLI integration is included:

```bash
uv run projectkoios bootstrap validate-python-policy --paths src/python/projectkoios/bootstrap/python_policy tests/projectkoios/bootstrap/python_policy
```

## Risks and mitigations

- Existing code may violate new rules heavily.
  - Mitigation: default to `--changed` and support explicit `--paths`; defer whole-repo enforcement.
- Local variable annotation policy is stricter than common Python style.
  - Mitigation: make findings precise and actionable; document edge cases in tests.
- `Any` can enter through aliases or imports.
  - Mitigation: first slice catches direct/nested AST-visible `Any`; leave alias analysis to a later slice.
- Mypy availability may vary across worktrees.
  - Mitigation: use the dev dependency group and emit an actionable error when unavailable.
- AST checks can be noisy for destructuring/comprehensions.
  - Mitigation: define first-slice behavior explicitly and add tests before broad enforcement.

## Acceptance criteria

- A developer can run the validator against explicit paths and changed files.
- The validator reports file, line, column, rule ID, and message for policy violations.
- Missing return annotations are detected.
- Unannotated local variable introductions are detected for the first-slice AST node set.
- Local variable annotations using direct or nested `Any` are detected.
- Static type checking can be invoked and its success/failure recorded.
- Tests cover accepted and rejected cases for each first-slice rule.
- Implementation report records validation output and any deferred edge cases.

## Next expected artifact

If accepted, the next artifact should be either:

- `docs/plans/implementation-brief.<timestamp>_python-policy-validator.md`, if ATHENA/user wants a formal brief; or
- a VULCAN implementation report after direct implementation from this plan, if the user authorizes implementation.
