# Verification Checklist

Prove four distinct layers: working-tree content, index state, intended behavior, and operation state.

## Core Rule

```text
marker-free ≠ staged ≠ behaviorally correct ≠ operation complete
```

Match every completion claim to the layer actually observed.

## Layer 1 — Working-Tree Resolution

Run before staging is authorized.

### Conflict coverage

- Every path from the original unmerged inventory has a resolution record.
- Every text conflict block is removed from the intended working-tree result.
- Modify/delete, rename/delete, add/add, binary, mode, and submodule conflicts were inspected even if no marker existed.
- Related replacement paths, source manifests, schemas, templates, and generator inputs were included where required.

### Semantic review

- Each side's intended behavior is preserved, deliberately superseded, or reported as an unresolved tradeoff.
- No blanket side selection discarded unrelated hunks.
- No unrelated refactor, formatting sweep, dependency change, or behavior was introduced.
- Pre-existing staged, unstaged, and untracked work remains unchanged.

### Syntax and source-derived artifacts

- Touched source parses or compiles at the narrowest correct seam.
- Imports, types, file modes, and path references are coherent.
- Generated output was produced from resolved source inputs with the repository's existing generator.
- Lockfiles were produced from resolved manifests with the pinned package manager when regeneration was available.
- A second generation/check does not reveal unexplained nondeterminism or unrelated churn.

At this layer the index can still report unmerged paths. Say:

```text
Working-tree resolution verified; Git index remains unmerged because staging was not authorized.
```

Do not say the Git conflict is fully resolved.

## Layer 2 — Index Resolution

Run only after explicit staging authorization.

- Stage exact resolution paths and intended deletions/renames.
- Inspect the staged diff, not only the working-tree diff.
- Confirm no unrelated path or pre-existing change was captured.
- Confirm the unmerged index is empty.
- Confirm staged content still contains the verified resolution.
- Run whitespace/patch checks appropriate to the repository.

If any unmerged entry remains, the conflict is not recorded as resolved. If unrelated content was staged, correct the index without discarding the working tree.

Valid claim:

```text
All inventoried conflicts are staged and the operation remains paused.
```

This does not claim the operation continued or completed.

## Layer 3 — Behavioral Resolution

A syntactically valid merge can still silently lose functionality.

Map each retained intent to an observable check:

| Intent shape | Required proof |
|---|---|
| Independent function behavior | Focused test for each side plus their combined path |
| Rename with incoming modification | Replacement path contains the change; old path/reference topology is correct |
| Dependency change | Manifest and lockfile agree; relevant build/import/test succeeds |
| Generated API/schema | Source contains both intended changes; generator succeeds; output exposes both |
| Revert | Target behavior is absent/restored as intended while later behavior remains |
| Rebase/cherry-pick delta | The paused commit's observable change works on the current base |

Prefer repository-declared checks in this order when relevant:

1. focused regression or feature tests
2. parser or syntax check
3. typecheck or compile
4. focused integration/build check
5. broader test/lint/format checks required by repository policy

Formatting is not semantic proof. If a formatter changes unrelated files, do not stage them as part of conflict resolution.

### Failed or unavailable checks

When a check fails:

1. record the exact command and failure
2. determine whether the resolution caused it
3. fix only resolution-caused failures
4. rerun the same check
5. keep the operation paused if required proof still fails

When a check cannot run, name the missing dependency, environment, credential, generator, or fixture. Replace it with a narrower valid check only if that check proves the same contract; otherwise report the verification gap.

## Layer 4 — Operation State

Run after the last authorized mutation-boundary decision, including a decision to stop before staging or continuation.

Read fresh Git state and record three independent dimensions:

**Content/index state**

- working-tree content edited while the index intentionally remains unmerged
- exact resolution staged with no unmerged index entries
- new unmerged entries appeared after continuation

**Operation state**

- original operation active and not advanced
- original operation active and advanced to a later sequencer step
- original operation inactive because it completed
- original operation inactive because the user explicitly aborted it

**Pause reason**

- user-authorized scope ended
- verification failed or remains unavailable
- intent remains unresolved
- continuation stopped at a new conflict
- none

Use “completed” only when the original operation is no longer active. Use “advanced” only when that operation remains active and no new unmerged entry exists. Record “aborted” only after the explicit abort action was observed. Keeping these dimensions separate prevents a staged-but-failing resolution or a new conflict from being mislabeled as ordinary progress.

For a completed operation, verify:

- Git reports no active operation of the original type
- no unmerged index entry remains
- expected commits or merge result exist without an extra manual commit
- focused behavior checks still pass after any later sequencer steps
- unrelated pre-existing work is preserved

A clean worktree is not required if it was not clean beforehand.

## Claim-to-Evidence Matrix

| Claim | Minimum fresh evidence |
|---|---|
| “Markers removed” | marker search and direct inspection of all text conflicts |
| “Working-tree resolution verified” | complete inventory, semantic rationale, focused file/artifact checks |
| “Conflicts staged” | staged diff inspected and unmerged index empty |
| “Behavior preserved” | checks mapped to both sides' observable intents |
| “Operation advanced” | continuation result plus fresh Git state |
| “Operation complete” | no active operation/unmerged entries plus post-continuation behavior checks |
| “Operation aborted” | explicit user choice, stated discard impact, fresh Git state |

Never use evidence from before the last generator run, edit, stage, continuation, or abort to support a later-state claim.

## Final Evidence Record

```md
## Verification

- Original conflict inventory:
- Marker/non-text coverage:
- Syntax/type/build checks:
- Intent A behavior check:
- Intent B behavior check:
- Generated/lockfile consistency:
- Staged diff and unmerged-index state:
- Current Git operation state:
- Checks unavailable or failing:
- Unrelated work preservation:
```

If any required row lacks evidence, scope the result accordingly instead of declaring completion.