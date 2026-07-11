# test-driven-development

[English](README.md) | [한국어](README.kr.md)

기능, 버그 수정, 리팩터링, 동작 변경을 test-first로 구현하기 위한 in-progress 스킬이다.

## 구성

```text
test-driven-development/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ test-quality.md
   ├─ mocking-guidelines.md
   ├─ interface-design.md
   └─ refactoring.md
```

## 파일 역할

- `SKILL.md`: 기본 스킬 정의와 RED-GREEN-REFACTOR checklist.
- `SKILL.kr.md`: `SKILL.md`의 한국어판.
- `README.md`: 영어 원본 README.
- `README.kr.md`: 이 README의 한국어 번역본.
- `references/test-quality.md`: public behavior 중심 테스트 기준.
- `references/mocking-guidelines.md`: mock 사용 기준과 anti-pattern.
- `references/interface-design.md`: 테스트하기 쉬운 interface 설계 기준.
- `references/refactoring.md`: green 상태에서의 refactor 기준.

## 사용 범위

사용할 때:

- 새 기능 구현
- 버그 수정의 regression test 작성
- 동작 변경
- 안전망이 필요한 refactor
- 새 public API, command, UI flow 구현

핵심 규칙:

```text
RED → GREEN → REFACTOR
```

production code를 쓰기 전에 실패하는 behavior test를 먼저 보고, green 이후에만 refactor한다.

## 레퍼런스 출처

이 스킬은 다음 레퍼런스를 바탕으로 정리했다.

- `mattpocock/skills/skills/engineering/tdd`
- `obra/superpowers/skills/test-driven-development`

## 참고한 파일

다음 파일이 업데이트되면 이 스킬도 다시 검토한다.

- `references/mattpocock/skills/skills/engineering/tdd/SKILL.md`
- `references/mattpocock/skills/skills/engineering/tdd/tests.md`
- `references/mattpocock/skills/skills/engineering/tdd/mocking.md`
- `references/obra/superpowers/skills/test-driven-development/SKILL.md`
- `references/obra/superpowers/skills/test-driven-development/testing-anti-patterns.md`

과거 upstream 경로(현재 소스는 아님, 이력 저장용 `694fa303...`):

- `interface-design.md`
- `deep-modules.md`
- `refactoring.md`

원본 저장소의 라이선스 고지는 루트 `NOTICE.md`를 따른다.