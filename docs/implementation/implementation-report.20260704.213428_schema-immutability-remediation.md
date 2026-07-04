# Implementation report 20260704.213428: Schema immutability remediation

## Status

Implementation complete; ready for ATHENA gap-closure review.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Branch: master
- Source review: `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md`
- Source implementation report: `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`
- Follow-up gap: shallow immutability in metadata/generic mappings
- Previous artifact: ATHENA conformance review outcome `conforms-with-gaps`
- Next expected artifact: ATHENA gap-closure or updated conformance review

## Summary

Remediated the shallow immutability gap found by ATHENA in the schema-record base slice.

Changed files:

- `src/python/projectkoios/bootstrap/schema/models.py`
  - Replaced shallow `MappingProxyType(dict(value))` freezing with recursive JSON-like freezing.
  - Added `freeze_json_value` to recursively convert mappings to `MappingProxyType` and lists/tuples to tuples.
  - Added `thaw_json_value` and `mutable_json_object` so `to_dict()` returns mutable JSON-compatible copies without exposing internal frozen structures.
  - Updated `RecordMetadata.to_dict()` and `SchemaRecordBase.to_dict()` to return deep mutable copies.
- `tests/projectkoios/bootstrap/schema/test__DraftAdrRecord__markdown.py`
  - Added tests proving source mutations after construction do not affect record metadata.
  - Added tests proving nested metadata mappings exposed through `RecordMetadata.fields` are immutable.
  - Added tests proving `to_dict()` returns deep mutable copies that can be modified without changing the record.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap`:

```bash
uv run pytest tests/projectkoios/bootstrap/schema -q
```

Result:

```text
19 passed in 0.13s
```

Static type checking:

```bash
uv run mypy src/python/projectkoios/bootstrap/schema
```

Result:

```text
Success: no issues found in 5 source files
```

Python policy validation:

```bash
uv run python - <<'PY'
from pathlib import Path
from projectkoios.bootstrap.python_policy import PythonPolicyValidator, TargetSelector
result=PythonPolicyValidator().validate_targets(TargetSelector(Path.cwd()).explicit_targets((Path('src/python/projectkoios/bootstrap/schema'),)))
for f in result.findings:
 print(f.format())
print('findings', len(result.findings))
raise SystemExit(1 if result.findings else 0)
PY
```

Result:

```text
findings 0
```

Broader regression:

```bash
uv run pytest -q
```

Result:

```text
211 passed in 1.01s
```

## Deviations and limitations

- The deep-freeze helper is scoped to JSON-like schema-record data. It is not a general-purpose arbitrary Python object freezer.
- Tuple conversion is used internally for frozen JSON arrays. Public `to_dict()` converts tuples back to mutable lists to preserve JSON-compatible output.
- The implementation continues to expose `RecordMetadata.fields` as a mapping for read-only access; nested mappings are now also read-only.

## Current status

The shallow immutability gap identified in `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md` is remediated in code and tests. ATHENA can review this report and the patch for gap closure.
