---
name: resolving-merge-conflicts
description: "Use when a Git merge, rebase, cherry-pick, or revert is stopped by conflicts and the competing changes must be reconciled without losing intent. Git merge, rebase, cherry-pick, revert가 충돌로 중단되고 양쪽 의도를 보존해 해결해야 할 때."
---

# Resolving Merge Conflicts

Resolve Git conflicts as intent reconciliation, not marker deletion.

This is a technique skill for an already-stopped merge, rebase, cherry-pick, or revert. Preserve the purpose of the current operation and every compatible behavior from the competing changes. Keep history-changing actions inside the user's explicit scope.

## Non-Negotiables

```text
NO RESOLUTION WITHOUT CONFIRMING THE OPERATION AND INVENTORYING EVERY CONFLICT.
NO BLANKET OURS/THEIRS SELECTION.
NO SILENT LOSS OF EITHER SIDE'S INTENT.
NO COMPLETION CLAIM FROM MARKER REMOVAL ALONE.
NO STAGE, CONTINUE, COMMIT, OR ABORT OUTSIDE EXPLICIT USER SCOPE.
NO RESET, CLEAN, OR PUSH WITHOUT AN EXPLICIT USER REQUEST.
FAILED VERIFICATION MEANS THE RESOLUTION IS NOT COMPLETE.
```

Do not invent behavior, perform unrelated refactors, or treat a generated artifact as its own source of truth. Time pressure does not weaken these rules.

## Supporting References

Keep this file as the operating checklist. Open the supporting file only when its topic is active:

- `references/operation-state.md` — identify the active Git operation, interpret index stages, and enforce mutation boundaries.
- `references/intent-reconstruction.md` — reconstruct each side's purpose and write a hunk-level resolution rationale.
- `references/verification-checklist.md` — prove file, index, behavior, and operation state without overclaiming.

## Use When

Use this skill when conflicts have stopped an active:

- `git merge`
- `git rebase`, including an interactive rebase
- `git cherry-pick`
- `git revert`

Use it for content, add/add, rename, rename/delete, modify/delete, generated-file, lockfile, binary, or mode conflicts.

Do not use it merely to predict future conflicts, review an ordinary diff, rewrite history that is not already in progress, or choose a branch-wide merge strategy before an operation starts.

## Phase 1 — Confirm Operation and User Scope

Before editing, identify both the active operation and the authorized mutation boundary.

Classify the request as one of these scopes:

```text
resolve files only
resolve and stage exact conflict resolutions
resolve, stage, and continue the current operation
abort the current operation
```

Rules:

- A request to “resolve the conflicts” authorizes inspecting and editing the conflicted files plus focused verification. It does not by itself authorize staging, continuing, committing, aborting, resetting, cleaning, or pushing.
- An explicit request to “stage,” “mark resolved,” “continue,” or “finish this rebase/merge/cherry-pick/revert” authorizes only the named action within the currently observed operation.
- If mutation scope is ambiguous, proceed through verified working-tree resolution and stop before the ambiguous mutation. Ask only when a semantic choice or destructive action genuinely requires the user.
- Never infer permission for `reset`, `clean`, `commit`, `push`, or force-push from a request to resolve or continue.

Then inspect read-only state:

1. Confirm which operation Git reports as active.
2. Record the current branch or detached state, paused commit where applicable, and operation goal.
3. Capture staged, unstaged, untracked, and unmerged paths before changing anything.
4. Separate pre-existing unrelated work from conflict-resolution work.
5. Stop if operation metadata is absent, contradictory, or indicates a different operation than the user described.

Use `references/operation-state.md` for detection, side semantics, continuation commands, and authorization rules.

## Phase 2 — Inventory the Entire Conflict Surface

Enumerate both the unmerged index and working-tree conflict artifacts. Neither view is sufficient alone.

The inventory must include:

- every unmerged path and its conflict type
- every conflict block in text files
- marker-free conflicts such as modify/delete, rename/delete, binary, file-mode, or submodule entries
- source manifests for lockfiles
- source schemas/templates and generator commands for generated files
- pre-existing staged, modified, and untracked paths that must remain untouched

