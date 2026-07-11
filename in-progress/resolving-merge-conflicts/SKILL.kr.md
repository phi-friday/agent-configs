---
name: resolving-merge-conflicts
description: "Git merge, rebase, cherry-pick, revert가 충돌로 중단되고 양쪽 의도를 보존해 해결해야 할 때. Use when a Git merge, rebase, cherry-pick, or revert is stopped by conflicts and the competing changes must be reconciled without losing intent."
---

# Resolving Merge Conflicts

Git conflict를 marker 삭제가 아니라 의도 조정으로 해결한다.

이것은 이미 중단된 merge, rebase, cherry-pick, revert를 위한 technique skill이다. 현재 operation의 목적과 competing changes에서 호환되는 모든 동작을 보존한다. history를 바꾸는 action은 사용자가 명시적으로 허용한 scope 안에서 수행한다.

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

동작을 지어내거나, 관련 없는 refactor를 수행하거나, generated artifact를 자체 source of truth로 취급하지 않는다. 시간 압박이 이 규칙을 약화시키지 않는다.

## Supporting References

이 파일은 실행 checklist로 유지한다. 주제가 활성화된 경우에만 supporting file을 연다.

- `references/operation-state.md` — active Git operation을 식별하고, index stage를 해석하며, mutation boundary를 적용한다.
- `references/intent-reconstruction.md` — 각 side의 목적을 재구성하고 hunk-level resolution rationale을 작성한다.
- `references/verification-checklist.md` — 과장 없이 file, index, behavior, operation state를 입증한다.

## Use When

다음 active operation이 conflict로 중단되었을 때 사용한다.

- `git merge`
- `git rebase`, interactive rebase 포함
- `git cherry-pick`
- `git revert`

content, add/add, rename, rename/delete, modify/delete, generated-file, lockfile, binary, mode conflict에 사용한다.

향후 conflict를 단순히 예측하거나, 일반 diff를 review하거나, 이미 진행 중이 아닌 history를 rewrite하거나, operation 시작 전에 branch-wide merge strategy를 선택하는 데는 사용하지 않는다.

## Phase 1 — Confirm Operation and User Scope

편집하기 전에 active operation과 허가된 mutation boundary를 모두 식별한다.

요청을 다음 scope 중 하나로 분류한다.

```text
resolve files only
resolve and stage exact conflict resolutions
resolve, stage, and continue the current operation
abort the current operation
```

Rules:

- “resolve the conflicts” 요청은 conflicted files의 inspect와 edit 및 focused verification을 허용한다. 그 자체로 staging, continuing, committing, aborting, resetting, cleaning, pushing을 허용하지 않는다.
- “stage,” “mark resolved,” “continue,” 또는 “finish this rebase/merge/cherry-pick/revert”를 명시적으로 요청하면 현재 관찰된 operation에서 이름이 지정된 action만 허용한다.
- mutation scope가 모호하면 검증된 working-tree resolution까지 진행하고 모호한 mutation 전에 멈춘다. semantic choice나 destructive action에 실제로 사용자가 필요할 때만 질문한다.
- `reset`, `clean`, `commit`, `push`, force-push에 대한 permission은 resolve 또는 continue 요청에서 절대 추론하지 않는다.

그 다음 read-only state를 inspect한다.

1. Git이 active로 보고하는 operation을 확인한다.
2. 현재 branch 또는 detached state, 해당되는 경우 paused commit, 그리고 operation goal을 기록한다.
3. 변경하기 전에 staged, unstaged, untracked, unmerged path를 수집한다.
4. 기존의 관련 없는 work와 conflict-resolution work를 분리한다.
5. operation metadata가 없거나, 서로 모순되거나, 사용자가 설명한 것과 다른 operation을 나타내면 멈춘다.

detection, side semantics, continuation command, authorization rule에는 `references/operation-state.md`를 사용한다.

## Phase 2 — Inventory the Entire Conflict Surface

unmerged index와 working-tree conflict artifact를 모두 열거한다. 어느 한 view만으로는 충분하지 않다.

Inventory에는 다음이 포함되어야 한다.

- 모든 unmerged path와 conflict type
- text file의 모든 conflict block
- modify/delete, rename/delete, binary, file-mode, submodule entry처럼 marker가 없는 conflict
- lockfile의 source manifest
- generated file의 source schema/template와 generator command
- 그대로 유지해야 하는 기존 staged, modified, untracked path

path별 또는 독립적으로 의미가 있는 hunk별로 하나의 conflict record를 만든다.

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

다른 conflict path를 아직 examine하지 않은 상태에서 가장 먼저 보이는 marker를 resolve하기 시작하지 않는다. 완전한 inventory는 한 conflict의 locally plausible한 edit가 다른 conflict와 모순되는 것을 방지한다.

## Phase 3 — Reconstruct Both Intents

각 record에 대해 content를 선택하기 전에 primary source를 읽는다.

