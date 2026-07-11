# Test Quality

Good TDD tests describe observable behavior through public interfaces.

## Good Tests

A good test:

- exercises real code paths
- uses public APIs, commands, UI, or caller-facing interfaces
- names behavior the user/caller cares about
- survives internal refactors
- fails when behavior breaks
- has one clear reason to fail

Example:

```ts
test('createUser makes the user retrievable', async () => {
  const user = await createUser({ name: 'Alice' });

  const retrieved = await getUser(user.id);

  expect(retrieved.name).toBe('Alice');
});
```

This tests behavior through the interface: after creation, the user can be retrieved.

## Bad Tests

A bad test couples to implementation:

- tests private methods
- asserts internal function calls
- asserts call order unless call order is the behavior
- queries storage directly when a public read interface exists
- breaks when code is refactored but behavior is unchanged
- name describes how the code works instead of what callers observe

Example:

```ts
test('createUser inserts a row', async () => {
  await createUser({ name: 'Alice' });

  const row = await db.query('select * from users where name = ?', ['Alice']);

  expect(row).toBeDefined();
});
```

This verifies storage shape, not caller behavior. Prefer reading through the interface unless persistence itself is the public contract.

## One Behavior Per Test

Split tests when the name needs “and.”

Bad:

```ts
test('validates email and trims whitespace and saves user', async () => {});
```

Better:

```ts
test('rejects invalid email', async () => {});
test('trims whitespace before saving user name', async () => {});
test('saves valid user', async () => {});
```

## Red Failure Quality

A RED failure is useful only when it proves the behavior is missing.

Good RED failure:

```text
Expected: "Email required"
Received: undefined
```

Bad RED failure:

```text
Cannot find module '../submit-form'
```

Fix setup/import/type errors until the test fails for the behavior reason.

## Tautological Test Risk

Red flags for tautologies:

- The assertion only compares values derived from test setup, fixtures, or mock output.
- The expected value is produced by the same logic as production.
- The assertion only proves the test fixture or mock data exists.

These tests can pass while a plausible bug slips through.

- Can you describe a single realistic production bug that this test would catch and the mutation that causes it?
- If no, redesign the test seam (usually the public interface) before writing the test.
- Define that mutation while fixture/mock/setup inputs stay constant; if the test still passes, it is not ready for RED.
- If the assertion only checks setup/fixture/mock-derived values, treat it as a tautology risk.

Examples:

Bad (likely tautology):

```ts
test('normalizes display name', async () => {
  const input = '  alice  ';
  const expected = normalize(input); // same logic as production

  const actual = normalize(input);

  expect(actual).toBe(expected);
});
```

Good:

```ts
test('trims user name before saving user', async () => {
  const created = await createUser({ name: '  alice  ' });

  const fetched = await getUser(created.id);

  expect(fetched.name).toBe('alice');
});
```

The good test fails if persistence, save, or normalization behavior changes incorrectly.

## Public Interface Rule

If a test can only be written by reaching into internals, treat that as design feedback:

```text
hard to test = hard to use or too coupled
```

First try to improve the public interface rather than testing internals.