Create one conflict record per path or independently meaningful hunk:

```md
- Path / hunk:
- Conflict type:
- Current-operation source:
- Competing source:
- Intent of each side:
- Compatible, incompatible, or uncertain:
- Proposed resolution:
- Evidence and rationale:
- Required verification:
```

Do not start resolving the first visible marker while other conflict paths remain unexamined. A complete inventory prevents a locally plausible edit from contradicting another conflict.

## Phase 3 — Reconstruct Both Intents

For every record, read the primary sources before choosing content:

1. active operation metadata and paused patch
2. base and available index stages for the path
3. source commits and their messages
4. linked PRs, issues, tickets, or design material when available
5. surrounding implementation, call sites, tests, and repository instructions
6. source manifests, schemas, templates, and generator configuration

Do not trust the labels “ours” and “theirs” without mapping them to the active operation. Their practical meaning changes during rebase and may be incomplete for delete conflicts.

Apply the correct operation lens:

- **Merge:** reconcile both parent lines against the stated integration goal. Do not silently discard either parent intent.
- **Rebase:** preserve the intent of the one paused commit on the new base. Do not mix in the meaning of later, not-yet-replayed commits.
- **Cherry-pick:** preserve the selected commit's intended delta while retaining unrelated current-branch behavior.
- **Revert:** reconstruct the intended inverse of the reverted commit while preserving later/current changes.

Classify each intent pair:

- **Compatible:** compose both behaviors with the smallest coherent edit.
- **Superseded:** keep the newer representation only when history, tests, or operation purpose proves it replaces the older one; transplant still-relevant behavior.
- **Incompatible:** present the concrete tradeoff and evidence. Do not invent a third policy.
- **Uncertain:** gather more source evidence; if a product or history choice remains, ask the user before editing that hunk.

Write the resolution rationale before applying the edit. Use `references/intent-reconstruction.md` for the conflict record, evidence order, and common conflict shapes.

## Phase 4 — Apply the Smallest Semantic Resolution

Edit only what the reconstructed intents require.

### Content conflicts

Preserve independent behaviors from both sides. Reconcile imports, types, ordering, error handling, and callers as needed for those behaviors to coexist. Do not keep both text blocks mechanically if doing so duplicates execution or violates an invariant.

### Rename/delete and modify/delete conflicts

Trace why the path moved or disappeared. If one side renamed a file and the other changed still-valid behavior at the old path, transplant that behavior to the replacement path and keep the obsolete path removed. If deletion intentionally removed the behavior, preserve the deletion only when primary-source evidence supports that intent.

### Lockfile conflicts

Resolve dependency intent in the source manifest first. Use the repository's pinned package manager and normal lockfile-generation path to regenerate the lockfile when possible. Do not hand-splice lockfile sections merely to remove markers. Inspect any install-script or dependency mutation before running it.

### Generated-file conflicts

Resolve the schema, template, source data, or generator inputs first. Run the repository's existing generator, then inspect the output. Never treat a manually merged generated file as a completed resolution. If an authoritative source input is unavailable, surface the tradeoff and keep the operation paused. If all inputs are resolved but the generator is unavailable, report the missing prerequisite and verification gap instead of claiming the artifact is resolved.

### Binary or non-text conflicts

Identify the producing source and intended artifact. Regenerate or choose an artifact only from evidence. If neither side can be semantically inspected and no reproducible source exists, surface the tradeoff instead of guessing.

After each edit, update the conflict record with the actual resolution. Do not stage yet unless staging is explicitly in scope.

## Phase 5 — Verify the Working-Tree Resolution

Marker removal is the start of verification, not its conclusion.

Before any staging:

