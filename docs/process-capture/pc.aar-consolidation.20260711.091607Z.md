# Process capture 20260711.091607Z: all-AAR consolidation

## Metadata

- Type: process-capture-consolidation
- Status: active-observation
- Repository: projectkoios-bootstrap
- Owner: KOIOS
- Scope: all AARs in `docs/AAR/` present at synthesis time
- Source count: 298 AAR files
- Requirements draft: `docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md`
- Authority: provenance/process observation only

## Non-authority statement

This artifact consolidates observations from AARs. It is not an ADR, architecture
specification, implementation plan, workflow policy, or completion decision. It
MUST NOT be treated as authority for implementation until candidate requirements
are promoted by the appropriate owner, normally ATHENA/user for workflow
architecture or VULCAN for implementation plans.

## Method

KOIOS reviewed the complete `docs/AAR/*.md` set available in the repository and
classified repeated process observations by source text, title, and declared AAR
sections. The source index below preserves every AAR reference used for this
synthesis.

## Source AAR index

| # | AAR | Title | Observed themes |
|---:|---|---|---|
| 1 | `docs/AAR/aar.20260701.012317_graphify-daemon-adr-session.md` | AAR 20260701.012317: Graphify daemon ADR session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 2 | `docs/AAR/aar.20260701.014145_promotion-review-routing.md` | AAR 20260701.014145: Promotion review routing | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 3 | `docs/AAR/aar.20260701.014433_always-aar-policy.md` | AAR 20260701.014433: Always write session AARs | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, skills |
| 4 | `docs/AAR/aar.20260701.014653_session-start-state-check.md` | AAR 20260701.014653: Session Start State Check | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet |
| 5 | `docs/AAR/aar.20260701.015026_session-boundary-and-athena-status-reporting.md` | AAR 20260701.015026: Session Boundary And Athena Status Reporting | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, schema-template-records |
| 6 | `docs/AAR/aar.20260701.021228_graphify-daemon-adr-routed-to-vulcan.md` | AAR 20260701.021228: Graphify daemon ADR routed to Vulcan | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 7 | `docs/AAR/aar.20260701.023512_graphify-daemon-implementation.md` | AAR 20260701.023512: Graphify ingestion daemon implementation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 8 | `docs/AAR/aar.20260701.023718_graphify-daemon-adr-completed.md` | AAR 20260701.023718: Graphify daemon ADR completed | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 9 | `docs/AAR/aar.20260701.024110_graphify-refresh-noop.md` | AAR 20260701.024110: Graphify Refresh No-op | role-authority, workspace-state-startup-closeout, validation-testing-policy, graphify-daemon-ingestion |
| 10 | `docs/AAR/aar.20260701.024417_daemon-one-shot-run.md` | AAR 20260701.024417: Daemon One-Shot Run | role-authority, validation-testing-policy, graphify-daemon-ingestion |
| 11 | `docs/AAR/aar.20260701.024500_graphify-metadata-staleness-fix.md` | AAR 20260701.024500: Graphify Metadata Staleness Fix | role-authority, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 12 | `docs/AAR/aar.20260701.024612_daemon-detached-run.md` | AAR 20260701.024612: Daemon Detached Run | role-authority, graphify-daemon-ingestion |
| 13 | `docs/AAR/aar.20260701.030000_graphify-daemon-runbook-note.md` | AAR 20260701.030000: Graphify Daemon Runbook Note | role-authority, graphify-daemon-ingestion |
| 14 | `docs/AAR/aar.20260701.030500_ollama-processing-visibility.md` | AAR 20260701.030500: Ollama Processing Visibility | schema-template-records, graphify-daemon-ingestion |
| 15 | `docs/AAR/aar.20260701.031000_ollama-model-resolution-fix.md` | AAR 20260701.031000: Ollama Model Resolution Fix | schema-template-records, graphify-daemon-ingestion |
| 16 | `docs/AAR/aar.20260701.031500_ollama-manifest-wide-batching.md` | AAR 20260701.031500: Ollama Manifest-Wide Batching | schema-template-records, graphify-daemon-ingestion |
| 17 | `docs/AAR/aar.20260701.032000_ollama-corpus-summary.md` | AAR 20260701.032000: Ollama Corpus Summary | schema-template-records, graphify-daemon-ingestion |
| 18 | `docs/AAR/aar.20260701.032257_daemon-liveness-logs.md` | AAR 20260701.032257: Daemon Liveness Logs | role-authority, validation-testing-policy, graphify-daemon-ingestion |
| 19 | `docs/AAR/aar.20260701.033848_session-start-graphify-schema-warning.md` | AAR 20260701.033848: Session Start Graphify Schema Warning | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 20 | `docs/AAR/aar.20260701.034204_human-review-agent-adr-proposal.md` | AAR 20260701.034204: Human Review Agent ADR Proposal | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion, workflow-petrinet |
| 21 | `docs/AAR/aar.20260701.034749_archon-review-agent-spec-run.md` | AAR 20260701.034749: Archon Review Agent Spec Run | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 22 | `docs/AAR/aar.20260701.040950_cross-repo-policy-baseline-incorporation.md` | AAR 20260701.040950: Cross-Repo Policy Baseline Incorporation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 23 | `docs/AAR/aar.20260701.052326_koios-technical-debt-plan.md` | AAR 20260701.052326: Koios Technical Debt Plan | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 24 | `docs/AAR/aar.20260701.052502_plan-refinement-first-review.md` | AAR 20260701.052502: Plan Refinement First Review | handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 25 | `docs/AAR/aar.20260701.052905_opencode-harness-crash-recovery.md` | AAR 20260701.052905: Opencode harness crash recovery | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 26 | `docs/AAR/aar.20260701.053127_dirty-tree-review.md` | AAR 20260701.053127: Dirty tree review | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 27 | `docs/AAR/aar.20260701.053534_review-agent-artifact-consolidation.md` | AAR 20260701.053534: Review agent artifact consolidation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 28 | `docs/AAR/aar.20260701.053849_new-state-check.md` | AAR 20260701.053849: New state check | workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet |
| 29 | `docs/AAR/aar.20260701.054000_new-session-state-check.md` | AAR 20260701.054000: New session state check | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet |
| 30 | `docs/AAR/aar.20260701.054945_review-agent-adr-promotion.md` | AAR 20260701.054945: Review agent ADR promotion | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 31 | `docs/AAR/aar.20260701.105808_athena-revise-adr-arg-parsing-fix.md` | AAR 20260701.105808: athena-revise-adr argument parsing fix | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet, skills |
| 32 | `docs/AAR/aar.20260701.110510_graphify-fresh-rebuild-node-id-warning.md` | AAR 20260701.110510: Fresh graphify rebuild and pre-#1504 node-ID warning | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 33 | `docs/AAR/aar.20260701.111757_adr-status-sync.md` | AAR 20260701.111757: ADR status sync for implemented decisions | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, graphify-daemon-ingestion, workflow-petrinet |
| 34 | `docs/AAR/aar.20260701.114300_conduct-interview-implementation.md` | AAR 20260701.114300: Conduct-interview workflow implementation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 35 | `docs/AAR/aar.20260701.115608_new-session-state-check.md` | AAR 20260701.115608: New Session State Check | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 36 | `docs/AAR/aar.20260701.120000_repo-root-agents-tradeoffs.md` | AAR 20260701.120000: Repo-root AGENTS tradeoff review | handoff-slice-gates, validation-testing-policy |
| 37 | `docs/AAR/aar.20260701.120745_adr-proposal-template.md` | AAR 20260701.120745: ADR proposal template added | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 38 | `docs/AAR/aar.20260701.121500_commit-push-graphify.md` | AAR 20260701.121500: Commit, push, and graphify | workspace-state-startup-closeout, graphify-daemon-ingestion |
| 39 | `docs/AAR/aar.20260701.122025_adr-proposal-domain-split.md` | AAR 20260701.122025: ADR proposal template updated for domain split | adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, workflow-petrinet |
| 40 | `docs/AAR/aar.20260701.122628_docs-architecture-canonicalization.md` | AAR 20260701.122628: Docs architecture canonicalization | adr-architecture-lifecycle, graphify-daemon-ingestion, operator-console-ui |
| 41 | `docs/AAR/aar.20260701.123101_cross-repo-routing-confusion.md` | AAR 20260701.123101: Cross-repo routing confusion | role-authority, adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion |
| 42 | `docs/AAR/aar.20260701.124545_session-cleanup.md` | AAR 20260701.124545: Session cleanup | adr-architecture-lifecycle, workspace-state-startup-closeout, graphify-daemon-ingestion |
| 43 | `docs/AAR/aar.20260701.124612_agent-charter-canonical-routing.md` | AAR 20260701.124612: Agent charter canonical routing | adr-architecture-lifecycle, handoff-slice-gates |
| 44 | `docs/AAR/aar.20260701.124912_extracted-repo-local-notes.md` | AAR 20260701.124912: Extracted repo local notes | role-authority |
| 45 | `docs/AAR/aar.20260701.125245_extracted-readme-pointer-cleanup.md` | AAR 20260701.125245: Extracted README pointer cleanup | role-authority, validation-testing-policy, schema-template-records |
| 46 | `docs/AAR/aar.20260701.125400_archive-all-adrs.md` | AAR 20260701.125400: Archive all ADRs | adr-architecture-lifecycle |
| 47 | `docs/AAR/aar.20260701.125559_role-prose-pruning.md` | AAR 20260701.125559: Role prose pruning | validation-testing-policy |
| 48 | `docs/AAR/aar.20260701.125611_architecture-index-adr-archive-link.md` | AAR 20260701.125611: Architecture index ADR archive link | adr-architecture-lifecycle, graphify-daemon-ingestion |
| 49 | `docs/AAR/aar.20260701.130000_map-standardization.md` | AAR 20260701.130000: Map standardization | role-authority, workspace-state-startup-closeout, validation-testing-policy, graphify-daemon-ingestion |
| 50 | `docs/AAR/aar.20260701.130032_adr-template-extracted.md` | AAR 20260701.130032: ADR template extracted | adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 51 | `docs/AAR/aar.20260701.131000_repo-projection-architecture.md` | AAR 20260701.131000: Repo projection architecture | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, schema-template-records, skills |
| 52 | `docs/AAR/aar.20260701.131245_architecture-index-linking.md` | AAR 20260701.131245: Architecture index linking | adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 53 | `docs/AAR/aar.20260701.131718_adr-template-control-note.md` | AAR 20260701.131718: ADR template control note | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 54 | `docs/AAR/aar.20260701.131745_architecture-status-date-slug.md` | AAR 20260701.131745: Architecture status date slug | adr-architecture-lifecycle, schema-template-records |
| 55 | `docs/AAR/aar.20260701.131900_architecture-frontmatter-conversion.md` | AAR 20260701.131900: Architecture frontmatter conversion | adr-architecture-lifecycle, schema-template-records, skills |
| 56 | `docs/AAR/aar.20260701.132048_adr-metadata-block.md` | AAR 20260701.132048: ADR metadata block | adr-architecture-lifecycle, schema-template-records, workflow-petrinet |
| 57 | `docs/AAR/aar.20260701.132621_adr-json-schema.md` | AAR 20260701.132621: ADR JSON schema | adr-architecture-lifecycle, schema-template-records, workflow-petrinet |
| 58 | `docs/AAR/aar.20260701.133946_deep-interview-skill-design.md` | AAR 20260701.133946: Deep interview skill design | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, skills |
| 59 | `docs/AAR/aar.20260701.134430_deep-interview-axis-design.md` | AAR 20260701.134430: Deep interview axis design | role-authority, schema-template-records, skills |
| 60 | `docs/AAR/aar.20260701.134909_deep-interview-ordering.md` | AAR 20260701.134909: Deep interview ordering | role-authority, workspace-state-startup-closeout, schema-template-records, skills |
| 61 | `docs/AAR/aar.20260701.135151_meta-harness-control-surfaces.md` | AAR 20260701.135151: Meta-harness control surfaces | adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, skills |
| 62 | `docs/AAR/aar.20260701.135339_meta-harness-axis-set.md` | AAR 20260701.135339: Meta-harness axis set | adr-architecture-lifecycle, schema-template-records, workflow-petrinet, skills |
| 63 | `docs/AAR/aar.20260701.135521_meta-harness-rubric-mechanism.md` | AAR 20260701.135521: Meta-harness rubric mechanism | adr-architecture-lifecycle, workspace-state-startup-closeout, schema-template-records, workflow-petrinet, skills |
| 64 | `docs/AAR/aar.20260701.135948_architecture-formatting-instructions.md` | AAR 20260701.135948: Architecture formatting instructions | adr-architecture-lifecycle, workspace-state-startup-closeout, schema-template-records, workflow-petrinet, skills |
| 65 | `docs/AAR/aar.20260701.140312_architecture-file-protection.md` | AAR 20260701.140312: Architecture file protection | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 66 | `docs/AAR/aar.20260701.140351_control-surface-matrix.md` | AAR 20260701.140351: Control-surface matrix | role-authority, adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, skills |
| 67 | `docs/AAR/aar.20260701.140745_agent-charter-instructions-template.md` | AAR 20260701.140745: Agent charter instructions template | validation-testing-policy, schema-template-records |
| 68 | `docs/AAR/aar.20260701.140853_debt-triage-promotion.md` | AAR 20260701.140853: Debt triage promotion | adr-architecture-lifecycle, skills |
| 69 | `docs/AAR/aar.20260701.141133_debt-triage-scoring.md` | AAR 20260701.141133: Debt triage scoring | adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, skills |
| 70 | `docs/AAR/aar.20260701.141202_weighted-rubric-human-override.md` | AAR 20260701.141202: Weighted rubric with human override | schema-template-records, skills |
| 71 | `docs/AAR/aar.20260701.141419_leverage-feasibility-routing.md` | AAR 20260701.141419: Leverage feasibility routing | adr-architecture-lifecycle, handoff-slice-gates, skills |
| 72 | `docs/AAR/aar.20260701.141500_workspace-bootstrap-skill.md` | AAR 20260701.141500: Workspace bootstrap skill | role-authority, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, skills |
| 73 | `docs/AAR/aar.20260701.141616_control-surface-adr-promotion.md` | AAR 20260701.141616: Control-surface ADR promotion | adr-architecture-lifecycle, schema-template-records, skills |
| 74 | `docs/AAR/aar.20260701.141728_workspace-command-and-skill.md` | AAR 20260701.141728: Workspace command and Koios skill | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, skills |
| 75 | `docs/AAR/aar.20260701.141840_policy-surface-priority-update.md` | AAR 20260701.141840: Policy surface priority update | handoff-slice-gates, validation-testing-policy, skills |
| 76 | `docs/AAR/aar.20260701.142022_hermes-workspace-agents-file.md` | AAR 20260701.142022: Hermes workspace AGENT file | role-authority, workspace-state-startup-closeout, validation-testing-policy, schema-template-records |
| 77 | `docs/AAR/aar.20260701.142323_scenario-first-interview-reset.md` | AAR 20260701.142323: Scenario-first interview reset | adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, skills |
| 78 | `docs/AAR/aar.20260701.142445_workspace-mail-system.md` | AAR 20260701.142445: Workspace mail system | role-authority, workspace-state-startup-closeout, handoff-slice-gates, intercom-mailbox-messaging, skills |
| 79 | `docs/AAR/aar.20260701.142619_policy-personality-scenario.md` | AAR 20260701.142619: Policy personality scenario | adr-architecture-lifecycle, validation-testing-policy, schema-template-records |
| 80 | `docs/AAR/aar.20260701.142823_question-prioritization.md` | AAR 20260701.142823: Question prioritization | validation-testing-policy, schema-template-records, skills |
| 81 | `docs/AAR/aar.20260701.142910_apartment-message-banner.md` | AAR 20260701.142910: Apartment message banner | workspace-state-startup-closeout, validation-testing-policy, intercom-mailbox-messaging |
| 82 | `docs/AAR/aar.20260701.143022_question-queue-collapsed.md` | AAR 20260701.143022: Question queue collapsed | handoff-slice-gates, validation-testing-policy, schema-template-records |
| 83 | `docs/AAR/aar.20260701.143115_hermes-command-authority.md` | AAR 20260701.143115: HERMES command authority note | role-authority, workspace-state-startup-closeout, handoff-slice-gates |
| 84 | `docs/AAR/aar.20260701.143555_policy-baseline-changes.md` | AAR 20260701.143555: Policy baseline changes | adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 85 | `docs/AAR/aar.20260701.143556_hermes-workspace-migration.md` | AAR 20260701.143556: Hermes workspace migration | role-authority, workspace-state-startup-closeout |
| 86 | `docs/AAR/aar.20260701.150100_workspace-local-harness-instantiation-planning.md` | AAR 20260701.150100: Workspace-local harness instantiation planning | adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 87 | `docs/AAR/aar.20260701.150220_workspace-identity-from-agents-clarification.md` | AAR 20260701.150220: Workspace identity from AGENTS clarification | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates |
| 88 | `docs/AAR/aar.20260701.150623_draft-adr-vulcan-comments.md` | AAR 260701.150623: Draft ADR Vulcan comments | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 89 | `docs/AAR/aar.20260701.150835_draft-adr-comment-policy-codified.md` | AAR 260701.150835: Draft ADR comment policy codified | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy |
| 90 | `docs/AAR/aar.20260701.150900_new-adr-comment-policy-session.md` | AAR 260701.150900: New ADR comment policy session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 91 | `docs/AAR/aar.20260701.151100_workspace-identity-contract-brief.md` | AAR 20260701.151100: Workspace identity contract brief | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 92 | `docs/AAR/aar.20260701.151900_adr-lifecycle-policy.md` | AAR 20260701.151900: ADR lifecycle policy | adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 93 | `docs/AAR/aar.20260701.152300_review-template-adr-lifecycle-link.md` | AAR 20260701.152300: Review template ADR lifecycle link | adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 94 | `docs/AAR/aar.20260701.152548_agent-identity-and-adr-pause.md` | AAR 20260701.152548: Agent identity and ADR pause | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, graphify-daemon-ingestion |
| 95 | `docs/AAR/aar.20260701.152749_new-session-state-check.md` | AAR 20260701.152749: New session state check | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 96 | `docs/AAR/aar.20260701.153038_delegated-identity-resolution.md` | AAR 20260701.153038: Delegated identity resolution | role-authority, handoff-slice-gates, validation-testing-policy |
| 97 | `docs/AAR/aar.20260701.154234_sandbox-message-delivery-terminology.md` | AAR 20260701.154234: Sandbox Message Delivery Terminology | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, intercom-mailbox-messaging, workflow-petrinet |
| 98 | `docs/AAR/aar.20260701.154729_new-session.md` | AAR YYYYMMDD.HHMMSS: New Session Start | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, graphify-daemon-ingestion |
| 99 | `docs/AAR/aar.20260701.160322_workspace-local-agents-copy.md` | AAR YYYYMMDD.HHMMSS: Workspace-local agents copy | role-authority, workspace-state-startup-closeout, validation-testing-policy |
| 100 | `docs/AAR/aar.20260701.161827_copy-koios-agents-workspace.md` | AAR 20260701.161827: Copy Koios agents into workspace | role-authority, workspace-state-startup-closeout |
| 101 | `docs/AAR/aar.20260701.162012_commit-and-push-session.md` | AAR 20260701.162012: Commit and push session | role-authority, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records |
| 102 | `docs/AAR/aar.20260701.165842_repo-context-scout.md` | AAR 20260701.165842: Repo context scout | role-authority, workspace-state-startup-closeout, validation-testing-policy |
| 103 | `docs/AAR/aar.20260701.182136_control-surfaces-draft-session.md` | AAR 20260701.182136: Control surfaces draft session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 104 | `docs/AAR/aar.20260701.182553_docs-model-workspace-artifacts.md` | AAR 20260701.182553: Docs model workspace artifacts | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet, operator-console-ui, skills |
| 105 | `docs/AAR/aar.20260701.183013_architecture-docs-active-file.md` | AAR 20260701.183013: Architecture docs active file | adr-architecture-lifecycle, validation-testing-policy, schema-template-records, workflow-petrinet, skills |
| 106 | `docs/AAR/aar.20260701.184337_python-architecture-status-enum.md` | AAR 20260701.184337: Python architecture status enum | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records |
| 107 | `docs/AAR/aar.20260701.184614_typescript-rust-mirror.md` | AAR 20260701.184614: TypeScript and Rust mirror for architecture status | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, operator-console-ui |
| 108 | `docs/AAR/aar.20260701.185145_precision-edit-loop-agents-update.md` | AAR 20260701.185145: Precision-edit loop instruction added | role-authority, workspace-state-startup-closeout, handoff-slice-gates, workflow-petrinet, skills |
| 109 | `docs/AAR/aar.20260701.191634_root-agents-role-table.md` | AAR 20260701.191634: Root AGENTS role table moved | role-authority, workspace-state-startup-closeout, handoff-slice-gates, workflow-petrinet |
| 110 | `docs/AAR/aar.20260701.192342_delegated-identity-resolution-root.md` | AAR 20260701.192342: Delegated identity resolution moved to root AGENTS | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, workflow-petrinet |
| 111 | `docs/AAR/aar.20260701.192556_delegation-provenance-moved-root.md` | AAR 20260701.192556: Delegation provenance moved to root | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, workflow-petrinet |
| 112 | `docs/AAR/aar.20260701.193907_hermes-agents-pruned.md` | AAR 20260701.193907: Hermes AGENTS pruned to Hermes-local scope | role-authority, workspace-state-startup-closeout, validation-testing-policy, workflow-petrinet |
| 113 | `docs/AAR/aar.20260701.215003_vulcan-adr-triple-implementation.md` | AAR 20260701.215003: VULCAN ADR triple implementation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion |
| 114 | `docs/AAR/aar.20260701.233318_graphify-ast-mode-fallback.md` | AAR 20260701.233318: Graphify AST-mode fallback | role-authority, graphify-daemon-ingestion |
| 115 | `docs/AAR/aar.20260701.233722_graphify-ast-only-runbook-note.md` | AAR 20260701.233722: Graphify AST-only runbook note | graphify-daemon-ingestion |
| 116 | `docs/AAR/aar.20260701.235306_new-session-process-cleanup.md` | AAR 20260701.235306: New Session Process Cleanup | role-authority, workspace-state-startup-closeout, schema-template-records, graphify-daemon-ingestion |
| 117 | `docs/AAR/aar.20260702.000000_new-session-startup.md` | AAR: New session startup check | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 118 | `docs/AAR/aar.20260702.000551_idea-spike-adr-workflow.md` | AAR 20260702.000551: Idea-Spike-ADR Workflow Draft | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 119 | `docs/AAR/aar.20260702.001234_idea-spike-adr-architecture-index.md` | AAR 20260702.001234: Idea-Spike-ADR Architecture Index Update | role-authority, adr-architecture-lifecycle, graphify-daemon-ingestion, workflow-petrinet |
| 120 | `docs/AAR/aar.20260702.001845_lifecycle-index-created.md` | AAR 20260702.001845: Lifecycle Index Created | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion |
| 121 | `docs/AAR/aar.20260702.002233_architecture-index-table.md` | AAR 20260702.002233: Architecture Index Table | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion, workflow-petrinet |
| 122 | `docs/AAR/aar.20260702.003120_architecture-index-now-includes-adrs.md` | AAR 20260702.003120: Architecture Index Now Includes ADRs | role-authority, adr-architecture-lifecycle, graphify-daemon-ingestion, workflow-petrinet |
| 123 | `docs/AAR/aar.20260702.004200_adr-title-naming-convention.md` | AAR 20260702.004200: ADR Title Naming Convention | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 124 | `docs/AAR/aar.20260702.004512_adr-template-conformance.md` | AAR 20260702.004512: ADR Template Conformance | role-authority, adr-architecture-lifecycle, schema-template-records, workflow-petrinet |
| 125 | `docs/AAR/aar.20260702.004943_adr-filenames-and-json-idea.md` | AAR 20260702.004943: ADR Filenames and JSON Storage Idea | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 126 | `docs/AAR/aar.20260702.005121_spike-entry-conditions-idea.md` | AAR 20260702.005121: Spike Entry Conditions Idea | adr-architecture-lifecycle, workflow-petrinet |
| 127 | `docs/AAR/aar.20260702.005312_archive-adr-template-normalization.md` | AAR 20260702.005312: Archive ADR Template Normalization | adr-architecture-lifecycle, schema-template-records |
| 128 | `docs/AAR/aar.20260702.005650_brainstorm-capture-template-adr.md` | AAR 20260702.005650: Brainstorm Capture Template ADR | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 129 | `docs/AAR/aar.20260702.005825_incubator-template-in-docs-templates.md` | AAR 20260702.005825: Incubator Template in docs/templates | adr-architecture-lifecycle, schema-template-records |
| 130 | `docs/AAR/aar.20260702.005917_architecture-index-links-incubator-template.md` | AAR 20260702.005917: Architecture Index Links Incubator Template | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 131 | `docs/AAR/aar.20260702.010225_high-leverage-workflow-scope.md` | AAR 20260702.010225: High-Leverage Workflow Scope | adr-architecture-lifecycle, workspace-state-startup-closeout, graphify-daemon-ingestion, workflow-petrinet |
| 132 | `docs/AAR/aar.20260702.010530_agents-md-prose-rewrite.md` | AAR 20260702.010530: AGENTS.md Prose Rewrite | schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 133 | `docs/AAR/aar.20260702.010828_workspace-agent-guides-local-only.md` | AAR 20260702.010828: Workspace Agent Guides Are Local Only | role-authority, workspace-state-startup-closeout |
| 134 | `docs/AAR/aar.20260702.011217_athena-language-moved-to-workspace-guide.md` | AAR 20260702.011217: Athena Language Moved to Workspace Guide | role-authority, workspace-state-startup-closeout |
| 135 | `docs/AAR/aar.20260702.011340_vulcan-language-moved-to-workspace-guide.md` | AAR 20260702.011340: Vulcan Language Moved to Workspace Guide | role-authority, workspace-state-startup-closeout, workflow-petrinet |
| 136 | `docs/AAR/aar.20260702.011415_koios-language-moved-to-workspace-guide.md` | AAR 20260702.011415: Koios Language Moved to Workspace Guide | role-authority, workspace-state-startup-closeout, workflow-petrinet |
| 137 | `docs/AAR/aar.20260702.011829_agent-windows-on_message-idea.md` | AAR 20260702.011829: Agent Windows with on_message Idea | role-authority, adr-architecture-lifecycle, handoff-slice-gates, intercom-mailbox-messaging |
| 138 | `docs/AAR/aar.20260702.012544_incubator-comments-and-spike-requirements.md` | AAR 20260702.012544: Incubator Comments and Spike Requirements | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 139 | `docs/AAR/aar.20260702.013215_adr-draft-comment-promotion-workflow.md` | AAR 20260702.013215: ADR Draft Comment Promotion Workflow | adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 140 | `docs/AAR/aar.20260702.014027_new-session-athena-default.md` | AAR: New-session ATHENA defaulting | role-authority, workspace-state-startup-closeout, graphify-daemon-ingestion |
| 141 | `docs/AAR/aar.20260702.014603_skill-register-binding-implementation.md` | AAR 20260702.014603: Skill register binding implementation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, skills |
| 142 | `docs/AAR/aar.20260702.020532_hermes-message-delivery-adr-session.md` | AAR 20260702.020532: Hermes message delivery ADR session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 143 | `docs/AAR/aar.20260702.020601_canonical-workspace-state-protocol.md` | AAR 20260702.020601: canonical workspace state protocol | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 144 | `docs/AAR/aar.20260702.020904_comment-scope-rule-session.md` | AAR 20260702.020904: comment-scope rule session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet |
| 145 | `docs/AAR/aar.20260702.021842_harness-identity-prose-refactor.md` | AAR 20260702.021842: Harness identity prose refactor | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, skills |
| 146 | `docs/AAR/aar.20260702.022639_archon-skill-description-conflict.md` | AAR 20260702.022639: Archon skill description conflict | role-authority, workspace-state-startup-closeout, validation-testing-policy, skills |
| 147 | `docs/AAR/aar.20260702.023230_athena-comments-on-ideas-and-drafts.md` | AAR 20260702.023230: Athena comments on ideas and draft ADRs | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records |
| 148 | `docs/AAR/aar.20260702.023544_koios-comment-attribution-correction.md` | AAR 20260702.023544: Koios comment attribution correction | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout |
| 149 | `docs/AAR/aar.20260702.030640_vulcan-session-agents-adrs-coding-standards.md` | AAR: Vulcan session — AGENTS.md cleanup, draft ADR comments, implementation plan ADR, coding standards flow | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet, skills |
| 150 | `docs/AAR/aar.20260702.030848_archon-skill-description-shortened.md` | AAR 20260702.030848: Archon skill description shortened | role-authority, workspace-state-startup-closeout, validation-testing-policy, skills |
| 151 | `docs/AAR/aar.20260702.031406_root-agents-docs-pointers.md` | AAR 20260702.031406: Root AGENTS docs pointers | role-authority, validation-testing-policy |
| 152 | `docs/AAR/aar.20260702.032308_controlling-adr-join-protocol.md` | AAR 20260702.032308: Controlling ADR join protocol draft | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, graphify-daemon-ingestion |
| 153 | `docs/AAR/aar.20260702.032505_draft-adr-comment-processing-protocol.md` | AAR 20260702.032505: Draft ADR comment-processing protocol | role-authority, adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, workflow-petrinet |
| 154 | `docs/AAR/aar.20260702.034139_skill-register-binding-policy.md` | AAR 20260702.034139: Skill register and ADR binding policy | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, skills |
| 155 | `docs/AAR/aar.20260702.040139_skill-register-population.md` | AAR 20260702.040139: Skill register population | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, skills |
| 156 | `docs/AAR/aar.20260702.040645_custom-graphrag-incubator-note.md` | AAR 20260702.040645: Custom GraphRAG incubator note | role-authority, validation-testing-policy, graphify-daemon-ingestion |
| 157 | `docs/AAR/aar.20260702.040919_custom-graphrag-spike-promotion.md` | AAR 20260702.040919: Custom GraphRAG spike promotion | role-authority, adr-architecture-lifecycle, validation-testing-policy, graphify-daemon-ingestion |
| 158 | `docs/AAR/aar.20260702.041132_custom-graphrag-spike-expanded.md` | AAR 20260702.041132: Custom GraphRAG spike expanded | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion |
| 159 | `docs/AAR/aar.20260702.041548_custom-graphrag-two-plane-spike.md` | AAR 20260702.041548: Custom GraphRAG two-plane spike rewrite | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 160 | `docs/AAR/aar.20260702.042026_aar-json-postgres-storage-spike.md` | AAR 20260702.042026: AAR JSON storage spike | role-authority, schema-template-records, workflow-petrinet |
| 161 | `docs/AAR/aar.20260702.042653_petri-net-executor-adr-plan.md` | AAR 20260702.042653: Petri-net executor ADR and implementation plan | role-authority, adr-architecture-lifecycle, handoff-slice-gates, workflow-petrinet |
| 162 | `docs/AAR/aar.20260702.043444_workflow-executor-target-migration.md` | AAR 20260702.043444: Workflow executor target and migration framing | role-authority, adr-architecture-lifecycle, handoff-slice-gates, workflow-petrinet |
| 163 | `docs/AAR/aar.20260702.043948_koios-basic-code-review-authority.md` | AAR 20260702.043948: Koios basic code review authority | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy |
| 164 | `docs/AAR/aar.20260702.044127_koios-adversarial-review-emphasis.md` | AAR 20260702.044127: Koios adversarial review emphasis | role-authority, handoff-slice-gates, validation-testing-policy |
| 165 | `docs/AAR/aar.20260702.044254_koios-adversarial-code-review-wording.md` | AAR 20260702.044254: Koios adversarial code-review wording | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 166 | `docs/AAR/aar.20260702.044539_koios-adversarial-review-adr-rename.md` | AAR 20260702.044539: Koios adversarial review ADR rename | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion |
| 167 | `docs/AAR/aar.20260702.050213_commit-push-closeout.md` | AAR 20260702.050213: commit-push-closeout | role-authority, workspace-state-startup-closeout |
| 168 | `docs/AAR/aar.20260702.052017_koios-role-motivation.md` | AAR 20260702.052017: Koios role motivation note | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout |
| 169 | `docs/AAR/aar.20260702.052145_blind-commit-all-scope.md` | AAR 20260702.052145: Blind commit-all scope | workspace-state-startup-closeout, schema-template-records |
| 170 | `docs/AAR/aar.20260702.053015_session-start-format.md` | AAR 20260702.053015: Session start format update | workspace-state-startup-closeout |
| 171 | `docs/AAR/aar.20260702.053312_session-start-draft-adr-check.md` | AAR 20260702.053312: Session start draft ADR check | adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates |
| 172 | `docs/AAR/aar.20260702.053445_session-start-incubator-spike-check.md` | AAR 20260702.053445: Session start incubator and spike check | adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates |
| 173 | `docs/AAR/aar.20260702.053812_high-leverage-session-sweep.md` | AAR 20260702.053812: High-leverage session sweep | adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 174 | `docs/AAR/aar.20260702.121432_adr-encapsulation-hierarchy.md` | AAR 20260702.121432: ADR encapsulation and hierarchy | adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 175 | `docs/AAR/aar.20260702.125652_workflow-binding-adr-update.md` | AAR 20260702.125652Z: Workflow-binding ADR update | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 176 | `docs/AAR/aar.20260702.130032_session-closing-sequence-confusion.md` | AAR 20260702.130032Z: Session closing sequence confusion | role-authority, workspace-state-startup-closeout, workflow-petrinet |
| 177 | `docs/AAR/aar.20260702.130210_closeout-sequence-clarified-in-agents.md` | AAR 20260702.130210Z: Closeout sequence clarified in AGENTS | workspace-state-startup-closeout |
| 178 | `docs/AAR/aar.20260702.152613_session-close.md` | AAR 20260702.152613: session close | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, graphify-daemon-ingestion |
| 179 | `docs/AAR/aar.20260702.173456_incubator-supersedence-check.md` | AAR: Incubator supersedence check | role-authority, adr-architecture-lifecycle, validation-testing-policy |
| 180 | `docs/AAR/aar.20260702.173801_json-db-spike-and-production-trace.md` | AAR 20260702.173801: JSON DB Spike, Production Trace ADR, and Plan Decomposition | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, skills |
| 181 | `docs/AAR/aar.20260702.174927_spike-taxonomy-draft-adr-alignment.md` | AAR 20260702.174927: Spike Taxonomy and Draft ADR Alignment | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 182 | `docs/AAR/aar.20260702.180350_adr-names-umbrella-linking.md` | AAR 20260702.180350: ADR Names Umbrella and Child-Link Encapsulation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 183 | `docs/AAR/aar.20260702.180845_architecture-adr-names-index-split.md` | AAR 20260702.180845: Architecture ADR Names Index Split | role-authority, adr-architecture-lifecycle, graphify-daemon-ingestion |
| 184 | `docs/AAR/aar.20260702.181459_architecture-index-table-normalization.md` | AAR 20260702.181459: Architecture Index Table Normalization | role-authority, adr-architecture-lifecycle, schema-template-records, graphify-daemon-ingestion |
| 185 | `docs/AAR/aar.20260702.181831_architecture-adr-00-index-surface.md` | AAR 20260702.181831: Architecture ADR 00 Index Surface | role-authority, adr-architecture-lifecycle, handoff-slice-gates, graphify-daemon-ingestion |
| 186 | `docs/AAR/aar.20260702.183000_template-and-implementation-namespace-split.md` | AAR: Template and implementation namespace split | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, intercom-mailbox-messaging, workflow-petrinet |
| 187 | `docs/AAR/aar.20260702.184300_adr-lifecycle-converted-to-adr.md` | AAR 20260702.184300: ADR Lifecycle Converted to ADR | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 188 | `docs/AAR/aar.20260702.184548_policy-lifecycle-file-move.md` | AAR 20260702.184548: Policy Lifecycle File Move | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 189 | `docs/AAR/aar.20260702.192138_inline-supersession-markers-for-promotion-mechanics.md` | AAR 20260702.192138: Inline Supersession Markers for Promotion Mechanics | role-authority, adr-architecture-lifecycle, workflow-petrinet |
| 190 | `docs/AAR/aar.20260702.192807_remove-delegated-operator-from-active-adrs.md` | AAR 20260702.192807: Remove Delegated-Operator from Active ADRs | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 191 | `docs/AAR/aar.20260702.193846_lifecycle-status-and-promotion-model-refresh.md` | AAR 20260702.193846: Lifecycle Status and Promotion Model Refresh | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 192 | `docs/AAR/aar.20260702.194412_archive-draft-comment-and-promotion-workflow.md` | AAR 20260702.194412: Archive Draft Comment and Promotion Workflow | role-authority, adr-architecture-lifecycle, workflow-petrinet |
| 193 | `docs/AAR/aar.20260702.201028_commit-and-push-session.md` | AAR 20260702.201028: Commit and Push Session | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, workflow-petrinet |
| 194 | `docs/AAR/aar.20260702.201751_deprecate-incubator-and-spikes-directories.md` | AAR 20260702.201751: Deprecate Incubator and Spikes Directories | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 195 | `docs/AAR/aar.20260702.203600_close-session-kernel-package.md` | AAR 20260702.203600: Close Session for Kernel Package Prompt | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout |
| 196 | `docs/AAR/aar.20260702.205545_prompt-iterate-vulcan-blocker-handling.md` | AAR 20260702.205545: Prompt iterate Vulcan blocker handling | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, schema-template-records |
| 197 | `docs/AAR/aar.20260702.213614Z_implementation-control-kernel-seed.md` | AAR — Implementation control kernel seed | role-authority, workspace-state-startup-closeout, handoff-slice-gates |
| 198 | `docs/AAR/aar.20260702.220000_hermes-autoprocess-startup.md` | AAR — Hermes autoprocess startup | role-authority, workspace-state-startup-closeout |
| 199 | `docs/AAR/aar.20260703.000000_graphrag-process-capture-observation.md` | AAR 20260703.000000: GraphRAG process-capture observation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, intercom-mailbox-messaging, workflow-petrinet, skills, process-capture |
| 200 | `docs/AAR/aar.20260703.003305_routing-cleanup-and-ui-namespace-sweep.md` | AAR: Routing cleanup and UI namespace sweep | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 201 | `docs/AAR/aar.20260703.010000_graphrag-docs-relocation.md` | AAR 20260703.010000: GraphRAG docs relocation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 202 | `docs/AAR/aar.20260703.024352_mailbox-bridge-validation-friction.md` | AAR 20260703.024352: Mailbox bridge validation friction | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 203 | `docs/AAR/aar.20260703.040438_adr-schema-file-addition.md` | AAR 20260703.040438: ADR schema file addition | adr-architecture-lifecycle, schema-template-records |
| 204 | `docs/AAR/aar.20260703.040619_adr-implementation-schema-addition.md` | AAR 20260703.040619: ADR implementation schema addition | adr-architecture-lifecycle, schema-template-records |
| 205 | `docs/AAR/aar.20260703.040738_adr-kernel-addition.md` | AAR 20260703.040738: ADR kernel addition | adr-architecture-lifecycle |
| 206 | `docs/AAR/aar.20260703.101637_hermes-startup-path-resolution-friction.md` | AAR 20260703.101637: Hermes startup path resolution friction | role-authority, workspace-state-startup-closeout, handoff-slice-gates, workflow-petrinet |
| 207 | `docs/AAR/aar.20260703.101900_gitignore-ds-store-ignore.md` | AAR 20260703.101900: .DS_Store ignore added | general-process |
| 208 | `docs/AAR/aar.20260703.104142_end-session-protocol-miss.md` | AAR: End-session protocol miss | role-authority, handoff-slice-gates, intercom-mailbox-messaging |
| 209 | `docs/AAR/aar.20260703.104744_hermes-startup-rollback.md` | AAR 20260703.104744: Hermes startup rollback | role-authority, workspace-state-startup-closeout |
| 210 | `docs/AAR/aar.20260703.113005_canonical-context-table-and-graphify-mismatch.md` | AAR 20260703.113005: Canonical context table and graphify mismatch | workspace-state-startup-closeout, graphify-daemon-ingestion |
| 211 | `docs/AAR/aar.20260703.114802_mailbox-bridge-stabilization.md` | AAR 20260703.114802: Mailbox bridge stabilization | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 212 | `docs/AAR/aar.20260703.121208_session-start-solved-problem-routes.md` | AAR 20260703.121208: Session-start solved-problem routing | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, workflow-petrinet |
| 213 | `docs/AAR/aar.20260703.134342_meeting-round-control-boundary-miss.md` | AAR 20260703.134342: Meeting round control-boundary miss | role-authority, adr-architecture-lifecycle, intercom-mailbox-messaging |
| 214 | `docs/AAR/aar.20260703.145202_adr-skill-review-fix.md` | AAR 20260703.145202: ADR skill review fixes | role-authority, adr-architecture-lifecycle, handoff-slice-gates, schema-template-records, skills |
| 215 | `docs/AAR/aar.20260703.150105_missing-hermes-workspace-startup-fix.md` | AAR 20260703.150105: Missing Hermes workspace startup fix | role-authority, workspace-state-startup-closeout |
| 216 | `docs/AAR/aar.20260703.151135_intercom-directive-addition.md` | AAR 20260703.151135: Intercom directive addition | intercom-mailbox-messaging |
| 217 | `docs/AAR/aar.20260703.161251_session-start-sweep.md` | AAR: Session start sweep | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion, workflow-petrinet, skills |
| 218 | `docs/AAR/aar.20260703.170208_athena-workspace-state-surface.md` | AAR: Athena workspace-state surface | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout |
| 219 | `docs/AAR/aar.20260703.170556_remove-workspaces-ignore.md` | AAR: Remove workspaces ignore | workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 220 | `docs/AAR/aar.20260703.223117_restore-vulcan-agents.md` | AAR 20260703.223117: Restore Vulcan workspace AGENTS | role-authority, workspace-state-startup-closeout, validation-testing-policy |
| 221 | `docs/AAR/aar.20260704.000000_remove-mailbox-control-surfaces.md` | AAR 20260704.000000: Remove mailbox control surfaces | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 222 | `docs/AAR/aar.20260704.000100_document-state-orchestration-correction.md` | AAR 20260704.000100: Document-state orchestration correction | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 223 | `docs/AAR/aar.20260704.000647_koios-agent-policy-identity-cleanup.md` | AAR 20260704.000647: Koios agent policy identity cleanup | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, workflow-petrinet |
| 224 | `docs/AAR/aar.20260704.000741_graphrag-first-slice-closeout.md` | AAR 20260704.000741: GraphRAG first slice closeout | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 225 | `docs/AAR/aar.20260704.051713_python-coding-standard-sweep.md` | Python coding standard sweep AAR | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 226 | `docs/AAR/aar.20260704.091823_koios-process-capture-and-docs-cleanup.md` | AAR 20260704.091823: Koios process capture and docs cleanup | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet, process-capture |
| 227 | `docs/AAR/aar.20260704.123324_workspace-layout-commit-closeout.md` | AAR 20260704.123324: Workspace layout commit closeout | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 228 | `docs/AAR/aar.20260704.145301_vulcan-python-control-closeout.md` | AAR: Vulcan Python control closeout | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, graphify-daemon-ingestion |
| 229 | `docs/AAR/aar.20260704.151640_graphrag-persisted-index.md` | AAR 20260704.151640: GraphRAG persisted-index implementation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 230 | `docs/AAR/aar.20260704.162218_workspace-state-proposal-promotion.md` | AAR 20260704.162218: workspace-state proposal promotion | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 231 | `docs/AAR/aar.20260704.162554_workspace-state-adr-acceptance.md` | AAR 20260704.162554: workspace-state ADR acceptance | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 232 | `docs/AAR/aar.20260704.172155_schema-base-pre-vulcan-refinement.md` | AAR 20260704.172155: Schema-base pre-Vulcan refinement | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 233 | `docs/AAR/aar.20260704.173652_schema-record-brief-handoff.md` | AAR 20260704.173652: Schema-record brief handoff | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, intercom-mailbox-messaging |
| 234 | `docs/AAR/aar.20260704.174859_schema-record-worktree-implementation.md` | AAR 20260704.174859: Schema-record worktree implementation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 235 | `docs/AAR/aar.20260704.193035_python-policy-validator-first-slice.md` | AAR 20260704.193035: Python policy validator first slice | role-authority, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 236 | `docs/AAR/aar.20260704.205637_schema-package-policy-remediation.md` | AAR 20260704.205637: Schema package policy remediation | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 237 | `docs/AAR/aar.20260704.213600_schema-record-conformance-review.md` | AAR 20260704.213600: Schema-record conformance review | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 238 | `docs/AAR/aar.20260704.214623_validation-package-policy-remediation.md` | AAR 20260704.214623: Validation package policy remediation | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 239 | `docs/AAR/aar.20260704.220328_commands-package-policy-remediation.md` | AAR 20260704.220328: Commands package policy remediation | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 240 | `docs/AAR/aar.20260704.221001_harness-data-policy-remediation.md` | AAR 20260704.221001: Harness data package policy remediation | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 241 | `docs/AAR/aar.20260704.222506_harness-handoffs-policy-remediation.md` | AAR 20260704.222506: Harness handoffs package policy remediation | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 242 | `docs/AAR/aar.20260704.223422_harness-daemon-watcher-scheduler-policy-remediation.md` | AAR 20260704.223422: Harness daemon watcher/scheduler policy remediation | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 243 | `docs/AAR/aar.20260704.224451_harness-daemon-activities-publisher-policy-remediation.md` | AAR 20260704.224451: Harness daemon activities/publisher policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 244 | `docs/AAR/aar.20260704.225212_harness-daemon-orchestrator-policy-remediation.md` | AAR 20260704.225212: Harness daemon orchestrator policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 245 | `docs/AAR/aar.20260704.225528_harness-daemon-graphify-runner-policy-remediation.md` | AAR 20260704.225528: Harness daemon Graphify runner policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 246 | `docs/AAR/aar.20260704.230324_harness-daemon-ollama-policy-remediation.md` | AAR 20260704.230324: Harness daemon Ollama policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 247 | `docs/AAR/aar.20260704.230851_bootstrap-residual-policy-remediation.md` | AAR 20260704.230851: Bootstrap residual policy remediation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 248 | `docs/AAR/aar.20260704.231604_cli-package-policy-remediation.md` | AAR 20260704.231604: CLI package policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 249 | `docs/AAR/aar.20260704.232402_ingestors-source-retrieval-policy-remediation.md` | AAR 20260704.232402: Ingestors source/retrieval policy remediation | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 250 | `docs/AAR/aar.20260704.233415_ingestors-answer-backend-policy-remediation.md` | AAR 20260704.233415: Ingestors answer/backend policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 251 | `docs/AAR/aar.20260704.233957_ingestors-index-app-policy-remediation.md` | AAR 20260704.233957: Ingestors index/app policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 252 | `docs/AAR/aar.20260704.234720_ingestors-config-schema-policy-remediation.md` | AAR 20260704.234720: Ingestors config/schema policy remediation | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 253 | `docs/AAR/aar.20260704.235450_source-python-policy-closeout-packaging.md` | AAR 20260704.235450: Source Python policy closeout packaging | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy |
| 254 | `docs/AAR/aar.20260704.235829_python-policy-validator-cli.md` | AAR 20260704.235829: Python policy validator CLI integration | role-authority, workspace-state-startup-closeout, validation-testing-policy, workflow-petrinet |
| 255 | `docs/AAR/aar.20260705.000755_schema-test-policy-remediation.md` | AAR 20260705.000755: Schema test policy remediation | role-authority, workspace-state-startup-closeout, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 256 | `docs/AAR/aar.20260705.001733_ingestors-test-policy-remediation.md` | AAR 20260705.001733: Ingestors test policy remediation | role-authority, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 257 | `docs/AAR/aar.20260705.002345_python-policy-test-remediation.md` | AAR 20260705.002345: Python policy test remediation | role-authority, validation-testing-policy, schema-template-records |
| 258 | `docs/AAR/aar.20260705.003351_workspace-state-protocol-bootstrap-reconciliation.md` | AAR 20260705.003351: Workspace-state protocol bootstrap reconciliation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 259 | `docs/AAR/aar.20260705.010450_root-bootstrap-test-policy-remediation.md` | AAR 20260705.010450: Root bootstrap test policy remediation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records |
| 260 | `docs/AAR/aar.20260705.011110_adr-lifecycle-naming-consolidation-proposal.md` | AAR 20260705.011110: ADR lifecycle/naming consolidation proposal | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 261 | `docs/AAR/aar.20260705.013339_harness-validation-test-policy-remediation.md` | AAR 20260705.013339: Harness validation test policy remediation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, validation-testing-policy, schema-template-records |
| 262 | `docs/AAR/aar.20260705.013729_daemon-activities-test-policy-remediation.md` | AAR 20260705.013729: Daemon activities test policy remediation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 263 | `docs/AAR/aar.20260705.014833_template-representation-proposal-review.md` | AAR 20260705.014833: Template representation proposal review | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 264 | `docs/AAR/aar.20260705.015600_archon-run-watch-test-policy-remediation.md` | AAR 20260705.015600: Archon run watch test policy remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet, skills |
| 265 | `docs/AAR/aar.20260705.020437_publisher-test-policy-and-layout-remediation.md` | AAR 20260705.020437: Publisher test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 266 | `docs/AAR/aar.20260705.020850_schema-backed-template-adr.md` | AAR 20260705.020850: Schema-backed template ADR correction | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 267 | `docs/AAR/aar.20260705.021059_ollama-test-policy-and-layout-remediation.md` | AAR 20260705.021059: Ollama test policy and layout remediation | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 268 | `docs/AAR/aar.20260705.021601_daemon-run-once-test-policy-and-layout-remediation.md` | AAR 20260705.021601: Daemon run-once test policy and layout remediation | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 269 | `docs/AAR/aar.20260705.022028_watcher-test-policy-and-layout-remediation.md` | AAR 20260705.022028: Watcher test policy and layout remediation | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 270 | `docs/AAR/aar.20260705.032754_handoff-evaluator-test-policy-and-layout-remediation.md` | AAR 20260705.032754: Handoff evaluator test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 271 | `docs/AAR/aar.20260705.033230_topics-view-full-test-policy-and-layout-remediation.md` | AAR 20260705.033230: Topics view full test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 272 | `docs/AAR/aar.20260705.033644_handoff-parser-test-policy-and-layout-remediation.md` | AAR 20260705.033644: Handoff parser test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, skills |
| 273 | `docs/AAR/aar.20260705.034033_exclusion-policy-test-policy-and-layout-remediation.md` | AAR 20260705.034033: Exclusion policy test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 274 | `docs/AAR/aar.20260705.034512_topics-view-deterministic-test-policy-and-layout-remediation.md` | AAR 20260705.034512: Topics view deterministic test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 275 | `docs/AAR/aar.20260705.035102_scheduler-test-policy-and-layout-remediation.md` | AAR 20260705.035102: Scheduler test policy and layout remediation | role-authority, adr-architecture-lifecycle, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 276 | `docs/AAR/aar.20260705.035308_message-test-policy-and-layout-remediation.md` | AAR 20260705.035308: Message test policy and layout remediation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 277 | `docs/AAR/aar.20260705.095200_remaining-test-policy-remediation-session-closeout.md` | AAR 20260705.095200: Remaining test policy remediation session closeout | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 278 | `docs/AAR/aar.20260705.100243_handoff-artifact-test-policy-remediation.md` | HandoffArtifact test policy remediation AAR | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 279 | `docs/AAR/aar.20260705.100714_violation-appender-test-policy-remediation.md` | ViolationAppender test policy remediation AAR | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 280 | `docs/AAR/aar.20260705.100911_handoff-evaluator-grouping-test-policy-remediation.md` | HandoffEvaluator grouping test policy remediation AAR | role-authority, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 281 | `docs/AAR/aar.20260705.101124_violation-formatting-test-policy-remediation.md` | Violation formatting test policy remediation AAR | role-authority, workspace-state-startup-closeout, validation-testing-policy, schema-template-records |
| 282 | `docs/AAR/aar.20260705.102506_workflow-petri-net-executor-first-slice.md` | Workflow Petri-net executor first slice AAR | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 283 | `docs/AAR/aar.20260705.105604_workflow-adapter-dependency-encapsulation.md` | Workflow adapter dependency encapsulation AAR | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 284 | `docs/AAR/aar.20260705.111255_workspace-adr-consolidation.md` | AAR 20260705.111255: Workspace ADR consolidation | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion |
| 285 | `docs/AAR/aar.20260705.142149_petrinet-separation-adr-remediation.md` | Petri-net separation ADR remediation AAR | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 286 | `docs/AAR/aar.20260705.173808_petrinet-followups.md` | AAR 20260705.173808: Petri-net follow-ups | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, workflow-petrinet |
| 287 | `docs/AAR/aar.20260706.045501_workflow-adapter-contract-hardening.md` | AAR 20260706.045501: Workflow adapter topology round trip | role-authority, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 288 | `docs/AAR/aar.20260708.041331_template-representation-vulcan-handoff.md` | AAR 20260708.041331: Template representation VULCAN handoff | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging, workflow-petrinet |
| 289 | `docs/AAR/aar.20260708.044531_template-representation-roundtrip.md` | AAR 20260708.044531: Template representation schema-backed round-trip | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, process-capture |
| 290 | `docs/AAR/aar.20260709.010343_template-record-roundtrip-skill-brief.md` | AAR 20260709.010343: Template record round-trip skill brief | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, skills |
| 291 | `docs/AAR/aar.20260709.010828_koios-comments-skill-brief-update.md` | AAR 20260709.010828: KOIOS comments applied to skill brief | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, intercom-mailbox-messaging, skills |
| 292 | `docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md` | AAR 20260709.012011: Template record round-trip skill integration | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, intercom-mailbox-messaging, skills |
| 293 | `docs/AAR/aar.20260709.014124_adr-json-database-pilot-brief.md` | AAR 20260709.014124: ADR JSON/database pilot brief | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, intercom-mailbox-messaging |
| 294 | `docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md` | AAR 20260711.035759: ADR JSON/database one-ADR pilot | role-authority, adr-architecture-lifecycle, workspace-state-startup-closeout, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet |
| 295 | `docs/AAR/aar.20260711.051951_json-document-database-separation.md` | AAR 20260711.051951: JSON document database separation | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records |
| 296 | `docs/AAR/aar.20260711.065704_json-schemas-adr-conformance.md` | AAR 20260711.065704: JSON schemas ADR conformance | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, graphify-daemon-ingestion, workflow-petrinet |
| 297 | `docs/AAR/aar.20260711.081405_operator-console-review-one-proposal-fixture.md` | AAR 20260711.081405: Operator Console review one proposal fixture | role-authority, adr-architecture-lifecycle, handoff-slice-gates, validation-testing-policy, schema-template-records, workflow-petrinet, operator-console-ui |
| 298 | `docs/AAR/aar.20260711.090601_operator-console-fixture-interaction-visibility.md` | AAR 20260711.090601: Operator Console fixture interaction visibility | role-authority, handoff-slice-gates, schema-template-records, intercom-mailbox-messaging, operator-console-ui |