1. active operation metadata와 paused patch
2. 해당 path의 base 및 사용 가능한 index stage
3. source commit과 commit message
4. 가능한 경우 linked PR, issue, ticket, design material
5. 주변 implementation, call site, test, repository instruction
6. source manifest, schema, template, generator configuration

active operation에 매핑하지 않은 채 “ours”와 “theirs” label을 신뢰하지 않는다. rebase 중에는 실질적 의미가 달라지고 delete conflict에서는 불완전할 수 있다.

올바른 operation lens를 적용한다.

- **Merge:** 명시된 integration goal에 맞춰 양쪽 parent line을 조정한다. 어느 parent의 intent도 조용히 버리지 않는다.
- **Rebase:** 새 base 위에서 paused commit 하나의 intent를 보존한다. 아직 replay되지 않은 이후 commit의 의미를 섞지 않는다.
- **Cherry-pick:** 선택한 commit의 의도된 delta를 보존하면서 현재 branch의 관련 없는 behavior를 유지한다.
- **Revert:** revert된 commit의 의도된 inverse를 재구성하면서 이후/current change를 보존한다.

각 intent pair를 분류한다.

- **Compatible:** 두 behavior를 가장 작고 일관된 edit로 조합한다.
- **Superseded:** history, test, 또는 operation purpose가 이전 representation을 대체한다고 입증할 때만 최신 representation을 유지하고, 여전히 관련 있는 behavior는 transplant한다.
- **Incompatible:** 구체적인 tradeoff와 evidence를 제시한다. 제3의 policy를 지어내지 않는다.
- **Uncertain:** 더 많은 source evidence를 수집한다. product 또는 history 선택이 남으면 해당 hunk를 edit하기 전에 사용자에게 묻는다.

edit을 적용하기 전에 resolution rationale을 작성한다. conflict record, evidence order, common conflict shape에는 `references/intent-reconstruction.md`를 사용한다.

## Phase 4 — Apply the Smallest Semantic Resolution

재구성한 intent가 요구하는 것만 edit한다.

### Content conflicts

양쪽의 독립적인 behavior를 보존한다. 해당 behavior들이 공존하는 데 필요한 경우 import, type, ordering, error handling, caller를 조정한다. 두 text block을 기계적으로 모두 남겨 실행이 중복되거나 invariant를 위반하게 만들지 않는다.

### Rename/delete and modify/delete conflicts

path가 이동했거나 사라진 이유를 추적한다. 한 side가 file을 rename하고 다른 side가 old path에서 여전히 유효한 behavior를 바꿨다면 그 behavior를 replacement path로 transplant하고 obsolete path는 제거된 상태로 둔다. deletion이 의도적으로 behavior를 제거한 것이라면 primary-source evidence가 그 intent를 뒷받침할 때만 deletion을 보존한다.

### Lockfile conflicts

dependency intent를 source manifest에서 먼저 resolve한다. 가능하면 repository가 고정한 package manager와 일반적인 lockfile-generation path로 lockfile을 regenerate한다. marker를 제거하려고 lockfile section을 손으로 splice하지 않는다. 실행하기 전에 install-script 또는 dependency mutation을 inspect한다.

### Generated-file conflicts

schema, template, source data, generator input을 먼저 resolve한다. repository의 기존 generator를 실행한 뒤 output을 inspect한다. 수동으로 merge한 generated file을 완료된 resolution으로 취급하지 않는다. authoritative source input을 사용할 수 없다면 tradeoff를 드러내고 operation을 paused 상태로 유지한다. 모든 input은 resolve됐지만 generator를 사용할 수 없다면 artifact가 resolve됐다고 주장하지 말고 누락된 prerequisite와 verification gap을 보고한다.

### Binary or non-text conflicts

producing source와 의도된 artifact를 식별한다. evidence로만 artifact를 regenerate하거나 선택한다. 어느 side도 semantic하게 inspect할 수 없고 reproducible source도 없다면 추측하지 말고 tradeoff를 드러낸다.

각 edit 후 conflict record를 실제 resolution으로 갱신한다. staging이 명시적으로 scope에 포함되지 않았다면 아직 stage하지 않는다.

## Phase 5 — Verify the Working-Tree Resolution

marker removal은 verification의 시작이지 결론이 아니다.

staging 전에 다음을 수행한다.

1. inventory한 모든 text conflict에 unresolved marker가 없는지 확인한다.
2. marker-free conflict path와 예상한 rename/deletion outcome을 모두 inspect한다.
3. 올바른 가장 좁은 seam에서 touched file을 parse하거나 compile한다.
4. 보존한 각 behavior와 현재 operation의 의도된 change를 실행하는 focused test를 수행한다.
5. 해당되는 source-derived conflict에서는 artifact를 regenerate하고 source/output consistency를 확인한다.
6. lockfile conflict에서는 project package manager로 manifest/lockfile consistency를 검증한다.
7. resulting diff에서 dropped behavior, duplicate behavior, accidental formatting, unrelated change를 inspect한다.
8. 기존 staged, modified, untracked work가 변경되지 않았는지 확인한다.

