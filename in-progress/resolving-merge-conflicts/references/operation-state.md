# Operation State and Mutation Boundaries

Identify the exact Git operation before interpreting sides or mutating its state.

## Core Rule

```text
operation identity + paused unit + complete conflict index + explicit mutation scope
```

A conflict resolution is not one atomic action. Editing files, staging paths, continuing a sequencer, recording a commit, aborting, resetting, cleaning, and pushing have different effects and require separate authorization.

## Detect the Active Operation

Start with Git's own status and path resolution rather than assuming `.git` is a directory. A linked worktree may store operation metadata elsewhere.

Useful read-only evidence includes:

```sh
git status --short
git status
git diff --name-only --diff-filter=U
git ls-files --unmerged
git rev-parse --show-toplevel
git rev-parse --git-path MERGE_HEAD
git rev-parse --git-path REBASE_HEAD
git rev-parse --git-path CHERRY_PICK_HEAD
git rev-parse --git-path REVERT_HEAD
```

Use operation-specific evidence:

| Operation | Primary state evidence | Paused-unit evidence |
|---|---|---|
| Merge | `git status`, `MERGE_HEAD` | merge heads, parent commits, merge message/goal |
| Rebase | `git status`, rebase metadata, often `REBASE_HEAD` | `git rebase --show-current-patch`, todo/done state, paused commit |
| Cherry-pick | `git status`, `CHERRY_PICK_HEAD` | selected commit and its parent/delta |
| Revert | `git status`, `REVERT_HEAD` | target commit, inverse patch, later/current changes |

Do not infer an operation from conflict markers alone. A file can contain old markers with no active operation, and modify/delete or binary conflicts can have no markers.

Stop before editing when:

- Git reports no active merge, rebase, cherry-pick, or revert
- metadata for multiple operations appears inconsistent
- the operation differs from the user's description and the difference changes the intended resolution
- the paused commit or merge goal cannot be identified well enough to interpret the conflict

## Inventory Index Stages

For an unmerged path, Git's index may expose:

```text
stage 1: merge base
stage 2: one operation side
stage 3: the competing operation side
```

Inspect available stages without assuming all three exist:

```sh
git show :1:path/to/file
git show :2:path/to/file
git show :3:path/to/file
```

Delete, add/add, binary, mode, and rename-related conflicts can omit a stage or represent intent across more than one path. `git ls-files --unmerged` is the authoritative inventory of index stages; the working-tree marker layout is only one rendering.

## Map Sides Through the Operation

Do not write a rationale that merely says “ours” or “theirs.” Name the actual source.

### Merge

Stage 2 commonly corresponds to current `HEAD`; stage 3 corresponds to a merged head. Verify this against commit content and the merge heads, especially for octopus or unusual merges.

### Rebase

The practical labels are counterintuitive: one side commonly reflects the new base plus already-replayed commits, while the other reflects the commit currently being replayed. Use the current patch and commit identity to map each stage. Never treat “ours” as automatically meaning the user's feature branch.

Resolve only the paused commit's intent. Later commits in the rebase may change the same code but are not part of this stop yet.

### Cherry-pick

Interpret the conflict as the selected commit's delta applied to current `HEAD`. Preserve unrelated current-branch behavior while retaining the picked delta that remains applicable.

### Revert

Interpret the conflict as an inverse change applied to current `HEAD`. Verify that the result intentionally undoes the target behavior while retaining changes made after the target commit.

## Capture Pre-Existing Work

Before editing, record:

- already-staged paths unrelated to the conflict
- unstaged modifications unrelated to the conflict
- untracked files
- files modified by generators or package-manager commands during resolution

Do not use a clean final worktree as the success criterion when unrelated work existed before the operation. The invariant is preservation, not emptiness.

## Authorization Matrix

| Action | Implied by “resolve the conflicts”? | Required boundary |
|---|---:|---|
| Read status, history, operation metadata | Yes | Read-only investigation |
| Edit conflicted files and their required source artifacts | Yes | Conflict-resolution scope |
| Run focused, non-destructive verification | Yes | Resolution proof |
| Stage exact resolution paths | No | Explicit stage/mark-resolved/finish scope |
| Continue merge/rebase/cherry-pick/revert | No | Explicit continue/finish-current-operation scope |
| Record a standalone commit | No | Explicit commit request |
| Abort the operation | No | Explicit abort choice after impact is stated |
| Reset or clean | No | Explicit destructive request and path/scope review |
| Push or force-push | No | Explicit publication request |

If the user explicitly asks to finish the entire current operation, that scope can cover later stops in the same operation. Each stop still requires a new inventory, intent reconstruction, verification, and pre-continuation state report. It does not authorize work after the observed operation completes.

## Continuation Effects

| Operation | Normal continuation | Important effect |
|---|---|---|
| Merge | `git merge --continue` | Can create the merge commit |
| Rebase | `git rebase --continue` | Records/replays the paused commit and advances the sequencer |
| Cherry-pick | `git cherry-pick --continue` | Records the picked commit and advances a sequence if present |
| Revert | `git revert --continue` | Records the revert and advances a sequence if present |

Use the command that matches observed state. Do not run a manual `git commit` merely because continuation records a commit. Do not suppress commit hooks or editors unless the user or repository workflow authorizes that behavior.

## Pre-Mutation Report

Before staging, continuing, committing, or aborting, report:

```md
- Active operation:
- Paused unit:
- Current conflict/index state:
- Verification completed:
- Exact next mutation:
- Expected history/worktree effect:
- Actions still out of scope:
```

If authorization is already explicit, this report is notice and evidence, not a redundant approval request. If authorization is absent, stop before the mutation.