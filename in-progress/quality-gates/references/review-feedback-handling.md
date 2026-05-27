# Review Feedback Handling

Review feedback must be understood and verified before implementation.

## Response Pattern

```text
READ all feedback
UNDERSTAND each item
VERIFY against the codebase
DECIDE: fix, reject with reason, or ask clarification
IMPLEMENT one item/coherent group
TEST affected behavior
REPORT evidence
```

Do not implement the first item before reading the rest. Items may interact.

## Clarify Before Acting

If any item is unclear, ask before implementing.

Bad:

```text
I understand items 1,2,3 and will do those now. I'll ask about 4 later.
```

Good:

```text
I understand items 1,2,3. Need clarification on 4 before changing code because it may affect the same path.
```

## Evaluate External Feedback

Check:

- is the suggestion technically correct for this codebase?
- does it break existing behavior or compatibility?
- does current code have a reason for being this way?
- is the suggested feature actually used?
- does it conflict with prior user or architectural decisions?
- can it be verified with tests or code inspection?

If wrong, push back with technical reasoning and evidence.

## YAGNI Check

When feedback asks to “properly implement” an unused path:

1. search for actual usage
2. if unused, recommend removing or deferring
3. if used, implement properly with tests

Do not add unused professional-looking features just to satisfy review aesthetics.

## Implementation Order

For multiple feedback items:

1. clarify unclear items
2. fix blocking issues: broken behavior, security, data loss
3. fix simple safe items: typos, imports, clear missing checks
4. fix complex items: refactors, logic changes
5. test after each item or coherent group
6. verify no regressions

## Pushback Format

```md
I checked <evidence>. This suggestion would <technical consequence>. Current behavior is needed because <reason>. Recommend <alternative>.
```

Keep it factual. Do not defend ego.

## Correct Feedback Format

When feedback is correct, state the fix and evidence.

Good:

```text
Fixed missing validation in `search.ts`; invalid dates now throw a clear error. Targeted tests pass.
```

Avoid performative agreement or gratitude as a substitute for action.

## Resolution Map

For review batches, track every item:

```md
- [x] Item 1 — fixed in file.ts; test command passed
- [x] Item 2 — rejected; breaks backwards compatibility, evidence: ...
- [ ] Item 3 — needs clarification: ...
```

Do not claim “review addressed” until every item has a status and evidence.
