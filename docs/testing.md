# Testing strategy

## Directory structure

Tests under `tests/` mirror the source package layout. Each module under
`src/python/projectkoios/` has a corresponding module under `tests/`.

Example:

```
src/python/projectkoios/bootstrap/harness/data/artifact.py
  → tests/harness/data/__ArtifactToken__from_header__parses_yaml_frontmatter.py
```

## Naming convention

```
File:      __ClassName__method_name__testdesc.py
Function:  test__ClassName__method_name__testdesc()
```

The file and function names are identical except the function is prefixed
with `def test_`.

Examples:

| File | Function |
|------|----------|
| `__HandoffParser__parse_header__parses_yaml_frontmatter.py` | `test__HandoffParser__parse_header__parses_yaml_frontmatter()` |
| `__Guards__hermes_forwarded_without_decision__checks_raw_role_state.py` | `test__Guards__hermes_forwarded_without_decision__unknown_kind_in_pi_place_is_violation()` |
| `__ViolationAppender__append_to_file__appends_violation_block.py` | `test__ViolationAppender__append_to_file__appends_violation_block()` |

## Fixtures

- Use `tmp_path` for file I/O tests.
- Handoff fixture files are created inline or via helper factories placed
  alongside the test or in `tests/conftest.py` if shared.

## What to test

- Public API of each DataObject (construction, validation, representation)
- Each guard predicate (pass and fail cases)
- ActionObjects (happy path and violation path)
- CLI registration and output
