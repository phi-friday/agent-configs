# Root Cause Tracing

Trace backward from the symptom until you find where bad state, bad input, or a bad assumption first entered the system.

## Core Rule

```text
Fix the source, not the crash site.
```

The line that throws is often only the first place the system can no longer tolerate already-bad state.

## Backward Trace

Use this shape for deep stack failures:

```text
symptom
  ↑ immediate failing operation
  ↑ caller and arguments
  ↑ earlier transformation
  ↑ source of invalid state or assumption
```

At each level ask:

- What exact value or state is bad here?
- Was it already bad on entry?
- Who called this and with what arguments?
- Which config, environment, lifecycle event, persisted state, cache, or dependency influenced it?
- Where is the first point it diverges from expected behavior?

Stop only when you find the first divergence.

## Boundary Trace

For multi-component systems, inspect boundaries before proposing fixes.

```text
producer ──payload/config/state──▶ boundary ──payload/config/state──▶ consumer
             expected? actual?                 expected? actual?
```

Record for each boundary:

- input
- output
- visible environment/config
- state read
- state written
- ordering/lifecycle assumptions
- whether the value was already bad before the boundary

This identifies which component first produced the bad result.

## Working-vs-Broken Comparison

If a similar path works, compare every difference:

- input shape
- config and environment
- dependency versions
- initialization order
- lifecycle timing
- ownership and state mutation
- auth/session/user context
- serialization/deserialization
- caching key and invalidation
- external API contract

Do not dismiss a difference as irrelevant until a probe rules it out.

## Temporary Stack Instrumentation

When manual tracing stalls, add a targeted temporary diagnostic at the boundary or dangerous operation.

Include:

- unique prefix such as `[DEBUG-a4f2]`
- value being traced
- caller or stack trace when useful
- cwd, environment, config, tenant/user/session identifiers when relevant
- timestamp or sequence number for ordering bugs

Remove temporary diagnostics before completion unless deliberately promoted to permanent observability.
