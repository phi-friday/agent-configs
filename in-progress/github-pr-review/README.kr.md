# github-pr-review

[English](README.md) | [한국어](README.kr.md)

`github-pr-review`는 GitHub PR review draft와 통제된 review submission을 위한 in-progress skill이다.

Review draft와 GitHub publication을 별도 mode로 다룬다. 먼저 user input에서 mode를 resolve하고, ambiguous request는 `ask` tool로 확인한 뒤 선택된 mode를 계속 수행한다.

## 파일 구성

```text
github-pr-review/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ mode-selection.md
   ├─ draft-mode.md
   ├─ submit-mode.md
   └─ payload-approval.md
```

## 파일 역할

- `SKILL.md`: 기본 skill 정의, mode summary, safety-critical contract.
- `SKILL.kr.md`: `SKILL.md`의 한국어판.
- `README.md`: 영어 README.
- `README.kr.md`: 한국어 README.
- `references/mode-selection.md`: user input을 Draft, Submit, ambiguous로 분류하는 규칙.
- `references/draft-mode.md`: read-only PR review workflow와 draft output format.
- `references/submit-mode.md`: selected `PRF-*` submission workflow와 mutation scope.
- `references/payload-approval.md`: exact preview format과 mandatory `ask` approval gate.

## Scope

다음에 사용한다.

- GitHub PR을 review하되 comment를 제출하지 않을 때
- stable `PRF-*` review finding ID를 만들 때
- draft finding을 later submission으로 handoff할 때
- existing draft에서 selected finding을 제출할 때
- 의도적으로 제외된 review context를 보존할 때

GitHub PR target이 없는 generic code review skill로 사용하지 않는다.

## Core Flow

```text
user input
    │
    ▼
resolve mode
    │
    ├─ Draft mode ──▶ context 읽기 → diff review → PRF-* finding을 chat에만 보고
    │
    └─ Submit mode ─▶ PRF-* 선택 → anchor validate → exact payload preview → ask approval → submit
```

핵심 규칙:

```text
mode resolve → 안전하게 draft 또는 existing draft에서 submit → exact ask approval 없이 GitHub mutate 금지
```
