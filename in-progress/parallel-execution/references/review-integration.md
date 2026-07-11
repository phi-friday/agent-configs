# Review and Integration

The controller owns integration. Subagent reports are inputs, not proof.

## Read Every Result First

Before editing or running final checks, read all returned reports.

Create a small integration map:

```text
Task                 Files touched          Status              Concern
────────────────────────────────────────────────────────────────────────
Auth copy update     login.tsx, copy.ts     DONE                none
Pricing test audit   pricing.test.ts        DONE_WITH_CONCERNS  flaky setup
Docs references      README.md              DONE                none
```

## Spec Compliance Before Quality

First ask:

- Did the subagent do exactly what was requested?
- Did it miss any acceptance criteria?
- Did it add unrequested behavior?
- Did it touch files outside scope?

Only after this passes, ask:

- Is the implementation maintainable?
- Are names and boundaries consistent?
- Are tests behavior-focused?
- Did parallel work create duplication or inconsistent patterns?

## File-Based Large-Slice Review

For larger or higher-risk slices, use one read-only task reviewer with local handoff.

Use the Review Assignment template in `references/subagent-prompts.md` and pass:

- task brief file (`local://...`) with exact target and scope
- implementation report file (`local://...` or `artifact://...`) with concrete findings
- review package file (`local://...` or `artifact://...`) with exact target/evidence and diff/evidence bundle

Do not force this flow for every small task.

## Conflict Checks

Check for:

- same file edited by multiple agents
- same concept named differently
- duplicated helpers or abstractions
- inconsistent error handling
- one task invalidating another's assumptions
- generated files or lockfiles changed unexpectedly
- test expectations that conflict across files

If conflicts exist, sequence a follow-up task rather than letting both versions stand.

## Review Loop

```text
agent result
  ↓
spec compliance review
  ↓ if issues
focused fix
  ↓
quality/integration review
  ↓ if issues
focused fix
  ↓
central verification
```

Do not move to final verification while known spec gaps remain.

## Final Verification

Run relevant checks after all changes are integrated.

Choose checks based on changed scope:

- tests added or modified by the work
- tests for directly affected modules
- typecheck or lint only when relevant to the changed language/project
- targeted e2e or browser checks for user-facing flows

Do not claim broad verification unless it was actually run.

## Final Report Shape

```md
## Parallelized Work

## Integrated Changes

## Review Findings

## Verification

## Remaining Risks
```

Remaining risks should be explicit, not hidden behind “done.”
