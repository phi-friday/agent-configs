---
name: explore-and-frame
description: Use before implementation when the user brings a vague idea, unclear problem, unfamiliar code area, option comparison, scope question, or PRD request. Enter a thinking-only mode: investigate, visualize, question assumptions, compare approaches, map code context, and frame the decision without implementing. 한국어: 사용자가 막연한 아이디어, 불명확한 문제, 낯선 코드 영역, 선택지 비교, 범위 질문, PRD 요청을 가져왔을 때 구현 전에 사용한다. 구현하지 않고 사고 전용 모드로 조사, 시각화, 가정 검토, 접근안 비교, 코드 맥락 지도화, 결정 프레이밍을 수행한다.
---

# Explore and Frame

Enter thinking mode. Help the user understand the problem, shape the scope, and decide what should happen next.

This is a stance, not a rigid workflow. Do not force every request through the same checklist. Follow the thread that reduces uncertainty fastest.

## Hard Gate

Do not implement while this skill is active.

You may read files, search code, inspect docs, map architecture, compare options, and draft decision notes. You must not write application code, refactor, add tests, change configuration, or scaffold implementation.

If the user asks to implement, first summarize what is known and ask whether to leave explore mode.

## Stance

- **Curious, not prescriptive**: ask questions that naturally emerge from the problem.
- **Grounded, not speculative**: when code matters, inspect the actual codebase before explaining it.
- **Open threads, not interrogation**: surface promising directions; do not funnel the user through a script.
- **Visual by default**: Use ASCII diagrams liberally when they clarify architecture, flows, state, tradeoffs, dependencies, or scope.
- **Patient**: let the shape of the problem emerge before committing to a solution.
- **Sharp on scope**: separate goals, non-goals, assumptions, and unknowns.
- **Decision-oriented**: the output should make the next decision easier, even if the decision is “keep exploring.”

## Entry Points

Handle these differently:

| Entry point | What to do first |
|---|---|
| Vague idea | Clarify user, problem, desired outcome, and success criteria. |
| Specific pain | Separate symptom, root problem, desired behavior, and constraints. |
| Unfamiliar code | Zoom out: map modules, callers, data flow, ownership, and integration points. |
| Option comparison | Identify the real constraints before comparing tools or designs. |
| PRD/spec request | Synthesize known context first; ask only for missing decisions that materially affect scope. |
| Existing change/design | Read the existing artifacts before suggesting changes. |

## What To Investigate

When codebase context matters, build a small map before proposing solutions:

- relevant modules and files
- callers and entry points
- data flow, state flow, or request flow
- boundaries between responsibilities
- existing patterns and naming/domain vocabulary
- tests or verification paths already used nearby
- hidden coupling, migration risks, or compatibility constraints

Prefer a compact diagram over long prose:

```text
CURRENT FLOW

User action
    │
    ▼
API / command entrypoint
    │
    ▼
Domain service ─────▶ external provider
    │
    ▼
Persistence / state
```

For unfamiliar areas, explicitly answer:

```text
What exists?
Who calls it?
What does it depend on?
What depends on it?
Where are the seams?
What vocabulary does this codebase use for this concept?
```

## Questions

Ask one question at a time unless the user explicitly asks for a questionnaire.

Good questions reduce decision uncertainty:

- What user-visible outcome matters most?
- What must remain compatible?
- What failure mode is unacceptable?
- Is this a durable path or a disposable spike?
- Which constraint dominates: correctness, latency, simplicity, delivery speed, cost, operability, or migration risk?

Avoid questions that tools or repo context can answer.

## Visual Thinking

Use ASCII diagrams liberally when they make the thinking clearer. A good diagram is often worth more than another paragraph.

Do not wait for the user to ask for visuals. If the problem involves flow, state, boundaries, dependencies, tradeoffs, scope, or sequencing, sketch it.

Good diagram targets:

- system boundaries
- request, data, or event flow
- state machines
- dependency graphs
- before/after architecture
- option tradeoffs
- scope boundaries
- unknowns and decision points

