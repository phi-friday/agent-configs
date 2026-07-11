# Operation State and Mutation Boundaries

Identify the exact Git operation before interpreting sides or mutating state.
Keep intent reconciliation separate from index, history, and filesystem
mutation.

## Core rule

```text
operation identity + paused unit + complete conflict index
  + content baseline + explicit mutation scope
```

Editing, staging, continuing, committing, skipping, aborting, quitting,
resetting, cleaning, and pushing are distinct actions with distinct
authorization.

## Detect the active operation

Start with Git's state, then inspect metadata without mutating anything:

```sh
git status
git status --short
git diff --name-only --diff-filter=U
git ls-files --unmerged
git rev-parse --show-toplevel
for n in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD MERGE_AUTOSTASH; do
  p=$(git rev-parse --git-path "$n") || exit
  if test -f "$p"; then printf '%s (%s):\n' "$n" "$p"; cat "$p"
  elif test -e "$p"; then printf '%s exists at %s\n' "$n" "$p"
  else printf '%s absent at %s\n' "$n" "$p"; fi
done
for n in rebase-merge rebase-apply sequencer; do
  d=$(git rev-parse --git-path "$n") || exit
  test -d "$d" || continue
  for f in head-name onto msgnum end git-rebase-todo done autostash \
           todo head opts abort-safety; do
    test -f "$d/$f" && { printf '%s/%s:\n' "$d" "$f"; cat "$d/$f"; }
  done
done
```

The printed `--git-path` is only a location, not evidence of existence or an
active operation; linked worktrees may store metadata outside common `.git`.
For each present pseudo-ref, verify the object:

```sh
git rev-parse --verify --quiet MERGE_HEAD^{commit}
git rev-parse --verify --quiet REBASE_HEAD^{commit}
git rev-parse --verify --quiet CHERRY_PICK_HEAD^{commit}
git rev-parse --verify --quiet REVERT_HEAD^{commit}
git rev-parse --verify --quiet MERGE_AUTOSTASH^{commit}
```

Declare an operation active only when `git status`, its control directory, and any verified pseudo-ref agree. A printed/fake metadata path is not active state. Rebase may use `rebase-merge`/`rebase-apply`; multi-commit cherry-pick/revert may use `sequencer` even when the current pseudo-ref is absent. Stop when status is inactive, metadata conflicts, the request names another operation, or the paused unit/goal/options cannot be identified.

| Operation | Primary state evidence | Paused-unit evidence |
|---|---|---|
| Merge | `git status`, verified `MERGE_HEAD` | merge heads, parents, message/goal |
| Rebase | `git status`, rebase control directory | current patch, todo/done, paused commit, empty policy, autostash |
| Cherry-pick | `git status`, `CHERRY_PICK_HEAD` and/or `sequencer` | selected commit, todo/head/opts, mainline parent, remaining sequence |
| Revert | `git status`, `REVERT_HEAD` and/or `sequencer` | target commit, todo/head/opts, mainline parent, inverse, remaining sequence |

## Inventory index stages and map sides

For an unmerged path, inspect every available stage:

```sh
git show :1:path/to/file   # merge base
git show :2:path/to/file   # one operation side
git show :3:path/to/file   # competing side
```

Stages may be absent for delete, add/add, binary, mode, or rename conflicts; `git ls-files --unmerged` is authoritative. Name the source behind each side, not merely “ours” or “theirs.” For rebase, map the paused patch rather than assuming “ours” is the feature branch. For a merge-commit cherry-pick/revert, read `sequencer/opts` or equivalent command evidence and identify the selected `-m` mainline parent; stop if it is unavailable. Apply the selected delta or inverse while preserving unrelated current behavior.

## Capture the content baseline

Before editing, run the baseline set in `verification-checklist.md`; at minimum capture status, staged and unstaged binary diffs, and untracked paths. For every touched path, distinguish unrelated baseline hunks from resolution hunks and preserve staged/unstaged content independently. Cleanliness is not proof; preservation is.

## Authorization matrix

