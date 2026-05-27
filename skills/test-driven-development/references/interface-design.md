# Interface Design For TDD

A hard-to-write test is often feedback that the interface is unclear or too coupled.

## Prefer Deep Modules

Good module shape:

```text
small public interface
large hidden implementation
```

Ask:

- Can this interface have fewer methods?
- Can parameters be simpler?
- Can complexity move behind the interface?
- Can the test use caller vocabulary instead of implementation vocabulary?

## Accept Dependencies, Do Not Create Them Internally

Testable:

```ts
function processOrder(order: Order, paymentGateway: PaymentGateway) {
  return paymentGateway.charge(order.total);
}
```

Hard to test:

```ts
function processOrder(order: Order) {
  const paymentGateway = new StripeGateway(process.env.STRIPE_KEY);
  return paymentGateway.charge(order.total);
}
```

Dependency injection should be boring. Do not build a container unless the project already uses one.

## Return Results When Possible

Prefer functions that return observable results over functions that only mutate hidden state.

Testable:

```ts
function calculateDiscount(cart: Cart): Discount {}
```

Harder to test:

```ts
function applyDiscount(cart: Cart): void {
  cart.total -= calculateDiscount(cart).amount;
}
```

Mutation is sometimes correct, but the public interface still needs an observable result or read path.

## Use Wished-For API

In RED, write the test using the API you wish existed.

```ts
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });

  expect(result.error).toBe('Email required');
});
```

Then implement the smallest interface that satisfies that caller.

## When Test Setup Is Huge

Large setup usually means one of these is true:

- the public interface requires too much unrelated state
- dependencies are created internally
- the module is shallow and leaks implementation details
- the behavior belongs behind a different interface

Simplify the design before adding more helpers.
