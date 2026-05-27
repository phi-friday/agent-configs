# Timer Control and Condition-Based Waiting

Use this for flaky tests or async behavior where the code currently guesses with sleeps.

## Priority

```text
1. Fake timer / virtual clock when the behavior is timer-driven.
2. Condition-based waiting when real async work must complete.
3. Fixed sleep only when elapsed time itself is the behavior under test.
```

Do not start with polling if the test runner can control the clock directly.

## Prefer Fake Timers For Timer-Driven Code

Use fake timers when the code under test depends on:

- `setTimeout`
- `setInterval`
- debounce/throttle timers
- retry backoff timers
- scheduled expiration
- `Date.now()` or `new Date()`

Fake timers make the test deterministic without waiting for real time.

### Vitest

Vitest supports fake timers with `vi.useFakeTimers()`, virtual clock advancement with `vi.advanceTimersByTime()` / `vi.runAllTimers()`, and system clock control with `vi.setSystemTime()`.

```ts
import { afterEach, expect, test, vi } from 'vitest';

afterEach(() => {
  vi.useRealTimers();
});

test('runs after one second', () => {
  vi.useFakeTimers();

  const fn = vi.fn();
  setTimeout(fn, 1000);

  expect(fn).not.toHaveBeenCalled();

  vi.advanceTimersByTime(1000);

  expect(fn).toHaveBeenCalledTimes(1);
});
```

Use `vi.setSystemTime(date)` for code that reads the current date. Setting system time does not by itself fire pending timers.

### Jest

Jest supports the same shape: `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, `jest.runAllTimers()`, `jest.setSystemTime()`, and `jest.useRealTimers()`.

```ts
afterEach(() => {
  jest.useRealTimers();
});

test('runs after one second', () => {
  jest.useFakeTimers();

  const fn = jest.fn();
  setTimeout(fn, 1000);

  expect(fn).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);

  expect(fn).toHaveBeenCalledTimes(1);
});
```

Use `jest.setSystemTime(date)` for date-dependent code. It changes the mocked current time but does not itself fire timers.

### Bun

Bun exposes Jest-compatible fake timer APIs from `bun:test`: `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, `jest.runAllTimers()`, `jest.runOnlyPendingTimers()`, `jest.advanceTimersToNextTimer()`, `jest.clearAllTimers()`, `jest.getTimerCount()`, `jest.setSystemTime()`, and `jest.useRealTimers()`.

```ts
import { expect, jest, test } from 'bun:test';

test('runs after one second', () => {
  jest.useFakeTimers();

  const fn = jest.fn();
  setTimeout(fn, 1000);

  expect(fn).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);

  expect(fn).toHaveBeenCalledTimes(1);

  jest.useRealTimers();
});
```

Use `jest.setSystemTime(date)` or `setSystemTime(date)` for date-dependent code.

```ts
import { expect, setSystemTime, test } from 'bun:test';

test('uses a fixed date', () => {
  setSystemTime(new Date('2020-01-01T00:00:00.000Z'));

  expect(new Date().getFullYear()).toBe(2020);

  setSystemTime();
});
```

Bun's public docs can lag here: the Dates and Times page may still say timer mocking is not implemented. Verify against the project's Bun version when in doubt. On Bun 1.3.14, `jest.advanceTimersByTime()` advances `setTimeout` and `setInterval` in `bun:test`.

## Use Condition-Based Waiting When Fake Timers Are Not Enough

Use condition-based waiting when the test must wait for real work that fake timers do not control:

- file system changes
- network or browser/e2e behavior
- database writes
- worker, queue, or subprocess completion
- framework rendering that is not purely timer-driven
- external systems
- real async work outside Bun/Jest/Vitest fake timer control

Core rule:

```text
Wait for the condition you need, not a guessed duration.
```

A sleep only proves that the machine was fast enough this time.

## Replace Guessed Sleeps

Before:

```ts
await sleep(300);
expect(result).toBeDefined();
```

After:

```ts
await waitFor(() => getResult() !== undefined, 'result to exist');
expect(getResult()).toBeDefined();
```

Condition-based waiting still uses a short sleep internally as a polling interval. That interval is not the assertion. The assertion is the condition.

## Generic Helper

```ts
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000,
  intervalMs = 10,
): Promise<T> {
  const startedAt = Date.now();

  while (true) {
    const value = condition();
    if (value) return value;

    if (Date.now() - startedAt > timeoutMs) {
      throw new Error(`Timed out waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}
```

## Patterns

| Need | Pattern |
|---|---|
| Event appears | `waitFor(() => events.find((e) => e.type === 'DONE'), 'DONE event')` |
| State transition | `waitFor(() => machine.state === 'ready', 'machine ready')` |
| Count reaches threshold | `waitFor(() => items.length >= 2 && items, 'two items')` |
| File exists | `waitFor(() => existsSync(path), 'file to exist')` |
| Custom predicate | `waitFor(() => records.find(matches), 'matching record')` |

## Correct Fixed Sleep Use

A fixed delay is acceptable only when timing itself is the behavior under test.

Requirements:

1. First wait for the triggering condition.
2. Base the delay on known product behavior.
3. Document why that duration is required.

Example:

```ts
await waitFor(() => events.some((e) => e.type === 'STARTED'), 'start event');
await sleep(220); // debounce is 100ms; wait for two debounce windows plus margin
expect(flushCount).toBe(1);
```

## Common Mistakes

- using condition polling when fake timers could advance the clock directly
- forgetting to restore real timers after fake timer tests
- assuming `setSystemTime()` fires pending timers
- polling stale cached data instead of reading fresh state inside the loop
- polling too fast and creating CPU noise
- no timeout, causing hung tests
- asserting only that “something happened” instead of the specific condition
