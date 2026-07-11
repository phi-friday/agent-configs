# test-driven-development

[English](README.md) | [한국어](README.kr.md)

`test-driven-development` is an in-progress skill for implementing features, bug fixes, refactors, and behavior changes test-first.

## Layout

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

## File Roles

- `SKILL.md`: Base skill definition and RED-GREEN-REFACTOR checklist.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English source README.
- `README.kr.md`: Korean translation of this README.
- `references/test-quality.md`: Criteria for tests centered on public behavior.
- `references/mocking-guidelines.md`: Mocking criteria and anti-patterns.
- `references/interface-design.md`: Interface-design criteria for testable code.
- `references/refactoring.md`: Refactoring criteria after the code is green.

## Scope

Use this skill for:

- Implementing new features.
- Writing regression tests for bug fixes.
- Behavior changes.
- Refactors that need a safety net.
- New public APIs, commands, or UI flows.

Core rule:

```text
RED → GREEN → REFACTOR
```

See the failing behavior test before writing production code, and refactor only after the test is green.

## Reference Sources

This skill is based on these references:

- `mattpocock/skills/skills/engineering/tdd`
- `obra/superpowers/skills/test-driven-development`

## Reference Files

Review this skill again when these files change:

- `references/mattpocock/skills/skills/engineering/tdd/SKILL.md`
- `references/mattpocock/skills/skills/engineering/tdd/tests.md`
- `references/mattpocock/skills/skills/engineering/tdd/mocking.md`
- `references/obra/superpowers/skills/test-driven-development/SKILL.md`
- `references/obra/superpowers/skills/test-driven-development/testing-anti-patterns.md`

Historical upstream paths (not current source, kept for provenance only, commit `694fa303...`):

- `interface-design.md`
- `deep-modules.md`
- `refactoring.md`

License notices for the original repositories are covered by the root `NOTICE.md`.