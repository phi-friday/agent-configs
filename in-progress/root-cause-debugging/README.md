# root-cause-debugging

버그, 실패, 성능 저하, flaky 동작, 통합 문제를 수정하기 전에 root cause를 증거로 확인하도록 강제하는 in-progress 스킬이다.

## 구성

```text
root-cause-debugging/
├─ SKILL.md
├─ skill.kr.md
├─ README.md
└─ references/
   ├─ feedback-loops.md
   ├─ root-cause-tracing.md
   ├─ condition-based-waiting.md
   ├─ defense-in-depth.md
   └─ scripts/
      ├─ hitl-loop.template.sh
      └─ find-polluter.template.sh
```

## 파일 역할

- `SKILL.md`: 기본 스킬 정의와 실행 checklist.
- `skill.kr.md`: `SKILL.md`의 한국어판.
- `references/feedback-loops.md`: 재현 loop 선택과 품질 기준.
- `references/root-cause-tracing.md`: bad value/state를 source까지 추적하는 절차.
- `references/condition-based-waiting.md`: fake timer 우선 원칙과 condition-based wait 패턴.
- `references/defense-in-depth.md`: root cause 확인 뒤 layered guard를 추가하는 기준.
- `references/scripts/hitl-loop.template.sh`: manual reproduction이 불가피할 때 쓰는 template.
- `references/scripts/find-polluter.template.sh`: unwanted state를 만드는 test/command를 격리하는 template.

## 사용 범위

사용할 때:

- test/build/CI 실패
- runtime exception 또는 잘못된 출력
- flaky test나 timing 문제
- integration failure
- performance regression
- 이미 시도한 fix가 실패한 경우

핵심 규칙:

```text
재현 → 관찰 → 추적 → 가설 → 계측 → 근원 수정 → 검증
```

root cause를 확인하기 전에는 retry, timeout, fallback, warning suppression, broad refactor를 추가하지 않는다.

## 레퍼런스 출처

이 스킬은 다음 레퍼런스를 바탕으로 정리했다.

- `mattpocock/skills/skills/engineering/diagnose`
- `obra/superpowers/skills/systematic-debugging`

## 참고한 파일

다음 파일이 업데이트되면 이 스킬도 다시 검토한다.

- `references/mattpocock/skills/skills/engineering/diagnose/SKILL.md`
- `references/mattpocock/skills/skills/engineering/diagnose/scripts/hitl-loop.template.sh`
- `references/obra/superpowers/skills/systematic-debugging/SKILL.md`
- `references/obra/superpowers/skills/systematic-debugging/root-cause-tracing.md`
- `references/obra/superpowers/skills/systematic-debugging/defense-in-depth.md`
- `references/obra/superpowers/skills/systematic-debugging/condition-based-waiting.md`
- `references/obra/superpowers/skills/systematic-debugging/condition-based-waiting-example.ts`
- `references/obra/superpowers/skills/systematic-debugging/find-polluter.sh`
- `references/obra/superpowers/skills/systematic-debugging/CREATION-LOG.md`
- `references/obra/superpowers/skills/systematic-debugging/test-academic.md`
- `references/obra/superpowers/skills/systematic-debugging/test-pressure-1.md`
- `references/obra/superpowers/skills/systematic-debugging/test-pressure-2.md`
- `references/obra/superpowers/skills/systematic-debugging/test-pressure-3.md`

원본 저장소의 라이선스 고지는 루트 `NOTICE.md`를 따른다.