1. Confirm every inventoried text conflict has no unresolved markers.
2. Inspect every marker-free conflict path and expected rename/deletion outcome.
3. Parse or compile the touched files at the narrowest correct seam.
4. Run focused tests that exercise each preserved behavior and the current operation's intended change.
5. For applicable source-derived conflicts, regenerate artifacts and check source/output consistency.
6. For lockfile conflicts, validate manifest/lockfile consistency with the project's package manager.
7. Inspect the resulting diff for dropped behavior, duplicate behavior, accidental formatting, and unrelated changes.
8. Confirm pre-existing staged, modified, and untracked work is unchanged.

An unmerged index can remain at this point because Git records a resolution only when it is staged. Report this accurately as “working-tree resolution verified; not recorded in the index,” not “Git conflict resolved.”

If a check fails:

- keep the operation paused
- determine whether the resolution caused the failure
- revise only the responsible conflict resolution
- rerun the same check
- report unrelated or inaccessible failures precisely

Do not declare success while required verification is failing or unavailable. Use `references/verification-checklist.md` for proof layers and claim wording.

## Phase 6 — Cross the Mutation Boundary Deliberately

Staging, continuing, committing, and aborting are separate actions. Authorization for one does not imply the others.

### Stage only when explicitly authorized

Before staging, report:

- observed operation and paused commit, if any
- paths to be staged
- verification already completed
- exact staging action
- actions that remain out of scope

Stage exact resolution paths, including intended deletion/rename paths. Avoid broad staging that can capture unrelated work. Then inspect the staged diff and confirm the unmerged index is empty.

If staging exposes a missed path or stages unrelated content, stop and correct the index without destroying work.

### Continue only when explicitly authorized

Before continuation, report:

- that the index has no unmerged entries
- the checks that passed or remain unavailable
- the exact operation-specific continuation command
- whether continuation will record a commit
- whether authorization covers only this stop or the entire current operation

Then continue only the observed operation. Do not run a standalone commit merely because a continuation command will create or replay one.

If a long rebase or sequencer stops again:

1. treat the new stop as a new conflict inventory
2. reconstruct that paused commit's intent independently
3. rerun the verification and mutation gates
4. continue again only if the user's explicit scope covers the entire operation

### Abort only when explicitly chosen

Abort is a valid user option. Before aborting, state which in-progress resolution work and operation state will be discarded. Never replace a hard semantic choice with an automatic abort, and never follow an “always resolve” rule when evidence shows the operation goal is wrong.

`reset`, `clean`, `commit`, `push`, and force-push remain outside scope unless the user explicitly requests that exact action. Resolution is not publication authorization.

## Phase 7 — Prove the Observed End State

Re-read Git state after the last authorized mutation. Distinguish these outcomes:

```text
working-tree content resolved; index still unmerged by design
resolution staged; operation intentionally paused
operation continued and stopped at another conflict
operation completed; focused verification passed
operation paused because verification or intent is unresolved
operation aborted by explicit user choice
```

Report in this shape:

```md
## Operation

## Conflict Inventory

## Intent and Resolution

## Verification

## Mutation State

## Remaining Risk
```

For each conflict, connect the observed sources to the chosen resolution and verification. State exactly what was not staged, continued, committed, aborted, reset, cleaned, or pushed.

Completion requires evidence for the scope actually authorized:

- every inventoried conflict has a semantic resolution or an explicit unresolved tradeoff
- no unresolved marker remains in resolved text
- source-derived artifacts come from resolved sources
- focused syntax/type/build/test checks support the intended behavior
- failed checks are not hidden
- index state matches whether staging was authorized
- operation state matches whether continuation or abort was authorized
- unrelated work remains untouched

## Red Flags

Stop and return to the earliest violated phase if any of these appear:

- “Just take ours/theirs everywhere.”
- “The markers are gone, so it is done.”
- “The file was deleted, so the modification does not matter.”
- “This lockfile or generated file is easier to merge by hand.”
- “The tests fail, but Git accepts the resolution.”
- “A rebase conflict is just a normal merge conflict.”
- “Stage everything; we can inspect it later.”
- “Continue first and see whether it works.”
- “Never abort.”
- “The user asked to resolve, so commit or push is implied.”

These shortcuts create silent behavior loss or unauthorized history changes.