## Consolidated process observations

### 1. Durable filesystem state is the real workflow substrate

Across session-start, closeout, workspace-state, and process-capture AARs, the
stable coordination surface is not chat memory but repository artifacts:
`state.md`, `active.md`, ADRs, architecture notes, implementation briefs, plans,
reports, AARs, provenance notes, and process-capture traces. Intercom/chat can
move work, but durable state must be written back to files before a later role
can safely continue.

### 2. Role and authority boundaries repeatedly prevent silent promotion

AARs frequently record corrections where an implementation convenience,
workspace note, draft ADR, process note, or fixture could have become de facto
authority. The observed pattern is to name the represented role, source artifact,
document domain, approval state, and non-authority boundary before proceeding.

### 3. Work succeeds when sliced into bounded, named transitions

Successful implementation chains use a bounded token: user request or ADR intent
-> ATHENA brief/spec -> VULCAN plan -> explicit approval -> implementation/tests
-> implementation report/AAR -> ATHENA/KOIOS review. Large or ambiguous work
produced process friction until it was narrowed to a first slice, fixture,
package, or target document.

### 4. Approval and pause gates are process-critical, not ceremony

Many AARs preserve cases where coding had to pause for user/HERMES/ATHENA
approval, licensing/dependency policy, schema authority, lifecycle status,
workspace target, or source mutation scope. Pauses reduced authority drift.

