# Verification Checklist

Prove four layers separately: working-tree content, index state, intended behavior, and operation state.

## Core rule

```text
marker-free ≠ staged ≠ behaviorally correct ≠ operation complete
```

Match each claim to its layer and observed evidence. A clean worktree is not success if it was not clean at baseline.

## Baseline commands — define once, reuse fresh

Create one immutable full baseline before editing:

```sh
git status --short
git status
git rev-parse HEAD
git symbolic-ref --quiet HEAD
git ls-files -s
git ls-files --others --exclude-standard
git diff --name-only --diff-filter=U
git ls-files --unmerged
git diff --binary --no-ext-diff --unified=0
git diff --cached --binary --no-ext-diff --unified=0
git diff --binary --no-ext-diff --unified=0 -- <path>
git diff --cached --binary --no-ext-diff --unified=0 -- <path>
git show :1:<path>
git show :2:<path>
git show :3:<path>
git rev-parse --git-path MERGE_HEAD
git rev-parse --git-path REBASE_HEAD
git rev-parse --git-path CHERRY_PICK_HEAD
git rev-parse --git-path REVERT_HEAD
git rev-parse --git-path MERGE_AUTOSTASH
git rev-parse --git-path rebase-merge
git rev-parse --git-path rebase-apply
git rev-parse --git-path sequencer
git rev-parse --verify --quiet refs/stash
git reflog show --format=%H refs/stash
```

Inspect each metadata/control path for existence and contents. Record relevant branch/ref identities, index stages, and every affected path's mode/content or hash. Hash relevant untracked, binary, and scoped ignored files with a file-aware tool or `git hash-object -- <path>` without exposing secret content.

After an ordinary edit, use a **compact refresh**: status, unmerged index, operation metadata, and diffs/hashes only for paths changed since the previous snapshot. Before and after staging, a side-effectful command, or a transition, use a **full gate refresh** of all affected tracked/untracked/ignored content plus HEAD/refs/index/stash/autostash/control metadata. Stages or refs may be absent; record absence instead of inferring intent.

## Layer 1 — Working-tree resolution

Run before staging authorization.

### Coverage and marker triage

- Record a resolution for every original unmerged path (including marker-free paths) and every meaningful hunk.
- Inspect modify/delete, rename/delete, rename/rename, add/add, binary, mode, and submodule conflicts; include related replacements, manifests, schemas, templates, and generator inputs when required by intent.

Use these read-only checks; reuse baseline inventory commands:

```sh
git status --porcelain=v2
git diff --check
git grep -n -I -E '^(<<<<<<<|=======|>>>>>>>)' -- .
git grep --no-index -n -I -E '^(<<<<<<<|=======|>>>>>>>)' -- <path>
```

Marker search is not proof: it searches tracked text; can produce false positives in docs/tests/templates/escaped examples/generated output; and can miss binary, modify/delete, rename, mode, submodule, out-of-scope, or nonstandard-style conflicts. Inspect reported lines and compare the complete unmerged inventory; marker absence never substitutes for inventory.

### Content and semantic review

Record each side as preserved, deliberately superseded, or an unresolved tradeoff. No blanket side selection, unrelated refactor/formatting, dependency change, or lost baseline path/hunk. The index may remain unmerged here. Valid claim:

```text
Working-tree resolution verified; Git index remains unmerged because staging was not authorized.
```

Do not call the Git conflict fully resolved.

### Same-path unrelated edits — staging gate

Path identity is not hunk identity. For a conflicted path with unrelated work:

- Never use `git add <path>`, `git add -A`, or another path-wide staging operation.
- Do not treat `git add -p` as a resolution method; it may report `needs merge` while leaving index stages 1–3 unchanged.
- Proceed only with an explicit, reviewed separation plan that stages the exact stage-0 resolution, keeps unrelated content outside the index, and proves both staged and working-tree diffs against baseline.
- If that proof is unavailable, stop before staging/continuation and report the overlap. If unrelated content was staged, stop; never automatically reset, clean, checkout, stash, or run `git restore --staged` without explicit correction scope.

## Layer 2 — Index resolution

Run only after explicit authorization and only for its exact scope.

- Stage the exact resolution and intended deletions/renames. For same-path unrelated work, use only the reviewed Layer 1 separation plan.
- Inspect the cached diff against baseline. For every inventoried path, inspect `git ls-files -s -- <path>`: require exactly one intended stage-0 mode/blob, or no entry for an intentional deletion; compare its content identity with the verified resolution.
- Prove `git ls-files --unmerged` and `git diff --name-only --diff-filter=U` are empty. These prove stages 1–3 are gone; the per-path stage-0/intentional-deletion check proves what replaced them.

Any unmerged entry or unrelated staged content means pause and report; do not widen scope or destructively clean up. Valid claim:

```text
All inventoried conflicts are staged and the operation remains paused.
```

This does not claim continuation or completion.

## Layer 3 — Behavioral resolution

Map retained and deliberately removed intent to observable contracts; a syntactically valid merge can lose functionality.

### Proof classes

| Class | Rule and allowed claim |
|---|---|
| **Required** | Policy/intent requires this observable proof; a fresh pass is required for “behaviorally verified” or “complete.” |
| **Equivalent** | If the original cannot run, substitute only a proof of the same contract at the same boundary; record equivalence/limits or report a gap. |
| **Optional** | Broader out-of-scope coverage (full-suite, integration, lint, format); may remain unrun with an honest report. |

