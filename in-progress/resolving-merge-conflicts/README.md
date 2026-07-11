# resolving-merge-conflicts

[English](README.md) | [한국어](README.kr.md)

`resolving-merge-conflicts` is an in-progress adaptation of Matt Pocock’s resolving-merge-conflicts workflow. It treats conflicts as intent reconciliation: reconstruct both sides, apply the smallest semantic resolution, and verify behavior and operation state. It retains intent reconstruction and verification while replacing unconditional “never abort” and always-stage/commit/continue behavior with explicit user scope.

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

- `SKILL.md`: English execution contract for resolving conflicts in an already-stopped merge, rebase, cherry-pick, or revert.
- `SKILL.kr.md`: Korean counterpart to `SKILL.md`.
- `README.md`: English package manifest and provenance summary.
- `README.kr.md`: Korean counterpart to this manifest.
- `references/operation-state.md`: Operation detection, index-stage interpretation, pre-existing-work capture, and mutation authorization boundaries.
- `references/intent-reconstruction.md`: Evidence order, operation-specific intent lenses, conflict records, compatibility decisions, and silent-loss review.
- `references/verification-checklist.md`: Working-tree, index, behavioral, and operation-state proof layers and claim-to-evidence wording.

## Scope

Use this skill when an active `git merge`, `git rebase`, `git cherry-pick`, or `git revert` is paused by content, add/add, rename, modify/delete, generated-file, lockfile, binary, mode, or related conflicts. It covers complete conflict inventory, source-backed intent reconstruction, minimal semantic edits, and focused verification.

It is not for predicting future conflicts, reviewing an ordinary diff, choosing a branch-wide merge strategy before an operation starts, or rewriting history unrelated to an already-stopped operation. Never use blanket ours/theirs selection or treat marker removal alone as completion.

## Core Flow

```text
confirm operation and user scope
    → inventory every unmerged path and conflict artifact
    → reconstruct both intents from source evidence
    → apply the smallest semantic resolution
    → verify working tree, behavior, index, and operation state
    → cross staging/continuation/commit/abort boundaries only when explicitly authorized
```

Failed or unavailable required verification keeps the resolution incomplete and the operation paused; report the gap instead of overclaiming.

## Mutation Boundaries

- Editing conflicted files, required source artifacts, and running focused non-destructive verification are within “resolve the conflicts.”
- Staging exact paths, continuing the current operation, recording a standalone commit, and aborting require explicit user scope; none is implied by marker cleanup or file editing.
- `reset`, `clean`, and `push` (including force-push) require an explicit request and scope review.
- A continuation command may record or replay a commit; do not substitute a manual commit or continue automatically.

## Reference Source

This package is an in-progress adaptation of Matt Pocock’s resolving-merge-conflicts workflow, retaining intent reconstruction and verification while making mutation boundaries explicit. Revisit the upstream reference at `references/mattpocock/skills/skills/engineering/resolving-merge-conflicts/SKILL.md` when the source changes.

License notices for original repositories are covered by the root `NOTICE.md`.
