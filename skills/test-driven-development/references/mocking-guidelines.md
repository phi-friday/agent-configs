# Mocking Guidelines

Mocks are tools to isolate system boundaries. They are not the behavior under test.

## Mock Only Boundaries

Acceptable mock targets:

- external APIs
- payment/email/SMS providers
- time and randomness
- filesystem when real filesystem would be unsafe or too slow
- database only when a test database is not practical
- network, process, or OS boundary

Avoid mocking:

- internal modules you own
- domain services called by the unit under test
- private methods
- components just because setup feels inconvenient
- high-level methods whose side effects the test depends on

## Never Test Mock Behavior

Bad:

```ts
test('renders sidebar', () => {
  render(<Page />);

  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

This proves the mock rendered, not that the page works.

Better:

```ts
test('shows navigation on the page', () => {
  render(<Page />);

  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

## Before Adding A Mock

Ask:

1. What real dependency am I replacing?
2. Is it a system boundary or internal collaborator?
3. What side effects does the real dependency have?
4. Does this test depend on any of those side effects?
5. Can a real dependency or test double be simpler than a mock?

If unsure, run with the real dependency first to learn what the test actually needs.

## Mock At The Lowest Useful Level

If a high-level method both performs slow external work and updates local state, do not mock the whole high-level method when the test depends on the state update.

Mock the slow external operation instead.

```text
BAD: mock addServer(), then test duplicate detection
GOOD: keep addServer() real, mock only slow server startup
```

## Complete Mock Data

Mock real response shapes completely enough for downstream consumers.

Bad:

```ts
const response = { id: 'u1' };
```

Better:

```ts
const response = {
  id: 'u1',
  name: 'Alice',
  metadata: { requestId: 'req-1' },
};
```

If the API shape is unknown, read docs, fixtures, or captured responses before mocking.

## Test-Only Production Code

Never add production methods or branches that exist only for tests.

Bad:

```ts
class Session {
  async destroyForTestOnly() {}
}
```

Better:

```ts
// test-utils/session.ts
export async function cleanupSession(session: Session) {}
```

Production APIs should exist for production behavior.

## Red Flags

- assertion checks mock existence
- mock setup is larger than the behavior under test
- test fails when a mock is removed but real behavior still works
- cannot explain why the mock is needed
- mock omits fields from a real API response
- production code gains methods only called by tests
