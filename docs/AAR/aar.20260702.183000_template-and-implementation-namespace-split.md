# AAR: Template and implementation namespace split

## Scope
Project Koios bootstrap docs/architecture and docs/templates namespace cleanup.

## What happened
Created and linked new mothership ADRs for `adr.implementation` and `adr.templates`, added `docs/implementation/implementation.00.md` and `docs/templates/templates.00.md`, and moved the adversarial gate implementation note into `docs/implementation/`.

## Process issues
- The implementation-note location was initially ambiguous and had to be corrected from an architecture path to `docs/implementation/`.
- The template control split needed several iterations to separate `adr.adr-template-contract` from `adr.templates`.
- Intercom usage was discovered during the session; session-to-session messaging is useful but not yet part of the normal workflow.

## Proposed follow-up improvements
- Add explicit namespace guidance for architecture vs implementation vs templates in the bootstrap docs.
- Normalize control-link wording across templates and implementation notes.
- Document intercom usage in the relevant workspace guidance.

## Candidate ADR or implementation topics
- Promote `adr.implementation` and `adr.templates` once the implementation machinery is in place.
- Add a small implementation brief/template for namespace docs.
- Add intercom workflow guidance for Hermes/Vulcan coordination.

## Current status
Draft changes prepared locally; ready for commit.
