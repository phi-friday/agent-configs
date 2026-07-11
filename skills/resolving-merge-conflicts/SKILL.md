---
name: resolving-merge-conflicts
description: "Use when a Git merge, rebase, cherry-pick, or revert is stopped by conflicts and the competing changes must be reconciled without losing intent. Git merge, rebase, cherry-pick, revert가 충돌로 중단되고 양쪽 의도를 보존해 해결해야 할 때."
---

# Resolving Merge Conflicts

Resolve an already-stopped merge, rebase, cherry-pick, or revert by reconciling intent, not deleting markers. Preserve compatible behavior and stay inside the user's explicit mutation scope.

## Non-Negotiables

```text
CONFIRM THE OPERATION; A METADATA PATH IS NOT PROOF THAT METADATA EXISTS.
INVENTORY EVERY UNMERGED PATH, INCLUDING MARKER-FREE CONFLICTS.
NO BLANKET OURS/THEIRS SELECTION OR SILENT INTENT LOSS.
PRESERVE PRE-EXISTING WORK AT CONTENT/HUNK GRANULARITY.
STAGE, CONTINUE, SKIP, ABORT, QUIT, COMMIT, RESET, CLEAN, AND PUSH REQUIRE THEIR OWN SCOPE.
SIDE-EFFECTFUL GENERATORS, HOOKS, AND PACKAGE-MANAGER COMMANDS ARE MUTATIONS.
MARKER-FREE, STAGED, BEHAVIORALLY VERIFIED, AND OPERATION-COMPLETE ARE DIFFERENT CLAIMS.
```

Do not invent behavior, perform unrelated refactors, or treat generated output as its own source of truth.

## Supporting References

- `references/operation-state.md` — evidence, index stages, baselines, authorization, and exact transitions
- `references/intent-reconstruction.md` — intent evidence, compatibility decisions, conflict shapes, and automated-resolution provenance
- `references/verification-checklist.md` — working-tree, index, behavior, side-effect, and end-state proof

Open only the sections needed for the active conflict.

## Workflow

### 1. Confirm Operation, Scope, and Baseline

Treat `git status` as primary evidence. `git rev-parse --git-path` only locates possible metadata; verify that it exists and agrees with status. Stop if no supported operation is active or evidence is contradictory.

Record the operation, branch/detached state, paused unit, goal, staged/unstaged/untracked/unmerged content, and the HEAD/ref/index/stash identities required by the references. Identify unrelated content or hunks that must survive.

Authorization is per action. “Resolve the conflicts” permits investigation, scoped edits, and non-destructive checks. “Finish this operation” permits exact verified resolution staging at each stop plus repeated `continue`, but not unrelated staging, `skip`, `abort`, or `quit`. Standalone `commit`, `reset`, `clean`, and publication need separate requests.

Flag unrelated work in a conflicted path before editing; path-wide staging would capture it.

### 2. Inventory the Conflict Surface

Before the first marker, inventory every unmerged path, available index stage, and conflict type; all text markers and marker-free add/add, modify/delete, rename, binary, mode, symlink, and submodule conflicts; authoritative lockfile/generated inputs; related replacement paths/callers; and unexpected rerere/custom-driver results when evidence indicates them.

Use a concise rationale for a simple compatible hunk. For complex, multi-path, incompatible, or uncertain cases, record sources, both intents, compatibility, unrelated baseline content, chosen resolution, deliberately removed behavior, and required proof.

### 3. Reconstruct Intent

Follow the primary-source precedence in `references/intent-reconstruction.md`, then map “ours” and “theirs” through the active operation:

- **Merge:** reconcile parent intents against the integration goal.
- **Rebase:** replay only the paused commit's still-applicable delta.
- **Cherry-pick:** apply the selected delta while preserving unrelated current behavior.
- **Revert:** apply the intended inverse while preserving later/current changes.

Compose compatible intent, require evidence for supersession, expose incompatible choices, and stop rather than guess. For an empty or already-present rebase/cherry-pick/revert step, distinguish intentional empty history, safe redundancy, and unresolved loss; redundancy never authorizes `skip`.

### 4. Apply the Smallest Semantic Resolution

Edit only what the evidence requires. Preserve ordering, errors, types, modes, callers, and side effects. Do not concatenate both blocks mechanically or discard a modification merely because the other side renamed or deleted its path.

Resolve authoritative inputs before lockfiles or generated output. Before running a package manager or generator, inspect its hooks, network/credential use, and outputs; capture a baseline and isolate it when practical. Wider effects need explicit authorization. Unexpected churn means stop and inspect—not stage, reset, or clean.

Do not stage without exact staging authorization.

### 5. Verify Four Layers

Prove working-tree content → index content → intended behavior → operation state. Before staging, account for every inventoried path, run the narrowest valid parse/compile/type check, exercise retained intents together, verify source-derived output, and compare all resulting paths/hunks with baseline.

Required proof directly covers intent; an equivalent substitute proves the same contract at the same boundary; optional checks add broader coverage. Fix resolution-caused failures. If required proof is unavailable, report the exact gap and pause—an earlier continue request is not informed acceptance. Where policy permits, the user may explicitly accept the named risk, but the result remains behaviorally unverified.

### 6. Stage and Transition Deliberately

Stage only exact authorized content. Never path-stage a conflicted file containing unrelated edits; without a reviewed separation plan and stage-0 proof, stop before staging or continuation.

`Continue` may record/replay and advance. `Skip` exists only for rebase/cherry-pick/revert, omits the paused unit, and needs evidence plus explicit drop authorization. `Abort` attempts restoration but may fail to reconstruct pre-existing work. `Quit` ends metadata while preserving the current working tree/index; autostash still requires identity-based verification.

Before transition, report the exact command, paused unit, authorization, staged content, proof gaps, pending todo/sequence effects, applicable hooks, autostash/stash identity, and expected history/index/worktree effect. `Finish` does not authorize unreported `exec` or hook side effects. Never bypass hooks or substitute manual commit. Use a compact refresh after ordinary edits and a full gate refresh after stage, side-effectful command, or transition.

## Report the Observed State

Use scoped outcomes:

```text
working-tree resolution verified; index remains unmerged
exact resolution staged; operation remains paused
operation continued and stopped at a new conflict
paused unit explicitly skipped; fresh state observed
operation inactive after continuation; required behavioral proof unavailable
operation completed with required focused proof and verified autostash outcome
operation aborted; baseline restored and autostash A/pre-existing stash B outcomes explicitly accounted
operation quit; tree/index preserved and autostash A/pre-existing stash B identities accounted
```

Report:

```md
## Operation
## Conflict Inventory
## Intent and Resolution
## Verification
## Mutation State
## Remaining Risk
```

State what was not staged, continued, skipped, aborted, quit, committed, reset, cleaned, or pushed.
