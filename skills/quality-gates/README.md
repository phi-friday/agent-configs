# quality-gates

[English](README.md) | [한국어](README.kr.md)

`quality-gates` is an in-progress skill for checking fresh evidence and review gates before declaring states such as done, passing, fixed, review complete, or ready to merge.

## Layout

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

## File Roles

- `SKILL.md`: Base skill definition and quality-gate checklist.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English source README.
- `README.kr.md`: Korean translation of this README.
- `references/verification-evidence.md`: Standards for what verification evidence is required for each claim.
- `references/code-review-request.md`: Criteria and template for requesting code review.
- `references/review-feedback-handling.md`: Criteria for evaluating, applying, and pushing back on review feedback.

## Scope

Use this skill when:

- Before declaring work complete.
- Before saying a bug is fixed, tests pass, or a change is ready to merge.
- Requesting review for an important change.
- Receiving review feedback.
- Accepting a subagent result as complete.

Core rule:

```text
identify claim → gather fresh evidence → get required review → handle feedback → report only observed results
```

## Reference Sources

This skill is based on these references:

- `obra/superpowers/skills/verification-before-completion`
- `obra/superpowers/skills/requesting-code-review`
- `obra/superpowers/skills/receiving-code-review`

## Reference Files

Review this skill again when these files change:

- `references/obra/superpowers/skills/verification-before-completion/SKILL.md`
- `references/obra/superpowers/skills/requesting-code-review/SKILL.md`
- `references/obra/superpowers/skills/requesting-code-review/code-reviewer.md`
- `references/obra/superpowers/skills/receiving-code-review/SKILL.md`

<!-- publish_skills:reference-commits:start -->
## Reference Commits

Published against these submodule commits.

- `references/obra/superpowers`: `d884ae04edebef577e82ff7c4e143debd0bbec99`
<!-- publish_skills:reference-commits:end -->

License notices for the original repositories are covered by the root `NOTICE.md`.
