# quality-gates

[English](README.md) | [한국어](README.kr.md)

완료, 통과, 수정, 리뷰 완료, 병합 가능 같은 상태를 선언하기 전에 fresh evidence와 review gate를 확인하는 in-progress 스킬이다.

## 구성

```text
quality-gates/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ verification-evidence.md
   ├─ code-review-request.md
   └─ review-feedback-handling.md
```

## 파일 역할

- `SKILL.md`: 기본 스킬 정의와 quality gate checklist.
- `SKILL.kr.md`: `SKILL.md`의 한국어판.
- `README.md`: 영어 원본 README.
- `README.kr.md`: 이 README의 한국어 번역본.
- `references/verification-evidence.md`: claim별 필요한 검증 증거 기준.
- `references/code-review-request.md`: code review 요청 기준과 template.
- `references/review-feedback-handling.md`: review feedback 평가, 적용, pushback 기준.

## 사용 범위

사용할 때:

- 작업 완료를 선언하기 전
- bug fixed, tests pass, ready to merge라고 말하기 전
- 중요한 변경에 대해 review를 요청할 때
- review feedback을 받았을 때
- subagent 결과를 완료로 받아들일 때

핵심 규칙:

```text
claim 식별 → fresh evidence 확보 → 필요한 review → feedback 처리 → 관찰한 결과만 보고
```

## 레퍼런스 출처

이 스킬은 다음 레퍼런스를 바탕으로 정리했다.

- `obra/superpowers/skills/verification-before-completion`
- `obra/superpowers/skills/requesting-code-review`
- `obra/superpowers/skills/receiving-code-review`

## 참고한 파일

다음 파일이 업데이트되면 이 스킬도 다시 검토한다.

- `references/obra/superpowers/skills/verification-before-completion/SKILL.md`
- `references/obra/superpowers/skills/requesting-code-review/SKILL.md`
- `references/obra/superpowers/skills/requesting-code-review/code-reviewer.md`
- `references/obra/superpowers/skills/receiving-code-review/SKILL.md`

원본 저장소의 라이선스 고지는 루트 `NOTICE.md`를 따른다.
