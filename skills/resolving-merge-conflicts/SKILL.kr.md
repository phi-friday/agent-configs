---
name: resolving-merge-conflicts
description: "Use when a Git merge, rebase, cherry-pick, or revert is stopped by conflicts and the competing changes must be reconciled without losing intent. Git merge, rebase, cherry-pick, revert가 충돌로 중단되고 양쪽 의도를 보존해 해결해야 할 때."
---

# Resolving Merge Conflicts

이미 중단된 merge, rebase, cherry-pick, 또는 revert를 marker를 삭제하는 대신 의도를 조정해 해결한다. 호환되는 동작은 보존하고 사용자가 명시한 mutation scope 안에 머문다.

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

동작을 지어내거나 관련 없는 refactor를 수행하지 않으며, generated output을 자체 source of truth로 취급하지 않는다.

## Supporting References

- `references/operation-state.md` — evidence, index stages, baselines, authorization, exact transitions를 다룬다.
- `references/intent-reconstruction.md` — intent evidence, compatibility decisions, conflict shapes, automated-resolution provenance을 다룬다.
- `references/verification-checklist.md` — working-tree, index, behavior, side-effect, end-state proof를 다룬다.

현재 conflict에 필요한 섹션만 연다.

## Workflow

### 1. Confirm Operation, Scope, and Baseline

`git status`를 primary evidence로 취급한다. `git rev-parse --git-path`는 가능한 metadata의 위치만 찾으므로, 해당 metadata가 실제로 존재하고 status와 일치하는지 확인한다. 지원되는 operation이 active가 아니거나 evidence가 모순되면 멈춘다.

operation, branch/detached state, paused unit, goal, staged/unstaged/untracked/unmerged content와 references가 요구하는 HEAD/ref/index/stash identity를 기록한다. 계속 보존해야 하는 unrelated content 또는 hunk를 식별한다.

Authorization은 action별로 적용된다. “Resolve the conflicts”는 investigation, scoped edits, non-destructive checks를 허용한다. “Finish this operation”은 각 stop의 exact verified resolution staging과 반복되는 `continue`를 허용하지만 unrelated staging, `skip`, `abort`, `quit`은 포함하지 않는다. Standalone `commit`, `reset`, `clean`, publication에는 별도 요청이 필요하다.

conflicted path의 unrelated work는 편집 전에 표시한다. path-wide staging은 그것까지 포착하기 때문이다.

### 2. Inventory the Conflict Surface

첫 marker를 처리하기 전에 모든 unmerged path, 사용 가능한 index stage, conflict type, 모든 text marker와 marker-free add/add, modify/delete, rename, binary, mode, symlink, submodule conflict, authoritative lockfile/generated input, related replacement path/caller, evidence가 가리키는 unexpected rerere/custom-driver result를 inventory한다.

단순하고 호환되는 hunk에는 간결한 rationale을 사용한다. 복잡하거나 여러 path에 걸치거나 incompatible 또는 uncertain한 경우에는 source, 양쪽 intent, compatibility, unrelated baseline content, chosen resolution, 의도적으로 제거한 behavior, required proof를 기록한다.

### 3. Reconstruct Intent

`references/intent-reconstruction.md`의 primary-source precedence를 따른 뒤 “ours”와 “theirs”를 active operation을 통해 해석한다.

- **Merge:** integration goal에 맞춰 parent intent를 조정한다.
- **Rebase:** paused commit에서 여전히 적용 가능한 delta만 replay한다.
- **Cherry-pick:** unrelated current behavior를 보존하면서 selected delta를 적용한다.
- **Revert:** later/current change를 보존하면서 intended inverse를 적용한다.

호환되는 intent는 조합하고 supersession에는 evidence를 요구하며 incompatible choice는 드러낸다. 추측해야 한다면 멈춘다. 비어 있거나 이미 존재하는 rebase/cherry-pick/revert step은 intentional empty history, safe redundancy, unresolved loss로 구분한다. redundancy는 `skip` authorization이 아니다.

### 4. Apply the Smallest Semantic Resolution

evidence가 요구하는 것만 편집한다. ordering, errors, types, modes, callers, side effects를 보존한다. 두 block을 기계적으로 이어 붙이거나, 다른 쪽이 path를 rename 또는 delete했다는 이유만으로 modification을 버리지 않는다.

lockfile 또는 generated output보다 authoritative input을 먼저 해결한다. package manager나 generator를 실행하기 전에는 hook, network/credential 사용, output을 inspect하고 baseline을 수집해 가능한 경우 isolate한다. 더 넓은 effect에는 명시적 authorization이 필요하다. 예상 밖 churn이 발생하면 멈추고 inspect한다. stage, reset, clean하지 않는다.

정확한 staging authorization 없이는 stage하지 않는다.

### 5. Verify Four Layers

working-tree content → index content → intended behavior → operation state를 각각 증명한다. staging 전에는 inventory한 모든 path를 처리하고, 가장 좁은 parse/compile/type check를 실행하며, retained intent의 결합 경로를 검증하고, source-derived output을 확인하고, resulting path/hunk를 baseline과 비교한다.

Required proof는 intent를 직접 증명한다. Equivalent substitute는 같은 boundary에서 같은 contract를 증명한다. Optional check는 더 넓은 coverage를 추가한다. resolution-caused failure는 고친다. required proof가 unavailable이면 정확한 gap을 보고하고 paused 상태를 유지한다. 이전 continue 요청은 informed acceptance가 아니다. policy가 허용하고 사용자가 named risk를 명시적으로 수락해도 결과는 behaviorally unverified로 남는다.

### 6. Stage and Transition Deliberately

정확히 authorization된 content만 stage한다. unrelated edit가 함께 있는 conflicted file을 path-stage하지 않는다. reviewed separation plan과 stage-0 proof가 없으면 staging 또는 continuation 전에 멈춘다.

`Continue`는 기록/replay하고 진행할 수 있다. `Skip`은 rebase/cherry-pick/revert에만 존재하며 paused unit을 생략하므로 evidence와 explicit drop authorization이 필요하다. `Abort`는 복원을 시도하지만 pre-existing work를 재구성하지 못할 수 있다. `Quit`은 metadata를 끝내면서 현재 working tree/index를 보존하지만 autostash identity 검증은 별도로 필요하다.

transition 전에는 exact command, paused unit, authorization, staged content, proof gap, pending todo/sequence effect, applicable hook, autostash/stash identity, expected history/index/worktree effect를 보고한다. `Finish`는 보고되지 않은 `exec` 또는 hook side effect를 허가하지 않는다. hook을 우회하거나 manual commit으로 대체하지 않는다. 일반 edit 후에는 compact refresh를, stage, side-effectful command, transition 후에는 full gate refresh를 수행한다.

## Report the Observed State

scoped outcome을 사용한다.

```text
working-tree resolution verified; index remains unmerged
exact resolution staged; operation remains paused
operation continued and stopped at a new conflict
paused unit explicitly skipped; fresh state observed
operation inactive after continuation; required behavioral proof unavailable
operation completed with required focused proof and verified autostash outcome
operation aborted; baseline restoration과 autostash A/pre-existing stash B outcome을 명시적으로 확인함
operation quit; tree/index preservation과 autostash A/pre-existing stash B identity를 확인함
```

다음 형식으로 보고한다.

```md
## Operation
## Conflict Inventory
## Intent and Resolution
## Verification
## Mutation State
## Remaining Risk
```

무엇이 stage, continue, skip, abort, quit, commit, reset, clean, 또는 push되지 않았는지 명시한다.
