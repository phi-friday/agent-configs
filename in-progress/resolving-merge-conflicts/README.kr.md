# resolving-merge-conflicts

[English](README.md) | [한국어](README.kr.md)

`resolving-merge-conflicts`는 Matt Pocock의 resolving-merge-conflicts workflow를 바탕으로 한 in-progress adaptation이다. 충돌을 marker 삭제가 아니라 의도 조정으로 다루며, 양쪽 의도를 재구성하고 가장 작은 semantic resolution을 적용한 뒤 동작과 operation state를 검증한다. intent reconstruction과 verification은 유지하되, 무조건적인 “never abort” 및 항상 stage/commit/continue하는 동작은 명시적 user scope로 대체한다.

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

- `SKILL.md`: 이미 중단된 merge, rebase, cherry-pick, revert의 충돌을 해결하는 영어 실행 계약.
- `SKILL.kr.md`: `SKILL.md`의 한국어 counterpart.
- `README.md`: 영어 package manifest와 provenance 요약.
- `README.kr.md`: 이 manifest의 한국어 counterpart.
- `references/operation-state.md`: operation 감지, index stage 해석, 기존 작업 보존, mutation authorization boundary.
- `references/intent-reconstruction.md`: evidence 순서, operation별 intent 관점, conflict record, compatibility 판단, silent-loss 검토.
- `references/verification-checklist.md`: working tree, index, behavior, operation state를 증명하는 계층과 claim-to-evidence 표현.

## 사용 범위

활성 `git merge`, `git rebase`, `git cherry-pick`, `git revert`가 content, add/add, rename, modify/delete, generated-file, lockfile, binary, mode 또는 관련 충돌로 멈췄을 때 사용한다. 전체 conflict inventory, source 기반 intent reconstruction, 최소 semantic edit, focused verification을 다룬다.

미래 충돌 예측, 일반 diff review, operation 시작 전 branch-wide merge 전략 선택, 이미 중단된 operation과 무관한 history rewrite에는 사용하지 않는다. blanket ours/theirs 선택을 하지 않으며 marker 삭제만으로 완료되었다고 판단하지 않는다.

## 핵심 흐름

```text
operation과 user scope 확인
    → 모든 unmerged path와 conflict artifact inventory
    → source evidence로 양쪽 intent 재구성
    → 가장 작은 semantic resolution 적용
    → working tree, behavior, index, operation state 검증
    → 명시적으로 허가된 경우에만 staging/continuation/commit/abort boundary 통과
```

필수 verification이 실패하거나 실행 불가하면 resolution은 미완료이며 operation을 paused 상태로 둔다. 이를 숨기지 말고 gap을 보고한다.

## Mutation Boundary

- conflicted file, 필요한 source artifact를 편집하고 focused non-destructive verification을 실행하는 것은 “충돌 해결” 범위에 있다.
- 정확한 path staging, 현재 operation continuation, standalone commit 기록, abort는 명시적 user scope가 필요하다. marker cleanup이나 file editing만으로 어느 것도 허가되지 않는다.
- `reset`, `clean`, `push`(force-push 포함)는 명시적 요청과 scope 검토가 필요하다.
- continuation command가 commit을 기록하거나 replay할 수 있으므로, 수동 commit으로 대체하거나 자동으로 continue하지 않는다.

## Reference Source

이 package는 Matt Pocock의 resolving-merge-conflicts workflow를 바탕으로 한 in-progress adaptation이며, intent reconstruction과 verification을 유지하면서 mutation boundary를 명시적으로 만든다. source가 변경되면 upstream reference인 `references/mattpocock/skills/skills/engineering/resolving-merge-conflicts/SKILL.md`를 다시 검토한다.

원본 repository의 license notice는 root `NOTICE.md`를 따른다.
