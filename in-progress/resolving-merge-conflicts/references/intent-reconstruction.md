# Intent Reconstruction

Reconstruct what each change preserves before choosing surviving text.

## Core rule

```text
source evidence → side intent → compatibility → minimal resolution → observable proof
```

Conflict markers show overlapping text, not why it changed, whether one side supersedes the other, or whether behavior moved elsewhere.

## Conflict record

Create one record per path or independently meaningful hunk:

```md
## <path>:<symbol-or-hunk>

- Conflict type: content | add/add | modify/delete | rename/delete | rename/rename | binary | mode | submodule | generated | lockfile
- Active operation and paused unit:
- Base behavior and unrelated same-path baseline:
- Current-operation source and intent:
- Competing source and intent:
- Evidence:
- Relationship: compatible | superseded | incompatible | uncertain
- Proposed transition and resolution:
- Behavior retained:
- Behavior removed and why:
- Verification:
```

Separate pre-existing same-path content from conflict content. Do not assume interactive hunk staging can resolve an unmerged index; require the reviewed separation plan and stage-0 proof in [operation-state](operation-state.md). If safe separation cannot be shown, stop rather than stage the path. Post-state proof belongs in [verification-checklist](verification-checklist.md).
Record operation metadata existence and the paused unit; do not infer activity from conflict markers or a computed metadata path.

## Evidence order

Prefer primary sources in this order:

1. Paused commit patch, parent, and message.
2. Merge heads or selected/reverted commit.
3. Base and available index stages.
4. For lockfiles/generated files: authoritative manifest, schema, template, source data, tool configuration.
5. Adjacent commits introducing competing code.
6. Linked PR, issue, ticket, design decision, or migration note.
7. Repository instructions and invariants.
8. Current implementation, callers, tests, and public behavior.

A commit message alone is not proof when its patch, tests, or linked issue disagree. Record uncertainty rather than smoothing inconsistent evidence.

### Marker-free or auto-resolved state

Use this only when Git reports a conflict but markers are absent, content appears automatically resolved, or provenance affects the semantic decision:

1. Inspect operation status and index stages; compare the working tree with base/current/competing stages and the paused patch.
2. If needed, inspect `git rerere status`, `git rerere diff`, applicable `.gitattributes` driver entries, `merge.<driver>.driver`, and `merge.conflictStyle` (including config origins).
3. Treat rerere, custom/union drivers, and conflict style as mechanism evidence, never intent evidence. Validate behavior against commits, callers, tests, and other primary sources.

If the result cannot be explained and independently validated, classify it uncertain and stop.

## Operation lenses

### Merge

Identify the integration goal, independently required behavior of each parent, intentional removals/replacements, and whether composition would duplicate effects or conflict with policy.

### Rebase

Recover the exact paused delta on its selected parent(s); map it onto the new base and reject later commits as explanations for the current one. For `--rebase-merges`, identify the replayed merge and parent structure rather than assuming one parent.

### Cherry-pick

Select the useful delta, retain unrelated target behavior, and check whether it already exists. For a merge commit, require the recorded `-m` mainline parent from sequencer options or equivalent evidence before deriving the delta.

### Revert

Identify the target's introduced behavior, intended inverse, and dependent later changes. For a merge commit, require the recorded `-m` mainline parent before deriving the inverse. Prove absence/restoration without undoing unrelated work; compilation alone is insufficient.

## Compatibility decisions

### Compatible

Compose independent intents while preserving ordering, errors, return conventions, and side-effect boundaries. Reject false composition when it duplicates effects or validation, contradicts defaults, changes route/order precedence, masks errors, or mixes incompatible schema versions.

### Superseded

Replace a representation only with evidence: an intentional rename/migration, moved callers/tests, an explicit removal, or equivalent behavior already in the new base. Transplant still-valid intent before removing the obsolete form.

#### Empty or already-present sequencer step

For rebase/cherry-pick/revert, compare the paused delta or inverse and selected parent with current behavior and focused evidence. Marker removal or rerere alone cannot prove redundancy.

An evidence-backed no-op is a finding, **not skip authorization**:

- Preserve intentional empty history only when operation policy and the user's explicit choice require it.
- Drop the paused unit only after redundancy is proven and `skip` is explicitly authorized; finish scope does not include skip.
- If redundancy is unproven or skipping risks loss, stop; do not skip or invent an empty commit.

### Incompatible

State the real alternatives and losses:

```md
- Option A preserves <intent> but loses <behavior/risk>.
- Option B preserves <intent> but loses <behavior/risk>.
- Operation goal favors <option> because <evidence>.
- User decision required: yes/no and why.
```

Never invent an unsupported hybrid. If evidence and operation goal do not decide, use the user's decision as the primary source.

### Uncertain

Name the missing artifact—commit, PR, issue, test expectation, generator, binary source, or product decision—and stop rather than guess.

## Common conflict shapes

### Rename/delete or modify/delete

Trace whether the path was renamed, split, generated elsewhere, or intentionally removed; read both source changes; find replacement paths and callers; transplant compatible behavior; retain intentional deletion; verify topology and behavior. File existence alone does not establish intent.

### Rename/rename

Trace both destinations, their introducing commits, and current references. Keep one canonical path when both renames represent one move, or both only with evidence of an intentional split. Transplant compatible modifications before removing an obsolete destination; verify paths and callers.

### Submodule

Each gitlink stage names a submodule commit, not directory content. Inspect base/current/competing identities and submodule history. A new submodule commit is a separate repository/history mutation requiring explicit scope. Verify the selected commit exists, is reachable as expected, and preserves the superproject change.

### Same function, different features

Identify each observable behavior; compare preconditions, ordering, errors, and effects; compose only independent features; change callers/tests only as required; verify each behavior alone and together. Never concatenate blocks mechanically.

### Lockfile

Resolve dependency-manifest intent first using package-manager configuration as source, then regenerate with the pinned tool. Stop on unrelated dependency or script churn.

### Generated file

Resolve schema/template/source data and generator version/configuration, regenerate, and verify deterministic output. A generated header points to a source; it does not prove the generator is available.

Regeneration and package-manager commands are mutation boundaries, not read-only verification. Follow the baseline, authorization, isolation, hook/network/credential review, and fresh post-state procedure in [operation-state](operation-state.md) and [verification-checklist](verification-checklist.md). If effects exceed expected lockfile/generated outputs, stop; never automatically reset, clean, or roll back.

### Binary artifact

Find the producing source, release asset, or generator. If neither side is inspectable and provenance cannot decide, present choices and impact. Never claim a semantic byte merge you could not inspect.

## Silent-loss review

Before finalizing, answer:

- Which observable behavior from each side survives?
- What proves any removal is intentional?
- Did a rename hide a modification?
- Did a generator or lockfile conceal unresolved source intent?
- Did rebase absorb a later commit?
- Did cleanup add policy or unrelated refactoring?
- Which focused check would fail if retained intent were missing?

A complete rationale connects each answer to evidence, choice, authorization, and verification. Semantic no-op, marker-free content, and generated output do not by themselves prove authorized mutation or verified behavior.