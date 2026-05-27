# Defense-in-Depth After Root Cause

Use this only after tracing where invalid data or invalid state originates.

## Core Rule

```text
First find the source. Then decide which layers should prevent recurrence.
```

Do not add validation everywhere as a substitute for understanding the bug.

## When To Add Layers

Add multiple layers when:

- invalid input can enter through more than one public boundary
- mocks or alternate call paths bypass the first check
- a dangerous operation needs environment-specific protection
- future debugging needs permanent observability
- a domain invariant must never be violated internally

Do not add layers when a single source-level fix makes the invalid state impossible and extra checks would only duplicate noise.

## Layer Types

| Layer | Purpose |
|---|---|
| Boundary validation | Reject invalid user/API/CLI input early |
| Domain invariant | Prevent impossible internal state |
| Persistence guard | Prevent corrupt reads/writes or invalid migrations |
| Environment guard | Block dangerous operations in tests, CI, or production contexts |
| Permanent observability | Capture enough context if other layers fail |

## Application Process

1. Trace the bad data path from entry to symptom.
2. Mark every checkpoint where the data crosses a responsibility boundary.
3. Decide which checkpoints can catch distinct failure modes.
4. Add the smallest useful validation or guard at each selected checkpoint.
5. Test bypass paths, not only the normal entry path.

## Good Layering

```text
API boundary rejects missing project directory
  ↓
Domain service rejects empty project directory from internal callers
  ↓
Dangerous filesystem operation refuses unsafe cwd during tests
  ↓
Permanent diagnostic logs target path and caller for future forensics
```

Each layer catches a different class of recurrence.

## Bad Layering

```text
Add the same null check in five adjacent functions without tracing callers.
```

That hides uncertainty and creates maintenance noise.