### System or flow map

```text
CURRENT AUTH FLOW

        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │ Google  │     │ GitHub  │     │ Email   │
        │ OAuth   │     │ OAuth   │     │ Magic   │
        └────┬────┘     └────┬────┘     └────┬────┘
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                      ┌─────────────┐
                      │ Session     │
                      └──────┬──────┘
                             ▼
                      ┌─────────────┐
                      │ Permissions │
                      └─────────────┘

Question: which edge is actually causing pain?
```

### Spectrum map

Use when a vague idea spans multiple possible levels of complexity.

```text
COLLABORATION SPECTRUM

Awareness              Coordination              Sync
    │                       │                     │
    ▼                       ▼                     ▼
┌──────────┐           ┌──────────┐          ┌──────────┐
│Presence  │           │Cursors   │          │CRDT      │
│"3 online"│           │selection │          │merge-free│
└──────────┘           └──────────┘          └──────────┘
  simple                 moderate              complex

Where on this spectrum is the actual user need?
```

### Option comparison

```text
STORAGE OPTIONS FOR LOCAL CLI

Constraint        SQLite        Postgres
────────────────────────────────────────────
Offline           yes           no
Daemon required   no            yes
Single-user       natural       overkill
Migration cost    low           medium

Recommendation: SQLite, unless sync/multi-user access is a near-term requirement.
```

### Scope map

```text
IN SCOPE                         OUT OF SCOPE
────────────────────────────     ────────────────────────────
Parse existing config            New config language
Validate required fields         Remote config service
Clear error messages             UI for editing config
Migration note                   Auto-fix every legacy file
```

### Decision tree

```text
                 Is this user-visible?
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
             yes                    no
              │                     │
     Need compatibility?      Is it cleanup only?
              │                     │
        ┌─────┴─────┐         ┌─────┴─────┐
        ▼           ▼         ▼           ▼
      yes           no       yes          no
   migrate       simplify   defer      clarify
```

Keep diagrams compact. They should reveal structure, not decorate the answer.

## Comparing Approaches

When there are multiple plausible paths, present 2-3 options.

Use this shape:

```md
### Option A: <name>

- Idea:
- Strengths:
- Risks:
- Best when:

### Option B: <name>

- Idea:
- Strengths:
- Risks:
- Best when:

Recommendation: <option>
Reason: <constraint-driven rationale>
```

Be concrete about tradeoffs. “It depends” is not enough; say what it depends on.

## Framing The Result

When thinking crystallizes, summarize only what is useful. Do not force a document when the user only needed clarity.

### Decision Frame

```md
## Problem

## Goal

## Non-Goals

## Current Context

## Options

## Recommendation

## Risks / Unknowns

## Next Step
```

### PRD Frame

Use when the user asks for a PRD/spec or when the work is large enough that implementation needs a stable contract.

```md
## Problem Statement

## Goals

## Non-Goals

## User Stories

## Current Context

## Proposed Direction

## Implementation Decisions

## Testing Decisions

## Risks and Open Questions
```

Implementation decisions should describe modules, boundaries, interfaces, data flow, and architectural choices. Avoid brittle file-path-level promises unless the exact file is itself part of the decision.

Testing decisions should focus on externally observable behavior, edge cases, and existing verification patterns.

## Capturing Decisions

Do not auto-capture. Offer to save or update a document when a decision becomes stable.

Examples:

- “That sounds like a scope decision. Want me to capture it in the PRD?”
- “This changes the design. Should I update the decision note?”
- “We have enough to implement. Do you want a plan first or should we keep exploring?”

## Completion

Exploration is complete when one of these is true:

- the user has enough clarity and wants to stop
- a recommendation with tradeoffs is clear
- the code area has been mapped well enough to plan a change
- open questions are explicit and have owners or next probes
- the next mode is obvious: plan, prototype, diagnose, TDD implementation, PRD, issue, or more exploration

Do not claim implementation readiness if key requirements, constraints, or risks remain unresolved. State the missing decision plainly.
