# Verification Evidence

Every completion claim must map to fresh evidence.

## Gate Function

```text
1. IDENTIFY the exact claim.
2. CHOOSE the command or inspection that proves it.
3. RUN the verification in the current state.
4. READ exit code and full output.
5. CLAIM only what the output proves.
```

If any step is missing, do not make the claim.

## Claim-To-Proof Map

| Claim | Proof |
|---|---|
| Tests pass | test command output, exit 0, 0 failures |
| Build succeeds | build command output, exit 0 |
| Typecheck clean | typecheck command output, 0 errors |
| Lint clean | lint command output, 0 errors |
| Bug fixed | original repro no longer fails |
| Regression protected | test failed before fix and passes after fix |
| Requirements met | requirement checklist verified item by item |
| Review addressed | every review item mapped to fix, rejection, or clarification |
| Agent completed work | inspect changed files and verify relevant behavior |

## Reading Output

Check:

- command actually ran
- exit code
- failure/error count
- skipped tests or filtered suites
- warnings that affect the claim
- whether output was truncated by tooling
- whether the command covered the changed area

If the output is truncated, inspect the full artifact/log before making broad claims.

## Scoped Claims

Partial verification is acceptable only with a scoped claim.

Good:

```text
Targeted auth tests pass: `npm test auth.test.ts` reported 12/12 pass.
```

Bad:

```text
Tests pass.
```

## Regression Test Proof

For regression tests, prove the test can fail.

Preferred sequence:

```text
write test
run → fail for expected reason
apply fix
run → pass
```

If the fix already exists and cannot be reverted safely, state that limitation. Do not claim a full red-green proof.

## Requirement Checklist

Tests passing do not prove every requirement is met.

For plans/specs, create a checklist:

```md
- [x] Requirement A — evidence
- [x] Requirement B — evidence
- [ ] Requirement C — missing, explain
```

Report gaps instead of hiding them.