An unavailable required proof is not waived by “continue” or “finish.” Record exact command, missing credential/dependency/fixture, uncovered contract, and substitute. Keep paused unless policy permits advancement after informed explicit acceptance naming that gap and risk. Even then, never call the result behaviorally verified, behavior preserved, or complete; an accepted gap remains an accepted gap.

### Intent-to-proof map

| Intent | Required evidence |
|---|---|
| Function behavior | Focused proof for each side and combined path |
| Rename + modification | Replacement contains change; old path/reference topology is correct |
| Dependency change | Manifest/lockfile agree; relevant build/import/test succeeds |
| Generated API/schema | Source contains both intents; approved generation exposes both |
| Revert | Target behavior absent/restored while later behavior remains |
| Rebase/cherry-pick | Paused commit's observable change works on current base |

Prefer relevant repository checks: focused regression/feature test; parser/syntax; typecheck/compile; focused integration/build; broader policy-required check. Formatting is not semantic proof; unrelated formatter churn is not resolution content.

For failure, record exact command/result/failure; determine whether resolution caused it; fix only caused failures; rerun from fresh state; and stay paused while required proof fails. If unavailable, name missing environment, credential, generator, or fixture; do not relabel a narrower syntax check as the unavailable integration proof.

### Side-effectful commands

Generators, package managers, hooks, rebase `exec`, and network-capable checks are mutating when they can write files, change index/history/refs/stash, alter caches, or create external effects.

**Before:** run a full gate refresh; inventory known/scoped ignored roots with `git status --short --ignored=matching -- <output-root>` and content-hash every existing file beneath them; inspect scripts, todo, hooks, tool/config, network/external effects; isolate when possible or obtain explicit authorization for the exact effects.

**After:** repeat the full gate refresh and ignored-output hashes. Compare HEAD/relevant refs, index stages, stash/autostash, operation metadata, and every affected path with baseline. Unexpected or irreversible external effects mean paused report—never stage, continue, roll back, or hide them automatically.

## Layer 4 — Operation state

`continue`, `skip`, `abort`, and `quit` are distinct. “Finish the operation” authorizes exact verified resolution staging plus repeated `continue`, but not skip/abort/quit, unrelated staging, unreported side effects, or work after completion.

Before continue, inspect remaining rebase/sequencer todo, selected mainline/options, and applicable hooks. Obtain separate authorization for unreported `exec`, hook, network, or external effects; stop rather than bypass them. After any action, use fresh gate evidence and map claims to the resulting paused unit.

Keep content/index, operation state, and pause reason separate. Call a state **advanced** only when the operation remains active after authorized continue and no new unmerged entry exists; use **continued to a new conflict** when new unmerged entries appear.

Approve `skip` explicitly before action after proving redundancy. Before abort/quit, record autostash A and all pre-existing stash OIDs B. After abort classify A as applied cleanly, apply-conflicted, retained, moved, or unexplained; compare baseline tree/index/untracked content and prove every B remains reachable unchanged. After quit, prove control metadata ended, tree/index stayed unchanged, A was retained or moved as expected, and every B remains reachable. Any unexplained A/B or baseline difference blocks restored/preserved claims.

Use **completed** only when the original operation/control metadata is inactive, expected HEAD/history exists, no unmerged entry remains, required post-continuation proofs pass, all skipped units have approval/redundancy evidence, autostash outcome is verified, and unrelated baseline content is preserved.

## Claim-to-evidence matrix

| Claim | Minimum fresh evidence |
|---|---|
| Markers removed | Marker search, direct review, complete unmerged/non-text inventory |
| Working-tree resolution verified | Baseline path/hunk inventory, semantic rationale, required focused checks |
| Conflicts staged | Explicit authorization, inspected staged diff, empty unmerged index |
| Behavior preserved | Required checks mapped to both intents, or justified equivalent |
| Operation advanced | Authorized continue, no new unmerged entry, refreshed history/control state |
| Operation complete | Inactive control state, expected history, empty unmerged index, required proofs, verified skips/autostash |
| Operation skipped | Pre-action approval, discarded-unit evidence, fresh state |
| Operation aborted | Explicit abort/risk, baseline comparison, classified A outcome, every B OID preserved |
| Operation quit | Explicit preservation request, ended metadata, unchanged tree/index, classified A and preserved B OIDs |

Never use evidence from before the last edit, side-effectful command, stage, continue, skip, abort, or quit for a later claim.

## Final evidence record

```md
## Verification

- Operation, paused unit, todo/options/mainline:
- Baseline HEAD/refs/index/stash/autostash and affected content identities:
- Marker/unmerged checks and false-positive review:
- Intent records, tradeoffs, required/equivalent/optional proof:
- Side-effect/`exec`/hook authorization and pre/post inventory:
- Cached diff, exact stage-0 or intentional-deletion proof:
- Last transition, fresh control/history/content state:
- Failures/gaps, informed acceptance, pause reason:
```

If any required row lacks evidence, pause and scope the result. A generic continue request is not a waiver. An accepted gap must never be called behaviorally verified or complete.
