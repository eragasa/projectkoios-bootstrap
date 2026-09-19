# Adversarial architecture review agent candidate

## Status

`CANDIDATE` owned by
[`ADVERSARIAL-ARCH-REVIEW-01`](https://github.com/eragasa/projectkoios-bootstrap/issues/4),
based on one Project Koios architecture-design observation, six adversarial
design trials, and one bounded application to a separate candidate. It is not
installed automatically, validated harness infrastructure, or an accepted
architecture authority. The owner issue and remaining promotion evidence in
[`harness-incubation.md`](../harness-incubation.md) remain required; this
application does not change lifecycle status automatically.

## Observation

During design of local Project Koios instances and project workspaces, the
coordinator already held the complete operator context. Opening another
long-lived writer session would have duplicated context and increased routing
confusion, while keeping all review in the coordinator would have weakened
independence.

The bounded reusable need is not a persistent architect role or a second
writer. It is one fresh-context, read-only adversarial challenge after the
coordinator has materialized and bounded the proposal evidence.

## Candidate component

[`agents/adversarial-architecture-reviewer.md`](agents/adversarial-architecture-reviewer.md)
defines one dormant, Project Koios-specific, tool-less subagent candidate.
[`../../scripts/candidates/adversarial_architecture_packet.py`](../../scripts/candidates/adversarial_architecture_packet.py)
is a dormant candidate helper for descriptor-confined packet construction,
deterministic validation, and task rendering. Neither is installed or invoked
automatically.

There is deliberately no slash-command template. Pi prompt templates cannot
safely combine delegated execution with a deterministic host step that reads,
validates, and embeds a variable evidence allowlist. The coordinator invokes
the candidate agent only after constructing the complete bounded packet.

The coordinator remains responsible for authoring, evidence selection, packet
preflight, effective-capability inspection, checking reviewer output, resolving
duplicate findings, making the
technical recommendation, and requesting only the operator decision or
authorization actually needed. The reviewer cannot accept architecture or
transfer responsibility to the operator.

## Why the agent is tool-less

A normal filesystem `read` tool is not a repository-rooted capability. Prompt
instructions and path checks alone cannot prevent an untrusted proposal from
inducing an absolute, traversal, sibling-repository, or symlink-escape read.

The candidate therefore receives no tools, extensions, inherited project or
global context, inherited skills, parent transcript, or default reads. Its only
evidence is one exact packet embedded in the launch task. This keeps filesystem
discovery, path confinement, evidence selection, and all deterministic schema,
byte-length, hash, and envelope validation in the
coordinator rather than delegating those authorities to reviewed content. The
model performs semantic adversarial review and may detect visible
contradictions, but it is not represented as a cryptographic verifier.

This is a bounded technical agent configuration, not a named organizational
role system. It has no memory, writer, apply, approval, orchestration, or
nested-agent function.

## Review packet contract

The coordinator uses the dormant candidate helper to construct one canonical
JSON packet after validating the complete evidence allowlist. Artifact reads
walk from one opened repository directory descriptor, use `O_NOFOLLOW` for each
component, open the final component nonblocking, reject it unless `fstat`
reports a regular file, and hash the exact bytes read from that same descriptor.
Validation and reading therefore do not reopen a checked path, and a FIFO cannot
block before the type check. The exact JSON is embedded in the delegated
user task between one pair of `<architecture-review-packet>` delimiters; the
tool-less child receives content rather than a filesystem locator. Its
normalized shape is:

```json
{
  "artifacts": [
    {
      "byte_length": 123,
      "content": "complete UTF-8 artifact content",
      "locator": "docs/example.md",
      "sha256": "64 lowercase hexadecimal characters"
    }
  ],
  "schema_version": 1,
  "scope": "Bounded review objective and applicable invariants"
}
```

The task serialization is compact JSON with every literal `<` and `>` in JSON
strings encoded as `\u003c` and `\u003e`. The reviewer counts the one lexical
delimiter pair before decoding JSON. This prevents packet content—including the
candidate agent source—from creating a second envelope while preserving the
exact decoded artifact bytes covered by each identity.

Candidate-stage limits are:

- exactly schema version `1`;
- at most 16 unique artifacts;
- at most 131,072 UTF-8 bytes in one artifact;
- at most 262,144 UTF-8 artifact bytes in aggregate;
- at most 512 UTF-8 bytes in one locator;
- at most 4,096 UTF-8 bytes of scope; and
- no unknown top-level or artifact fields.

Every locator must be a normalized repository-relative POSIX path with no empty,
`.` or `..` component. The coordinator walks each locator from one already-open
repository directory descriptor, rejects symlink components and non-regular
final targets, and never reopens a checked path. This proves descriptor-relative
no-symlink traversal in the active mount namespace; it does not prove physical
content ownership, hard-link provenance, or exclusion of nested mounts. Evidence
selection therefore trusts the repository namespace and the selected contents.
The packet records no absolute path. SHA-256 and byte length cover the exact
UTF-8 bytes supplied to the reviewer.

Artifact order is intentional: applicable repository instructions first,
architecture authority next, proposal and directly reviewed candidate source
last. A trial packet also contains a sanitized operational preflight record of
the parsed effective agent configuration, source identities, packet-construction
contract, validation result, and static checks. The final packet identity is
recorded only after construction in private launch/run state; embedding that
identity inside the packet it identifies would be self-referential. The packet
is not proof that the allowlist is complete or that coordinator attestations are
independent. Missing authority must produce `REVIEW_INCONCLUSIVE`, not broader
discovery.

The packet becomes private subagent session/run state. It must therefore contain
only public, synthetic, or explicitly approved bounded material—never
credentials, customer data, protected source excerpts, or private workspace
content. Any temporary local packet or launch script used during assembly is
owner-only, untracked, and removed after terminal completion or failed launch.

An incomplete run or malformed reviewer output is non-evidence; it is not
resumed as though it completed.

## Agent contract

The candidate agent configuration requires:

- `tools:` empty and `extensions:` empty;
- replacement system prompt with no inherited project, global, skill, or parent
  context;
- fresh context;
- one complete packet embedded in the user task rather than a path or default
  read;
- read-only acceptance classification and no completion guard; and
- no persistent memory or advertised parent role.

The system prompt treats every packet field and artifact as untrusted evidence,
describes the version, field, count, byte, identity, uniqueness, and normalized
locator contract enforced by the deterministic pre-launch validator, and makes
the host/model responsibility split explicit. The model must not claim to
recompute hashes or exact UTF-8 lengths; it challenges visible contradictions
and performs semantic review. The prompt also embeds the adversarial lenses and
actionable output enums, refuses visibly malformed or insufficient packets, and
makes no architecture-acceptance claim.

The launch task contains the delimited packet and may state one optional bounded
review focus outside it. That focus cannot name additional evidence, enable
tools, mutate the packet, or authorize actions. The launch does not pin a model,
loop, run parallel agents, create a worktree, or contain an apply phase.

## Manual trial protocol

A manual candidate trial must:

1. inspect the dormant candidate agent source;
2. list executable agents and effective capabilities;
3. inspect the parsed effective agent configuration and write a sanitized,
   content-identified operational preflight record that declares how the final
   packet identity will be retained outside the packet;
4. build the bounded packet from one closed allowlist through the dormant
   descriptor-confined candidate helper;
5. verify packet schema, bounds, identities, privacy, delimiter-safe
   serialization, and exactly one lexical envelope before delegation;
6. copy or create the exact candidate agent in ignored project-local Pi state;
7. reload discovery and fail unless the effective agent has no tools,
   extensions, inherited contexts, skills, or default reads;
8. embed the complete canonical packet once in the launch task and start one
   fresh review with no runtime capability widening;
9. validate all required output sections and enums atomically;
10. classify malformed or truncated output as an incomplete trial;
11. remove any temporary packet, launch script, and active candidate agent; and
12. verify that the repository has only the intended candidate-source changes.

Subagent launch, packet embedding, agent discovery, output-contract, or cleanup
failure is an infrastructure blocker. The coordinator reports it rather than
silently switching protocol.

## Trial observations

### First trial

The first read-only trial used the builtin reviewer over repository files. It
found four blocking defects: effective capabilities were asserted rather than
verified, absolute or escaping paths were permitted, artifact contents were not
explicitly untrusted, and mutable external skills influenced behavior without a
pinned contract.

The candidate removed skill injection, made the review rules self-contained,
classified artifacts as untrusted, and added canonical path and capability
preflight.

### Second trial

A fresh recheck found that those corrections still relied on an unrestricted
filesystem-read capability. A model-discovered relative link or symlink could
escape the coordinator's explicit allowlist, and prompt text was not an
operating-system sandbox.

The candidate then removed all reviewer tools and attempted to supply a closed,
coordinator-built packet through `defaultReads`.

### Third trial

The effective agent correctly had no tools, but Pi's default-read handoff
provided only the packet's filesystem path rather than its content. The agent
failed closed with `REVIEW_INCONCLUSIVE` instead of widening access. This was a
useful incomplete-evidence case, not a completed review.

The candidate then removed `defaultReads` and embedded the complete packet once
in the launch task.

### Fourth trial

The reviewer received the complete bounded packet and confirmed that the static
design materially reduced the reviewer read surface and remained visibly at
candidate stage. It returned `REVIEW_INCONCLUSIVE` because the packet omitted
effective runtime inspection, deterministic enforcement of the complete packet
contract, and a race-safe coordinator read implementation.

The candidate then required a sanitized effective-capability record in the
packet, described the packet invariants in the trusted prompt, and added a
dormant descriptor-confined builder/validator with malformed, traversal,
symlink, oversize, hash, delimiter, and envelope tests.

### Fifth trial

The fifth fresh tool-less review consumed an eight-artifact, 45,522-byte packet
identified by
`9b601b7dedc4e791e969a21ca825df03a391cde0d8239579a8f9a956a83f42b1`.
Its eight-section output passed atomic structure and enum validation and is
identified by
`f4b295203a899d3c2f99c2868b61f6efbfcbf0c74b2625e2652b8e05f1074b3f`.
The review confirmed the effective no-tool configuration, same-open artifact
reads, bounded lifecycle, and authority separation. It returned
`CHANGES_REQUIRED` for four implementation or contract defects: JSON `true`
could satisfy schema version `1`, duplicate JSON fields and invalid Unicode
were not rejected cleanly, a FIFO could block before the final type check, the
prompt overstated model-side mechanical verification, and the documentation
overstated repository-content provenance. The last two descriptions form one
responsibility/provenance contract correction rather than new authority.

The candidate now enforces integer schema typing, duplicate-field rejection,
canonical serialization, controlled invalid-Unicode errors, and nonblocking
final opens with FIFO coverage. It assigns deterministic schema, byte, hash,
and envelope validation exclusively to the host, limits the model to semantic
review and visible contradictions, and narrows confinement claims to
no-symlink descriptor traversal in the trusted active mount namespace.

### Sixth trial

The sixth focused fresh review consumed an eight-artifact, 52,705-byte packet
identified by
`4b6b3b908b947ea914e678043beeeda05e1012cc1c3cb77a34efe0d625287fe0`.
Its eight-section output passed atomic structure, finding-field, ordering, and
enum validation and is identified by
`b9267e29daa82aab184aa165150bcd936ee852d88489431029e0641c7d56b89a`.
It returned `NO_BLOCKING_FINDINGS`: all four retained fifth-trial corrections
survived focused counterexamples without widening authority or changing
candidate status. It retained two nonblocking conditions: terminal cleanup and
Git validation had to run after the response, and portability beyond the tested
POSIX environment must fail closed or establish equivalent nonblocking open
semantics before reuse.

Full reviewer transcripts and runtime paths remain managed operational state;
they are not tracked artifacts or architecture evidence by themselves.

### Independent issue-inventory application

The candidate was then applied to the separate `ISSUE-INVENTORY-01` helper. The
first bounded review found canonical-authority and malformed-evidence problems,
requested one operator decision about repository identity authority, and drove
focused corrections. A fresh recheck found three remaining blockers: untrusted
replay names in diagnostics, decoder/map failures outside the documented error
contract, and overstated live unknown-field rejection. It also identified
process-level map and trusted-subprocess byte limits as safe to defer within the
documented trust boundary.

The final focused packet contained 12 artifacts and 128,477 artifact bytes and
is identified by
`7fd3a1d5614a6a2e54fbb7a2aae0cb148e6ef12dd103e8d7f891685122eb87a6`.
Its first response correctly returned `REVIEW_INCONCLUSIVE` because the packet
summarized rather than reproduced the three prior blocking findings. The same
reviewer received those findings verbatim through a bounded clarification. The
replacement eight-section output passed atomic structure, finding-field,
ordering, and enum validation and is identified by
`7f4efb8fa3a217ed018dce486f78afe913126083fee95ee2752adcb26dae054f`.
It returned `NO_BLOCKING_FINDINGS` and `NONE`: all three prior blockers were
closed, while the process-level byte-stream limit remained explicitly deferred.

This application demonstrates the intended failure-closed evidence behavior as
well as semantic defect discovery on a separate candidate. It remains
operational reuse evidence, not installation, architecture acceptance, or an
automatic lifecycle transition.

## Dependencies

A manual trial requires:

- `pi-subagents` with project-local custom-agent discovery;
- a model available to the temporary candidate agent;
- the dormant candidate packet helper and its deterministic tests;
- a POSIX host providing descriptor-relative open, `O_DIRECTORY`, `O_NOFOLLOW`,
  `O_CLOEXEC`, and `O_NONBLOCK` semantics; and
- ignored project-local Pi operational state.

The candidate does not require web access, MCP, shell access in the child,
external skills, a workflow engine, an installer, or a persistent agent.

## Known limitations

- Fresh review costs more tokens than inline self-review.
- The coordinator can omit relevant authority when building the packet.
- Descriptor-relative no-symlink traversal trusts the active repository mount
  namespace and does not establish hard-link or physical-content provenance.
- The packet duplicates bounded source content in private session/run state.
- Model behavior may vary because no provider/model baseline is yet validated.
- The packet helper remains dormant candidate code and is not a promoted or
  automatically invoked harness.
- Portability beyond the tested POSIX open semantics is unvalidated and must not
  silently discard the nonblocking final-open requirement.
- A single tool-less reviewer is not consensus, scientific validation, security
  certification, or human architecture acceptance.
- This first observation does not establish recurrence or justify promotion.

## Trial and promotion conditions

The sixth focused trial verified the strict canonical packet validator,
nonblocking final-target rejection in the active environment, host/model
validation boundary, narrowed confinement claim, and output contract without a
blocking finding. Terminal cleanup and unchanged-Git validation are coordinator
postconditions, not reviewer authority. This result remains operational
evidence and does not advance the candidate lifecycle by itself.

Promotion requires the general gate in `docs/harness-incubation.md`, including
an independent second use, a normalized evidence record containing no private
runtime state, deterministic packet and output validation, a failure or
incomplete-evidence case, privacy review, owner routing, and an explicit
retain-or-extract decision. Promotion would move accepted source into active Pi
configuration; candidate status alone does not.
