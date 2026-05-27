# Refactoring While Green

Refactor only when tests are green. Refactoring changes structure, not behavior.

## Allowed Refactors

- remove duplication
- improve names
- extract helpers behind the same public interface
- simplify conditionals
- reduce parameter lists
- move logic to the object/module that owns the data
- combine shallow pass-through modules
- hide complexity behind a smaller interface
- introduce value objects for repeated primitive rules

## Not Refactoring

These require a new failing test first:

- new behavior
- changed error handling
- changed public API contract
- new option/configuration
- different persistence format
- different external call behavior

## Refactor Loop

```text
GREEN
  ↓
small structural change
  ↓
run affected tests
  ↓
GREEN or revert/fix immediately
```

Do not batch several risky refactors before running tests.

## Keep Tests Stable

Tests should usually not change during refactor. If tests must change, ask why:

- Were tests coupled to implementation?
- Is the public contract actually changing?
- Did the old test assert the wrong behavior?

If behavior changes, leave refactor mode and start a new RED cycle.

## Cleanup Candidates

Look for:

- duplication created by GREEN implementation
- names that expose implementation rather than domain language
- long methods
- shallow modules
- feature envy
- primitive obsession
- existing code the new behavior reveals as problematic

## Stop Conditions

Stop refactoring when:

- tests are green
- names and duplication are acceptable
- further cleanup would broaden scope
- a desired change would alter behavior
