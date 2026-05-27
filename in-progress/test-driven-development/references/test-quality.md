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

## Public Interface Rule

If a test can only be written by reaching into internals, treat that as design feedback:

```text
hard to test = hard to use or too coupled
```

First try to improve the public interface rather than testing internals.
