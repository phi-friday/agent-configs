# root-cause-debugging

[English](README.md) | [한국어](README.kr.md)

`root-cause-debugging` is an in-progress skill that forces evidence-based confirmation of the root cause before fixing bugs, failures, performance regressions, flaky behavior, or integration problems.

## Layout

```text
root-cause-debugging/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ feedback-loops.md
   ├─ root-cause-tracing.md
   ├─ condition-based-waiting.md
   ├─ defense-in-depth.md
   └─ scripts/
      ├─ hitl-loop.template.sh
      └─ find-polluter.template.sh
```

## File Roles

- `SKILL.md`: Base skill definition and execution checklist.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English source README.
- `README.kr.md`: Korean translation of this README.
- `references/feedback-loops.md`: Criteria for choosing and evaluating reproduction loops.
- `references/root-cause-tracing.md`: Procedure for tracing bad values or state back to the source.
- `references/condition-based-waiting.md`: Fake-timer-first principle and condition-based wait patterns.
- `references/defense-in-depth.md`: Criteria for adding layered guards after the root cause is confirmed.
- `references/scripts/hitl-loop.template.sh`: Template for cases where manual reproduction is unavoidable.
- `references/scripts/find-polluter.template.sh`: Template for isolating the test or command that creates unwanted state.

## Scope

Use this skill for:

- Test, build, or CI failures.
- Runtime exceptions or incorrect output.
- Flaky tests or timing problems.
- Integration failures.
- Performance regressions.
- Cases where an already attempted fix failed.

Core rule:

```text
reproduce → observe → trace → hypothesize → instrument → fix root cause → verify
```

Do not add retries, timeouts, fallbacks, warning suppression, or broad refactors before confirming the root cause.

## Failure Reproduction Contract

- Use one command with a fixed assertion targeting the exact symptom.
- The command and assertion must show that exact symptom as RED before diagnosis.
- Reuse the same command and the same assertion to verify GREEN after a fix.
- For flaky failures, make the command pressure-capable enough to establish reproducible RED and record the reproduction rate.
- Use minimized repros for hypothesis work only; final proof must be the original unminimized scenario.

## Reference Sources

This skill is based on these references:

- `mattpocock/skills/skills/engineering/diagnosing-bugs`
- `obra/superpowers/skills/systematic-debugging`

## Reference Files

Review this skill again when these files change:

- `references/mattpocock/skills/skills/engineering/diagnosing-bugs/SKILL.md`
- `references/mattpocock/skills/skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh`
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

License notices for the original repositories are covered by the root `NOTICE.md`.