### 5. Validation evidence must include command context and scope

AARs repeatedly record validation improvements: run commands from repository
root when required, record exact commands and outputs, distinguish no-findings
from unsupported validation surfaces, and avoid treating one validator as proof
for unrelated artifact types.

### 6. Dirty-tree packaging is a recurring risk

Many closeout and remediation AARs record large dirty batches, concurrent
ATHENA/KOIOS/VULCAN changes, local generated files, and staging risk. A workflow
object needs explicit package boundaries, owner labels, and residual dirty-state
classification before commit.

### 7. Draft/proposal/incubator surfaces need explicit lifecycle handling

ADR, template, spike, incubator, and schema AARs repeatedly distinguish draft,
proposal, accepted, active, archived, superseded, generated, fixture, and
sidecar states. Problems occur when title, filename, status, and directory
location imply different authority.

### 8. Sidecar provenance and fixture provenance are first-class evidence

Schema/template/ADR JSON and Operator Console AARs show that source-only fields,
hashes, projection facts, generated artifact paths, and non-live fixture status
must be preserved outside the canonical record when the schema does not own them.
Fixture-backed UI must show this visibly to avoid fixture laundering.

### 9. Tooling and dependency decisions need local scope until promoted

Graphify/Ollama/daemon, Python policy, TypeScript, PM4Py/SNAKES, Vite, and skill
AARs show that tooling can solve a slice while still not being global policy.
Package-local config, optional dependency gates, draft coding policies, and
explicit extraction boundaries keep implementation from making architecture.

### 10. User-visible artifacts need user-preview validation

The Operator Console AARs show that for UI/operator-facing work, tests and builds
are insufficient process evidence by themselves. Local preview and user
inspection surfaced style and interaction-scope expectations that then became
bounded follow-up lessons.

### 11. Messaging systems are useful but insufficient as durable authority

Mailbox/intercom AARs show message delivery, session identity, duplicated names,
and disappearing sessions can lose or confuse authority. Important routing,
clarification, and acceptance criteria must be materialized as durable artifacts.

### 12. Skills and reusable procedures require stability gates

Skill AARs show that registering a draft skill or creating a Markdown skill file
is not the same as validating it. Stable skill promotion needs parser/schema or
frontmatter validation evidence and an owning review surface.

## Process-capture implications

The all-AAR pattern supports a future workflow object, but only as a candidate
requirements surface. The workflow object should model documents, transitions,
roles, gates, evidence, and non-authority markers rather than trying to infer
completion from chat state or file presence alone.

See `docs/process-capture/requirements.workflow-object.from-aar-synthesis.20260711.091607Z.md` for candidate requirements derived from these observations.