이 시점에는 unmerged index가 남아 있을 수 있다. Git은 stage될 때만 resolution을 기록하기 때문이다. 이를 정확히 “working-tree resolution verified; not recorded in the index”라고 보고하며 “Git conflict resolved”라고 보고하지 않는다.

check가 실패하면:

- operation을 paused 상태로 유지한다.
- resolution이 failure를 일으켰는지 판단한다.
- 책임 있는 conflict resolution만 수정한다.
- 동일한 check를 다시 실행한다.
- 관련 없거나 접근할 수 없는 failure는 정확히 보고한다.

필요한 verification이 실패했거나 unavailable인 동안 성공을 선언하지 않는다. proof layer와 claim wording에는 `references/verification-checklist.md`를 사용한다.

## Phase 6 — Cross the Mutation Boundary Deliberately

staging, continuing, committing, aborting은 별도의 action이다. 하나에 대한 authorization이 다른 action을 의미하지 않는다.

### Stage only when explicitly authorized

stage하기 전에 다음을 보고한다.

- 관찰된 operation과 해당되는 경우 paused commit
- stage할 path
- 이미 완료한 verification
- 정확한 staging action
- scope 밖에 남는 action

의도한 deletion/rename path를 포함해 정확한 resolution path만 stage한다. unrelated work를 포착할 수 있는 broad staging을 피한다. 그런 다음 staged diff를 inspect하고 unmerged index가 비었는지 확인한다.

staging이 빠진 path를 드러내거나 unrelated content를 stage하면 멈추고 work를 파괴하지 않는 방식으로 index를 바로잡는다.

### Continue only when explicitly authorized

continue하기 전에 다음을 보고한다.

- index에 unmerged entry가 없다는 사실
- 통과한 check 또는 아직 unavailable인 check
- operation에 정확히 맞는 continuation command
- continuation이 commit을 기록할지 여부
- authorization이 이번 stop에만 해당하는지, 현재 operation 전체에 해당하는지

그 다음 관찰된 operation만 continue한다. continuation command가 commit을 생성하거나 replay한다는 이유만으로 standalone commit을 실행하지 않는다.

긴 rebase 또는 sequencer가 다시 중단되면:

1. 새 stop을 새로운 conflict inventory로 취급한다.
2. 해당 paused commit의 intent를 독립적으로 재구성한다.
3. verification과 mutation gate를 다시 실행한다.
4. 사용자의 명시적 scope가 전체 operation을 포함할 때만 다시 continue한다.

### Abort only when explicitly chosen

abort는 유효한 사용자 선택지다. abort하기 전에 진행 중인 어떤 resolution work와 operation state가 버려질지 밝힌다. 어려운 semantic choice를 automatic abort로 대체하지 않으며, evidence가 operation goal이 잘못되었음을 보여주는데도 “always resolve” rule을 따르지 않는다.

`reset`, `clean`, `commit`, `push`, force-push는 사용자가 그 정확한 action을 명시적으로 요청하지 않는 한 계속 scope 밖이다. resolution은 publication authorization이 아니다.

## Phase 7 — Prove the Observed End State

마지막으로 허가된 mutation 후 Git state를 다시 읽는다. 다음 outcome을 구분한다.

```text
working-tree content resolved; index still unmerged by design
resolution staged; operation intentionally paused
operation continued and stopped at another conflict
operation completed; focused verification passed
operation paused because verification or intent is unresolved
operation aborted by explicit user choice
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

각 conflict에 대해 관찰한 source를 선택한 resolution 및 verification과 연결한다. 무엇이 stage, continue, commit, abort, reset, clean, push되지 않았는지 정확히 명시한다.

Completion에는 실제로 허가된 scope에 대한 evidence가 필요하다.

- inventory한 모든 conflict에 semantic resolution 또는 명시적인 unresolved tradeoff가 있다.
- resolved text에 unresolved marker가 남아 있지 않다.
- source-derived artifact가 resolved source에서 나왔다.
- focused syntax/type/build/test check가 의도된 behavior를 뒷받침한다.
- 실패한 check를 숨기지 않았다.
- index state가 staging authorization 여부와 일치한다.
- operation state가 continuation 또는 abort authorization 여부와 일치한다.
- unrelated work가 untouched 상태다.

## Red Flags

다음 중 하나라도 나타나면 가장 먼저 위반된 phase로 돌아간다.

- “어디서나 그냥 ours/theirs를 선택하자.”
- “marker가 사라졌으니 끝났다.”
- “file이 삭제됐으니 modification은 중요하지 않다.”
- “이 lockfile이나 generated file은 손으로 merge하는 편이 더 쉽다.”
- “test는 실패하지만 Git이 resolution을 받아들이니 괜찮다.”
- “rebase conflict도 그냥 일반 merge conflict다.”
- “전부 stage하고 나중에 inspect하자.”
- “일단 continue하고 작동하는지 보자.”
- “절대 abort하지 않는다.”
- “사용자가 resolve를 요청했으니 commit이나 push도 implied다.”

이 shortcut들은 조용한 behavior 손실 또는 unauthorized history change를 만든다.
