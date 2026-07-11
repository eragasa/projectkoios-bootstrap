<!-- GENERATED SLICE 4 DRY-RUN PROJECTION EVIDENCE: non-authoritative; not ADR source. -->
# Slice 4 Projection Evidence: docs/adr/adr.petrinet.20260705.132740Z.md

## Projection metadata

- Slice name: adr-json-authority-corpus-dry-run-inventory-slice-4
- Authority mode: candidate evidence only; not repository authority
- Corpus dry run: true
- Bounded subset only: true
- Cutover authorized: false

```json adr-corpus-dry-run-candidate
{
  "authority_change": false,
  "authority_mode": "candidate-evidence-only-not-repository-authority",
  "blocked_from_authority_promotion": true,
  "bounded_subset_only": true,
  "bulk_migration": false,
  "candidate_only": true,
  "content_candidate": {
    "acceptance_criteria": [
      "MUST Show that Place has identity and optional metadata but no token collection.",
      "MUST Show that Marking owns the mapping from place identifiers to immutable token collections.",
      "MUST Show that FiringRequest replaces FiringRule for explicit transition-fire requests.",
      "MUST Show that PetriNetState pairs exactly a static PetriNet with the current Marking.",
      "MUST Show that executor/runtime code, not Place or Transition data objects, owns state update and event emission behavior."
    ],
    "consequences": "The model is expected to become easier to validate against Petri-net mathematics and safer for replay, provenance, dry-run execution, and UI/runtime integration as follow-on implementation evidence accumulates.\n\n### Concern\n- MUST Represent execution as (N, M) transitioning to (N, M prime) through a selected transition and transition binding.\n- MUST Keep graph objects immutable and free of runtime mutation ownership.\n- SHOULD Prepare colored-token support by keeping token color/data on Token and token selection on TransitionBinding, consistent with docs/petri-net-model.md and current PetriNetToken.color implementation.\n- SHOULD Make runtime changes inspectable through explicit fired/marking-changed events rather than vague update callbacks.",
    "decision": "Separate the implementation into static net definition, runtime state, and execution runtime layers with explicit names and ownership boundaries.\n\n### Concern\n- MUST Use conceptual static-definition vocabulary PetriNet, Place, Transition, InputArc, OutputArc, and TransitionGuard while requiring prefixed implementation names and kinded arcs for the first slice.\n- MUST Use conceptual runtime vocabulary Token, Marking, TransitionBinding, FiringRequest, and PetriNetState while requiring the mapped prefixed implementation names for code.\n- MUST Use conceptual runtime vocabulary BindingResolver and PetriNetExecutor plus prefixed implementation event DataObjects and bounded in-process event emission for debugging.\n- MUST Limit acceptance to architecture vocabulary and future refactor authority; acceptance must not validate current dirty implementation.\n- MUST Preserve PetriNet as a reusable generic substrate and place workflow-specific behavior in WorkflowNet or an equivalent domain wrapper.\n- MUST Treat prefixed implementation names as mandatory for this implementation slice: PetriNetPlace, PetriNetToken, PetriNetTransition, PetriNetArc, PetriNetArcKind, PetriNetMarking, PetriNetTransitionBinding, PetriNetFiringRequest, PetriNetState, PetriNetTransitionFiredEvent, and PetriNetMarkingChangedEvent.\n- MUST If accepted, promptly reconcile older workflow draft and plan surfaces so their current vocabulary points to this accepted Petri-net separation decision.\n- MUST NOT Use FiringRule, broad ExecutionState for net-plus-marking only, on_update, place.tokens, or transition.fire_mutating_state as controlling vocabulary.",
    "normalized_status_candidate": "accepted",
    "observed_status_text": "accepted",
    "status_missing": false,
    "title": "ADR 20260705.132740Z: Separate Petri-net Definition, Marking, Binding, and Execution Runtime"
  },
  "conversion_completed_as_authoritative_record": false,
  "corpus_dry_run": true,
  "cutover_authorized": false,
  "database_authority": false,
  "entry_type": "adr_source_candidate",
  "object_type": "AdrJsonAuthorityCorpusDryRunCandidate",
  "outcome": "accepted_source_candidate_not_json_authority",
  "reviewed_inventory": {
    "authority_effect": "candidate",
    "automatic_conversion_eligibility_candidate": true,
    "category_candidate": "template_schema_contract",
    "disposition_candidate": "json_authority_candidate",
    "exclusion_blocking_reasons": [],
    "owner_domain_review_flags": {
      "domain_review_required": false,
      "manual_review_required": false,
      "owner_review_required": false
    }
  },
  "schema_change": false,
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "source_hash": "7fd761c39056bf7a81032b98aabde038d053931e73cd161fb9a48934b2a700a3",
  "source_mutation": false,
  "source_path": "docs/adr/adr.petrinet.20260705.132740Z.md"
}
```
