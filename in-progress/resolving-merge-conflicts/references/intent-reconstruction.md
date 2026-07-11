# Intent Reconstruction

Reconstruct what each change was trying to preserve before deciding what text survives.

## Core Rule

```text
source evidence → side intent → compatibility decision → minimal resolution → observable proof
```

Conflict markers show overlapping text. They do not show why either side changed, whether one side supersedes the other, or whether behavior moved to another path.

## Conflict Record

Create a record for each path or independently meaningful hunk:

```md
## <path>:<symbol-or-hunk>

- Conflict type: content | add/add | modify/delete | rename/delete | rename/rename | binary | mode | submodule | generated | lockfile
- Active operation and paused unit:
- Base behavior:
- Current-operation source and intent:
- Competing source and intent:
- Evidence:
- Relationship: compatible | superseded | incompatible | uncertain
- Proposed resolution:
- Behavior deliberately retained:
- Behavior deliberately removed and why:
- Verification:
```

For a multi-path rename or generated artifact, one record may link the related paths, but every unmerged index path must appear in the inventory.

## Evidence Order

Prefer the closest primary sources first:

1. paused commit patch, parent, and message
2. merge heads or selected/reverted commit
3. base and available index stages
4. for lockfile or generated conflicts, the authoritative manifest/schema/template/source data and tool configuration
5. adjacent commits that introduced the competing code
6. linked PR, issue, ticket, design decision, or migration note
7. repository instructions and documented invariants
8. current implementation, call sites, tests, and public behavior

A commit message alone is not proof when its patch, tests, or linked issue contradict it. Record uncertainty instead of smoothing over inconsistent evidence.

## Operation Lenses

### Merge

Ask:

- What integration goal caused these histories to meet?
- Which behaviors are independently required by each parent?
- Did one parent intentionally remove or replace behavior from the other?
- Can both intents coexist without duplicate execution or incompatible policy?

### Rebase

Ask:

- What exact delta did the paused commit introduce on its original parent?
- How does the new base represent the same concept now?
- Which parts of the paused delta still apply?
- Am I accidentally using a later commit to explain the current one?

The resolution should express the paused commit on the new base, not merge the whole old branch at once.

### Cherry-pick

Ask:

- What independently useful delta is being selected?
- Which current-branch behavior is unrelated and must remain?
- Has the target branch already implemented the delta under another name or path?

Do not convert a cherry-pick conflict into a broad branch merge.

### Revert

Ask:

- What behavior did the target commit introduce?
- What is the intended inverse?
- Which later changes depend on or reshape that behavior?
- Does the proposed result actually undo the target without undoing unrelated later work?

A revert resolution must prove the intended absence or restoration of behavior, not just compile.

## Compatibility Decisions

### Compatible

Compose both intents when they are independent. For example, if one side adds token-expiration validation and the other adds audience validation, preserve both while respecting established ordering, errors, and return conventions.

Watch for false composition:

- duplicated side effects
- the same validation running twice
- contradictory defaults
- route/order precedence changes
- one branch's fallback masking the other's error
- incompatible schema versions

### Superseded

One representation can replace another only with evidence. Common signals:

- an intentional rename or migration
- tests and callers moved to a replacement API
- an issue explicitly removes obsolete behavior
- the new base already implements the paused delta differently

Transplant any still-valid intent before removing the obsolete representation.

### Incompatible

When both policies cannot coexist, describe the actual choice:

```md
- Option A preserves <intent> but loses <behavior/risk>.
- Option B preserves <intent> but loses <behavior/risk>.
- Operation goal favors <option> because <source evidence>.
- User decision required: yes/no and why.
```

Do not create a hybrid policy unsupported by either change. If the operation goal and repository evidence do not settle the choice, use the user decision as the primary source.

### Uncertain

Uncertainty is a valid state, not permission to guess. Name the missing artifact: commit, PR, issue, test expectation, generator, binary source, or product decision.

## Common Conflict Shapes

### Rename/Delete or Modify/Delete

1. Trace whether the missing path was renamed, split, generated elsewhere, or intentionally removed.
2. Read the deletion/rename source and the modification source.
3. Find the replacement path and current callers.
4. Transplant still-valid behavior to the replacement when compatible.
5. Keep the obsolete path deleted when the move/removal is intentional.
6. Verify both path topology and behavior.

Choosing file existence alone loses intent.

### Rename/Rename

Trace both destination choices, the commits that introduced them, and current references. Preserve one canonical path when both renames represent the same move, or both paths only when evidence shows an intentional split. Transplant compatible modifications before removing an obsolete destination, then verify path topology and callers.

### Submodule

Treat each gitlink stage as a reference to a specific submodule commit, not as ordinary directory content. Inspect the base/current/competing commit identities and their submodule history before choosing a gitlink. If preserving both intents requires creating a new commit inside the submodule, treat that as a separate repository/history mutation requiring explicit user scope. Verify that the selected commit exists, is reachable as the project expects, and preserves the superproject change.

### Same Function, Different Features

1. Identify the observable behavior introduced by each side.
2. Check shared preconditions, ordering, error semantics, and side effects.
3. Compose both if independent.
4. Update callers/tests only when required to preserve those behaviors.
5. Verify each behavior separately and together.

Do not concatenate blocks mechanically.

### Lockfile

Treat the dependency manifest and package-manager configuration as the sources. Resolve manifest intent first, then regenerate with the pinned tool. If regeneration changes unrelated dependencies or scripts, stop and inspect rather than accepting churn.

### Generated File

Treat schemas, templates, source data, and generator version/configuration as the sources. Resolve those inputs, regenerate, and verify deterministic output. A generated header is evidence to find the source, not a guarantee the generator is available.

### Binary Artifact

Find its producing source, release asset, or generator. If neither side is inspectable and provenance cannot choose one, present the choice and impact. Never claim a semantic merge of bytes you could not inspect.

## Silent-Loss Review

Before finalizing a record, ask:

- Which observable behavior from side A survives?
- Which observable behavior from side B survives?
- If behavior was removed, which source proves removal is intentional?
- Did a rename hide a modification?
- Did a generator or lockfile conceal unresolved source intent?
- Did rebase resolution accidentally absorb a later commit?
- Did conflict cleanup introduce new policy or unrelated refactoring?
- Which focused check would fail if either retained intent were missing?

A rationale is complete only when these answers connect to evidence and verification.