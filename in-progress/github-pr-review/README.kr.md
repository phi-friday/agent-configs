# github-pr-review

[English](README.md) | [한국어](README.kr.md)

`github-pr-review`는 GitHub PR review draft, 통제된 review submission, explicit YOLO draft-and-submit/approve를 위한 in-progress skill이다.

Review draft, normal GitHub publication, YOLO publication을 별도 mode로 다룬다. 먼저 user input에서 mode를 resolve하고, ambiguous request는 `ask` tool로 확인한 뒤 선택된 mode를 계속 수행한다.

## 파일 구성

```text
github-pr-review/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
├─ references/
│  ├─ mode-selection.md
│  ├─ draft-mode.md
│  ├─ submit-mode.md
│  ├─ yolo-mode.md
│  └─ payload-approval.md
└─ scripts/
   └─ detect_mode.py
```

## 파일 역할

- `SKILL.md`: 기본 skill 정의, mode summary, safety-critical contract.
- `SKILL.kr.md`: `SKILL.md`의 한국어판.
- `README.md`: 영어 README.
- `README.kr.md`: 한국어 README.
- `references/mode-selection.md`: user input을 Draft, Submit, YOLO, ambiguous로 분류하는 규칙.
- `references/draft-mode.md`: read-only PR review workflow와 draft output format.
- `references/submit-mode.md`: selected `PRF-*` submission workflow와 mutation scope.
- `references/yolo-mode.md`: classifier가 explicit mode `yolo`를 반환할 때만 enable되는 same-run draft and submit/approve workflow.
- `references/payload-approval.md`: normal Submit mode의 exact preview format과 mandatory `ask` approval gate.
- `scripts/detect_mode.py`: raw user input의 explicit `draft`, `submit`, `yolo` mode keyword를 판정하는 runtime classifier.

## Scope

다음에 사용한다.

- GitHub PR을 review하되 comment를 제출하지 않을 때
- stable `PRF-*` review finding ID를 만들 때
- draft finding을 later submission으로 handoff할 때
- existing draft에서 selected finding을 제출할 때
- user inspection gate 없이 explicit `yolo`/`yolo,` draft-and-submit/approve를 실행할 때
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
    ├─ Submit mode ─▶ PRF-* 선택 → anchor validate → exact payload preview → ask approval → submit
    │
    └─ YOLO mode ───▶ draft → selected finding은 ask 없이 submit, finding이 없으면 approve
```

핵심 규칙:

```text
mode resolve → explicit `draft`/`submit`/`yolo` keyword가 있으면 사용 → `detect_mode.py`가 mode `yolo`를 반환하지 않으면 approval bypass 금지
```
