# resolving-merge-conflicts

[English](README.md) | [한국어](README.kr.md)

`resolving-merge-conflicts` is an in-progress adaptation of Matt Pocock’s resolving-merge-conflicts workflow. It reconciles competing intent, preserves compatible behavior, and makes mutation scope explicit.

## File Layout

```text
resolving-merge-conflicts/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ operation-state.md
   ├─ intent-reconstruction.md
   └─ verification-checklist.md
```

## File Roles

- `SKILL.md` / `SKILL.kr.md`: mirrored English and Korean execution contracts.
- `README.md` / `README.kr.md`: mirrored package manifests and provenance summaries.
- `references/operation-state.md`: operation evidence, index stages, baselines, and authorization boundaries.
- `references/intent-reconstruction.md`: intent evidence, compatibility decisions, conflict shapes, and silent-loss review.
- `references/verification-checklist.md`: working-tree, index, behavior, side-effect, and operation-state proof.

## Scope

Use for an active `git merge`, `git rebase`, `git cherry-pick`, or `git revert` paused by content or marker-free conflicts, including add/add, rename, modify/delete, generated-file, lockfile, binary, mode, symlink, and submodule cases. The package covers inventory, source-backed intent reconstruction, minimal semantic resolution, and focused proof.

It is not for predicting conflicts, ordinary diff review, choosing a branch-wide strategy before an operation starts, or unrelated history rewriting. Never use blanket ours/theirs selection or treat marker removal alone as completion.

## Core Flow

```text
confirm operation, scope, and baseline
    → inventory every unmerged path and conflict artifact
    → reconstruct compatible intents from source evidence
    → apply the smallest semantic resolution
    → verify working tree, index, behavior, and operation state
    → stage or transition only at separately authorized boundaries
```

Classify proof as required (directly proves retained intent or the paused delta), equivalent (proves the same contract at the same boundary), or optional (broader coverage). If required proof fails or is unavailable, report the exact gap and keep the operation paused; explicit informed acceptance of that named risk may authorize a user-requested progression, but the result remains behaviorally unverified.

## Mutation Boundaries

- Editing conflicted files, required source artifacts, and focused non-destructive checks is within conflict resolution.
- Generators, hooks, and package-manager commands that can rewrite files, update lockfiles, or use the network are side-effectful mutations: inspect their effects, resolve authoritative sources first, and run them only with scope to do so.
- If unrelated work shares a conflicted path, stop before path staging. Interactive hunk staging alone is insufficient; proceed only with a reviewed plan that constructs and proves the exact stage-0 resolution while keeping unrelated content outside the index.
- Plain conflict resolution does not stage. An explicit finish-current-operation request covers exact verified conflict staging plus repeated continuation. Standalone commit, unrelated staging, `reset`, `clean`, and `push` each require separate scope.

Transitions are independent and explicit:

| Action | Boundary |
| --- | --- |
| `continue` | Record/replay and advance after pending todo/hook effects are inspected and authorized. |
| `skip` | Omit a rebase/cherry-pick/revert unit only with redundancy evidence and explicit drop authorization; merge has no skip. |
| `abort` | Attempt restoration; classify autostash A as applied/conflicted/retained/moved and prove every pre-existing stash OID B remains reachable. |
| `quit` | End metadata while preserving tree/index; classify A retention/movement and prove every B remains reachable. |

Do not substitute a manual commit or bypass hooks. Use compact refreshes after ordinary edits and full gate refreshes after staging, side-effectful commands, and transitions.

## Reference Source

This package is an in-progress adaptation of Matt Pocock’s resolving-merge-conflicts workflow, retaining intent reconstruction and verification while making mutation boundaries explicit. Revisit the [upstream reference](../../references/mattpocock/skills/skills/engineering/resolving-merge-conflicts/SKILL.md) when the source changes.

License notices for original repositories are covered by the root `NOTICE.md`.
