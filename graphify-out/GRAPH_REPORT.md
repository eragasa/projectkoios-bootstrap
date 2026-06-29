# Graph Report - .  (2026-06-29)

## Corpus Check
- 164 files · ~135,290 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 260 nodes · 330 edges · 34 communities (15 shown, 19 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Archon Workflow Core|Archon Workflow Core]]
- [[_COMMUNITY_Archon Node Types & Configuration|Archon Node Types & Configuration]]
- [[_COMMUNITY_Graphify Knowledge Graph Pipeline|Graphify Knowledge Graph Pipeline]]
- [[_COMMUNITY_Archon Platform & Integration Guides|Archon Platform & Integration Guides]]
- [[_COMMUNITY_Pi Harness Archon Integration|Pi Harness Archon Integration]]
- [[_COMMUNITY_Project Koios Overview & Run Mgmt|Project Koios Overview & Run Mgmt]]
- [[_COMMUNITY_Archon Adapters & CLI|Archon Adapters & CLI]]
- [[_COMMUNITY_OpenCode Harness & Multi-Repo Extraction|OpenCode Harness & Multi-Repo Extraction]]
- [[_COMMUNITY_Pi Agent Configuration|Pi Agent Configuration]]
- [[_COMMUNITY_Architecture & Workflow Definitions|Architecture & Workflow Definitions]]
- [[_COMMUNITY_Interactive Workflow Protocol|Interactive Workflow Protocol]]
- [[_COMMUNITY_Goose MCP Setup|Goose MCP Setup]]
- [[_COMMUNITY_Workflow Run Lifecycle|Workflow Run Lifecycle]]
- [[_COMMUNITY_Koios Scripts & Harness|Koios Scripts & Harness]]
- [[_COMMUNITY_OpenCode Plugin Config|OpenCode Plugin Config]]
- [[_COMMUNITY_OpenCode Package Dependencies|OpenCode Package Dependencies]]
- [[_COMMUNITY_License|License]]
- [[_COMMUNITY_OpenCode AI Plugin Package|OpenCode AI Plugin Package]]
- [[_COMMUNITY_OpenCode Config|OpenCode Config]]
- [[_COMMUNITY_Koios Harness Script|Koios Harness Script]]
- [[_COMMUNITY_Gitignore|Gitignore]]
- [[_COMMUNITY_Goose Curate Prompt|Goose Curate Prompt]]
- [[_COMMUNITY_Goose Ingest Prompt|Goose Ingest Prompt]]
- [[_COMMUNITY_Goose Search Prompt|Goose Search Prompt]]
- [[_COMMUNITY_Goose UI Bootstrap|Goose UI Bootstrap]]
- [[_COMMUNITY_Interactive Protocol Concept|Interactive Protocol Concept]]
- [[_COMMUNITY_Node Types Concept|Node Types Concept]]
- [[_COMMUNITY_Pi Agent Trust|Pi Agent Trust]]
- [[_COMMUNITY_Pi Session Map|Pi Session Map]]
- [[_COMMUNITY_Pi Settings|Pi Settings]]
- [[_COMMUNITY_Provider Compatibility|Provider Compatibility]]
- [[_COMMUNITY_Harness Script Config|Harness Script Config]]
- [[_COMMUNITY_Three-Path Env Model|Three-Path Env Model]]

