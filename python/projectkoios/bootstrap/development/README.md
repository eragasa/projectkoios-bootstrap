# Local source-drop convention

This directory is the local intake surface for operator-provided source used to
extract reusable tools.

Use:

```text
python/projectkoios/bootstrap/development/<topic>/intake/
```

An intake is observational source material. It may be LLM-generated,
incomplete, product-specific, or dependent on another repository. It is not
presumed to be a patch, an accepted design, or code that belongs in bootstrap.
Intake directories are ignored by Git, and the development namespace is
excluded from Python package discovery.

The extraction sequence is:

1. inventory the drop without importing or executing it;
2. identify dependencies, effects, tests, and any declared relationship to an
   owner repository;
3. state the reusable behavior separately from the source implementation;
4. route component behavior to its owner;
5. implement only a bounded candidate with sanitized fixtures and deterministic
   normal and failure checks;
6. record limitations, replay behavior, stop conditions, and future ownership;
7. require independent reuse evidence before promotion.

Do not persist intake transcripts, generated review reports, work queues,
credentials, protected content, or machine-specific runtime state here. The
tracked result is the extracted candidate and its evidence, not the raw drop.
