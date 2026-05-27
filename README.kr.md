# Agent Configs

[English](README.md) | [한국어](README.kr.md)

개인용 에이전트 설정과 1차 작성 AI 에이전트 스킬을 관리하는 저장소입니다.

## 스킬

1차 작성 스킬의 원본은 [`in-progress/`](./in-progress/) 아래에 있습니다. 승인된 스킬은 [`publish-skills.py`](./publish-skills.py)를 통해 [`skills/`](./skills/)로 게시됩니다. 생성된 스킬 출력물은 직접 수정하지 않습니다.

현재 1차 작성 스킬:

- [`explore-and-frame`](./in-progress/explore-and-frame/): 모호한 작업을 구현 전에 탐색하고, 코드 맥락을 파악하며, 선택지를 비교하고, 결정을 정리합니다.
- [`parallel-execution`](./in-progress/parallel-execution/): 독립적인 작업을 서브에이전트로 나누되, 통합과 최종 검증은 컨트롤러가 책임지게 합니다.
- [`quality-gates`](./in-progress/quality-gates/): 완료, 수정됨, 통과, 리뷰 완료, 병합 준비 같은 상태를 선언하기 전에 최신 근거를 요구합니다.
- [`root-cause-debugging`](./in-progress/root-cause-debugging/): 버그, 회귀, 플레이크, 통합 실패를 고치기 전에 실제 근본 원인을 증거로 확인합니다.
- [`test-driven-development`](./in-progress/test-driven-development/): 기능, 버그 수정, 리팩터링, 동작 변경을 테스트 우선으로 구현합니다.

각 1차 작성 스킬은 영어 스킬 정의와 README 옆에 한국어 버전(`SKILL.kr.md`, `README.kr.md`)을 함께 둡니다.

이 저장소의 일부 또는 전체 커스텀 스킬은 아래 외부 참조 저장소의 작업에서 영감을 받았거나, 이를 각색했거나, 파생되었을 수 있습니다. 해당 업스트림 작업은 MIT 라이선스를 따르며, 그 작업을 복사, 수정, 또는 실질적으로 포함하는 경우 저작권 및 라이선스 고지를 보존해야 합니다.

## 외부 참조

[`references/`](./references/) 아래의 저장소는 커스텀 스킬을 만들 때 참고하는 외부 Git 서브모듈입니다. 명시적으로 따로 적지 않는 한, 이 저장소에서 작성한 원본이 아닙니다.

| 경로 | 출처 | 라이선스 |
|---|---|---|
| [`references/mattpocock/skills`](./references/mattpocock/skills) | <https://github.com/mattpocock/skills> | MIT |
| [`references/obra/superpowers`](./references/obra/superpowers) | <https://github.com/obra/superpowers> | MIT |
| [`references/Fission-AI/OpenSpec`](./references/Fission-AI/OpenSpec) | <https://github.com/Fission-AI/OpenSpec> | MIT |

서브모듈과 함께 복제:

```sh
git clone --recurse-submodules <repo-url>
```

복제 후 서브모듈 초기화:

```sh
git submodule update --init --recursive
```

## 라이선스 고지

각 외부 참조 저장소는 서브모듈 디렉터리 안에 자체 MIT 라이선스 파일을 유지합니다.

이 저장소의 커스텀 스킬이나 다른 파일이 해당 참조의 자료를 복사, 수정, 또는 실질적으로 포함하는 경우 관련 업스트림 저작권 및 MIT 라이선스 고지를 보존해야 합니다. 제3자 고지 추적은 [`NOTICE.md`](./NOTICE.md)를 참고하세요.