## God Nodes (most connected - your core abstractions)
1. `archon/skills/.claude/skills/archon/SKILL.md` - 19 edges
2. `Archon` - 17 edges
3. `Graphify Skill Definition` - 15 edges
4. `archon/skills/.agents/skills/archon/references/workflow-dag.md` - 13 edges
5. `Parameter Matrix Quick Reference` - 11 edges
6. `Parameter Matrix Reference` - 10 edges
7. `Archon CLI skill` - 10 edges
8. `Workflow Authoring DAG` - 10 edges
9. `archon/skills/.claude/skills/archon/guides/setup.md` - 9 edges
10. `Workflow Good Practices and Anti-Patterns` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Archon Configuration Guide` --semantically_similar_to--> `.archon/config.yaml Configuration`  [INFERRED] [semantically similar]
  .claude/skills/archon/guides/config.md → .archon/config.yaml
- `Graphify Knowledge Graph System` --semantically_similar_to--> `Manage Archon Runs Skill`  [INFERRED] [semantically similar]
  AGENTS.md → .claude/skills/manage-run/SKILL.md
- `Archon CLI` --semantically_similar_to--> `Archon Harness`  [INFERRED] [semantically similar]
  .claude/skills/manage-run/SKILL.md → README.md
- `Goose Harness` --conceptually_related_to--> `Goose MCP Configuration`  [INFERRED]
  README.md → goose/.mcp.json
- `Create ADR Workflow` --conceptually_related_to--> `Harness split (archon/goose/opencode/pi)`  [INFERRED]
  archon/workflows/create-adr.yaml → docs/architecture.00.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **** — archon_platform, archon_dot_diy, archon_setup_wizard, claude_skills_archon_guides_cli_setup_guide, claude_skills_archon_guides_config_guide, claude_skills_archon_guides_github_integration_guide, claude_skills_archon_guides_telegram_bot_guide, claude_skills_archon_guides_slack_bot_guide, claude_skills_archon_guides_discord_bot_guide, claude_skills_archon_guides_server_setup_guide, claude_skills_archon_references_workflow_dag_authoring, claude_skills_archon_references_dag_advanced_features, variable_substitution_ref, claude_skills_archon_references_cli_commands_ref, claude_skills_archon_references_authoring_commands_ref, claude_skills_archon_references_good_practices_ref, claude_skills_archon_references_interactive_workflows_ref, claude_skills_archon_references_troubleshooting_ref, claude_skills_archon_references_repo_init_ref, claude_skills_archon_references_parameter_matrix_ref, claude_skills_archon_examples_command_template_example, smart_issue_fix_example, archon_config_file [INFERRED]
- **** — readme_archon_harness, readme_opencode_harness, readme_goose_harness [EXTRACTED]
- **Pi Agent Configuration Subsystem** — pi_agent_auth_config, pi_agent_models_config, pi_agent_npm_package, pi_agent_settings_config, pi_agent_trust_config [EXTRACTED 1.00]
- **OpenCode Configuration Subsystem** — opencode_opencode_opencode_config, opencode_package_config, opencode_plugins_graphify_plugin, opencode_ai_plugin_library [EXTRACTED 1.00]

## Communities (34 total, 19 thin omitted)

### Community 0 - "Archon Workflow Core"
Cohesion: 0.06
Nodes (39): Approval Node Human in the Loop Gates, Artifact Chain Design Pattern, Cancel Node Guarded Exits, Common Workflow Failure Modes, Fresh Context with Artifact Handoff, Deterministic Nodes for Deterministic Work, Inline Sub-Agents for Map Reduce Patterns, Transparent Relay Protocol for Interactive Workflows (+31 more)

### Community 1 - "Archon Node Types & Configuration"
Cohesion: 0.11
Nodes (32): Archon Approval Nodes, Archon Approve/Reject Commands, Archon Bash Nodes, Archon Cancel Nodes, Archon Command Authoring, Archon Configuration System, Archon Workflow Good Practices, Archon Hooks (+24 more)

### Community 2 - "Graphify Knowledge Graph Pipeline"
Cohesion: 0.08
Nodes (29): Structural AST Extraction for Code Files, CLAUDE Dot Md Native Integration, Post-Commit Hook Graph Rebuild, Community Detection and Clustering, Confidence Scoring EXTRACTED INFERRED AMBIGUOUS, Cross-Repo Graph Merge, Export Formats HTML Obsidian Neo4j FalkorDB SVG GraphML, Extraction Cache for Incremental Reuse (+21 more)

### Community 3 - "Archon Platform & Integration Guides"
Cohesion: 0.17
Nodes (24): .archon/config.yaml Configuration, archon.diy Documentation Site, Archon, Archon Setup Wizard, Command File Template, CLI Setup Guide, Archon Configuration Guide, Discord Bot Setup Guide (+16 more)

### Community 4 - "Pi Harness Archon Integration"
Cohesion: 0.14
Nodes (18): Archon CLI (remote agentic coding platform), Goose harness (knowledge curation, vault), Pi harness (operator interface, orchestration), Archon command file template, Archon DAG workflow example (smart-issue-fix), Archon CLI setup guide, Archon configuration guide, Archon Discord bot setup guide (+10 more)

### Community 5 - "Project Koios Overview & Run Mgmt"
Cohesion: 0.13
Nodes (17): Approve-Reject-Resume Two-Step Pattern, Archon CLI, Archon Workflow Runs, Manage Archon Runs Skill, Graphify Knowledge Graph System, Graphify Instructions for Agents, graphify-out Directory, Filesystem MCP Server (+9 more)

### Community 6 - "Archon Adapters & CLI"
Cohesion: 0.23
Nodes (15): Archon CLI, Archon Discord Adapter, Archon Three-Path Env Model, Archon GitHub Adapter, Archon Server, archon/skills/.claude/skills/archon/guides/cli.md, archon/skills/.claude/skills/archon/guides/discord.md, archon/skills/.claude/skills/archon/guides/github.md (+7 more)

### Community 7 - "OpenCode Harness & Multi-Repo Extraction"
Cohesion: 0.20
Nodes (14): Multi-repo extraction plan (search, api, obsidian), opencode harness (implementation, tests, validation), Validation gates (pytest, ruff, mypy), Multi-repo execution readiness checklist, Multi-repo extraction phases 2-5 completion report, Build rules, Handoff contract rules, Specification gate rules (+6 more)

### Community 8 - "Pi Agent Configuration"
Cohesion: 0.16
Nodes (13): Pi Agent Auth Configuration, GPT-5.4-mini Default Model, Pi Agent Models Configuration, Llama 3.2 1B Local Model, Ollama Provider, Qwen3 Local Model, dependencies, pi-smart-fetch (+5 more)

### Community 9 - "Architecture & Workflow Definitions"
Cohesion: 0.29
Nodes (11): Create ADR Workflow, Design Review Workflow, Plan Feature Workflow, Harness split (archon/goose/opencode/pi), Bootstrap Architecture Document, Goose Agent Definition, Research Support Prompt, Package Responsibility Map (+3 more)

### Community 10 - "Interactive Workflow Protocol"
Cohesion: 0.32
Nodes (8): Interactive Workflow Guide, Parameter Matrix Reference, Repository Init Guide, Workflow Troubleshooting Guide, Variable Substitution Reference, Workflow DAG Authoring Guide, Interactive Workflow Relay Protocol, Three-Path Env Model

### Community 11 - "Goose MCP Setup"
Cohesion: 0.50
Nodes (3): filesystem, npx, @modelcontextprotocol/server-filesystem

### Community 12 - "Workflow Run Lifecycle"
Cohesion: 0.67
Nodes (3): Manage-Run Command Reference, Manage Archon Runs Skill, Workflow run lifecycle (start/approve/reject/abandon/resume)

### Community 13 - "Koios Scripts & Harness"
Cohesion: 0.67
Nodes (3): Koios Harness Management CLI, Koios Tmux Session Layout Four Windows, Koios Scripts README

## Knowledge Gaps
- **95 isolated node(s):** `$schema`, `plugin`, `@opencode-ai/plugin`, `npx`, `@modelcontextprotocol/server-filesystem` (+90 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `archon/skills/.claude/skills/archon/SKILL.md` connect `Archon Node Types & Configuration` to `Archon Adapters & CLI`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Archon Workflow DAG` (e.g. with `Archon Approval Nodes` and `Archon CLI`) actually correct?**
  _`Archon Workflow DAG` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `plugin`, `@opencode-ai/plugin` to the rest of the system?**
  _103 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Archon Workflow Core` be split into smaller, more focused modules?**
  _Cohesion score 0.0620782726045884 - nodes in this community are weakly interconnected._
- **Should `Archon Node Types & Configuration` be split into smaller, more focused modules?**
  _Cohesion score 0.11290322580645161 - nodes in this community are weakly interconnected._
- **Should `Graphify Knowledge Graph Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.07635467980295567 - nodes in this community are weakly interconnected._
- **Should `Pi Harness Archon Integration` be split into smaller, more focused modules?**
  _Cohesion score 0.13725490196078433 - nodes in this community are weakly interconnected._