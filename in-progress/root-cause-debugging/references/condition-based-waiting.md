# Condition-Based Waiting

Use this for flaky tests or async behavior where the code currently guesses with sleeps.

## Core Rule

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

## Correct Timeout Use

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

- polling stale cached data instead of reading fresh state inside the loop
- polling too fast and creating CPU noise
- no timeout, causing hung tests
- asserting only that “something happened” instead of the specific condition
