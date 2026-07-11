# resolving-merge-conflicts

[English](README.md) | [한국어](README.kr.md)

`resolving-merge-conflicts`는 Matt Pocock의 resolving-merge-conflicts workflow를 바탕으로 한 in-progress adaptation이다. 서로 다른 의도를 조정하고 호환되는 동작을 보존하며 mutation scope를 명시한다.

## 파일 구성

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

## 파일 역할

- `SKILL.md` / `SKILL.kr.md`: 서로 대응하는 영어·한국어 실행 계약.
- `README.md` / `README.kr.md`: 서로 대응하는 package manifest와 provenance 요약.
- `references/operation-state.md`: operation evidence, index stage, baseline, authorization boundary.
- `references/intent-reconstruction.md`: intent evidence, compatibility 판단, conflict 형태, silent-loss 검토.
- `references/verification-checklist.md`: working tree, index, behavior, side effect, operation state proof.

## 사용 범위

활성 `git merge`, `git rebase`, `git cherry-pick`, `git revert`가 content 또는 marker-free conflict로 중단된 경우에 사용한다. add/add, rename, modify/delete, generated-file, lockfile, binary, mode, symlink, submodule conflict도 포함한다. inventory, source 기반 intent reconstruction, 최소 semantic resolution, focused proof를 다룬다.

충돌 예측, 일반 diff review, operation 시작 전 branch-wide 전략 선택, 무관한 history rewrite에는 사용하지 않는다. blanket ours/theirs를 선택하지 않으며 marker 삭제만으로 완료되었다고 판단하지 않는다.

## 핵심 흐름

```text
operation, scope, baseline 확인
    → 모든 unmerged path와 conflict artifact inventory
    → source evidence로 호환되는 intent 재구성
    → 가장 작은 semantic resolution 적용
    → working tree, index, behavior, operation state 검증
    → 별도 허가된 boundary에서만 staging 또는 transition
```

proof는 required(보존한 intent 또는 paused delta를 직접 증명), equivalent(같은 boundary에서 같은 contract를 증명), optional(더 넓은 coverage)로 분류한다. required proof가 실패하거나 불가능하면 정확한 gap을 보고하고 operation을 paused 상태로 둔다. 사용자가 그 명명된 risk를 informed acceptance한 뒤 진행을 명시적으로 허가할 수 있지만 결과는 behaviorally unverified로 남는다.

## Mutation Boundaries

- conflicted file, 필요한 source artifact를 편집하고 focused non-destructive check를 실행하는 것은 conflict resolution 범위다.
- generator, hook, package-manager command가 file rewrite, lockfile update, network 사용을 일으킬 수 있으면 side-effectful mutation으로 보고 effect를 조사한다. authoritative source를 먼저 해결하고 scope가 있을 때만 실행한다.
- unrelated work가 conflicted path에 함께 있으면 path staging 전에 멈춘다. interactive hunk staging만으로는 부족하다. unrelated content를 index 밖에 유지하면서 exact stage-0 resolution을 구성하고 증명하는 reviewed plan이 있을 때만 진행한다.
- 단순 conflict resolution은 stage하지 않는다. 명시적인 finish-current-operation 요청은 exact verified conflict staging과 반복 continuation을 포함한다. standalone commit, unrelated staging, `reset`, `clean`, `push`에는 각각 별도 scope가 필요하다.

transition은 서로 독립적이며 각각 명시적으로 허가한다:

| Action | Boundary |
| --- | --- |
| `continue` | pending todo/hook effect를 inspect하고 authorize한 뒤 기록/replay하고 진행한다. |
| `skip` | redundancy evidence와 explicit drop authorization이 있을 때만 rebase/cherry-pick/revert unit을 생략한다. merge에는 skip이 없다. |
| `abort` | restoration을 시도한다. autostash A를 applied/conflicted/retained/moved로 분류하고 모든 pre-existing stash OID B가 reachable인지 증명한다. |
| `quit` | tree/index를 보존하며 metadata를 끝낸다. A의 retention/movement를 분류하고 모든 B가 reachable인지 증명한다. |

manual commit으로 대체하거나 hook을 우회하지 않는다. 일반 edit 후에는 compact refresh를, staging, side-effectful command, transition 후에는 full gate refresh를 사용한다.

## Reference Source

이 package는 Matt Pocock의 resolving-merge-conflicts workflow를 바탕으로 한 in-progress adaptation이며, intent reconstruction과 verification을 유지하면서 mutation boundary를 명시적으로 만든다. source가 변경되면 [upstream reference](../../references/mattpocock/skills/skills/engineering/resolving-merge-conflicts/SKILL.md)를 다시 검토한다.

원본 repository의 license notice는 root `NOTICE.md`를 따른다.