| Action | “Resolve conflicts” implies it? | Required boundary |
|---|---:|---|
| Read status, history, operation metadata | Yes | Read-only investigation |
| Edit conflicted files and required source artifacts | Yes | Resolution scope |
| Focused, non-destructive verification | Yes | Resolution proof |
| Stage exact conflict-resolution content | No | Explicit stage/mark-resolved scope, or explicit finish-current-operation scope |
| Continue | No | Explicit operation-specific continue or finish-current-operation scope |
| Skip | No | Explicit skip, paused-unit evidence, impact report |
| Abort | No | Explicit abort after impact statement |
| Quit | No | Explicit request to preserve tree/index |
| Generator/package-manager/hook/network/`exec` command | No | Explicit side-effect authorization, baseline, isolation, post-run inventory |
| Continue despite required proof gap | No | Exact gap and informed risk acceptance, if policy permits |
| Commit, reset, clean, push | No | Separate explicit request and scope review |

“Finish this operation” authorizes exact verified resolution staging plus repeated `--continue` for the observed operation—not skip, abort, quit, unrelated staging, unreported side-effectful commands, or a proof waiver. Before every continue, inspect remaining rebase/sequencer todo and applicable hooks. Disclose non-pick todo actions; require separate authorization for shell `exec`, hook, network, or other external effects not already named. Stop rather than bypass them.

## Operation transitions

Use only the command matching the observed operation. Each is a separate
mutation; re-check state afterward.

| Operation | `continue` | `skip` | `abort` | `quit` |
|---|---|---|---|---|
| Merge | `git merge --continue`: may record the merge commit and complete. | **Unsupported:** `git merge --skip` does not exist; stop. | `git merge --abort`: attempts pre-merge restoration. | `git merge --quit`: forgets metadata, keeps index/worktree. |
| Rebase | `git rebase --continue`: may record/replay and advance according to todo/empty policy. | `git rebase --skip`: discards paused commit and advances; explicit evidence/approval required. | `git rebase --abort`: resets toward pre-operation state. | `git rebase --quit`: ends metadata, preserves current `HEAD`, index, worktree. |
| Cherry-pick | `git cherry-pick --continue`: may record and advance the remaining sequence. | `git cherry-pick --skip`: discards current unit and advances. | `git cherry-pick --abort`: cancels sequence and attempts restoration. | `git cherry-pick --quit`: forgets sequence, preserves index/worktree. |
| Revert | `git revert --continue`: may record and advance the remaining sequence. | `git revert --skip`: discards current unit and advances. | `git revert --abort`: cancels sequence and attempts restoration. | `git revert --quit`: forgets sequence, preserves index/worktree. |

Before abort, quit, or completion, record autostash OID **A** (`MERGE_AUTOSTASH` or rebase `autostash`) and every pre-existing `refs/stash`/reflog OID **B**. Afterward classify A explicitly: applied cleanly, applied with conflicts, retained in operation metadata, moved to `refs/stash`, or missing/unexplained. Prove every B remains reachable with the same OID, explaining only an expected A insertion. Abort can fail to reconstruct dirty work; quit preserves current tree/index but can move A; completion can apply A and conflict. Do not claim restored/preserved/completed until baseline plus every A/B outcome is accounted. Never replace continuation with manual commit or suppress hooks/editors without authorization.

## Same-path gate and transition report

If unrelated work shares a conflicted path, do not path-stage it. `git add -p`
is not a conflict-resolution mechanism: it may report `needs merge` and leave
stages 1–3 unchanged. Proceed only with an explicit, reviewed separation plan
that constructs the exact stage-0 resolution while keeping unrelated content
outside the index, then proves both staged and working-tree diffs. Otherwise
stop before staging or continuation and report the boundary.

Before staging, continuing, skipping, aborting, quitting, or a side-effectful
command, report:

```md
- Active operation, verified control metadata, remaining todo/options:
- Paused unit and selected mainline parent:
- Baseline HEAD/relevant refs/index/staged/unstaged/untracked content:
- Autostash OID and pre-existing `refs/stash` identity:
- Same-path unrelated hunks and current conflict state:
- Verification completed and required gaps:
- Pending `exec`/hook/network effects and authorization:
- Exact next mutation and expected history/index/worktree/stash effect:
- Actions still out of scope:
```

After every transition or side-effectful command, run the full gate refresh from `verification-checklist.md`: compare HEAD/relevant refs, index stages, tracked/untracked/ignored content identities, operation/sequencer metadata, and autostash/stash state. Record completed, continued-to-new-conflict, cleanly advanced, paused, skipped, aborted, or quit without reusing pre-transition evidence.