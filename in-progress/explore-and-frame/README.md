# explore-and-frame

[English](README.md) | [한국어](README.kr.md)

`explore-and-frame` is an in-progress skill for pre-implementation exploration, problem framing, code-context discovery, option comparison, and PRD/decision-note drafting.

Its goal is not to “start building immediately.” Its goal is to clarify what should be built and why before implementation begins.

## File Layout

- `SKILL.md`: The actual skill definition. Its description includes both English and Korean so English and Korean requests can both trigger it.
- `SKILL.kr.md`: Korean translation of `SKILL.md`; use it as the source for reviewing or editing the skill in Korean.
- `README.md`: English source README explaining which reference elements were selected and how they were combined.
- `README.kr.md`: Korean translation of this README.

## Composition

This skill combines four reference roles into one exploration skill.

```text
brainstorming                       → questions and requirement clarification
openspec-explore                    → free-form exploration stance + strong visualization
historical zoom-out (removed)       → mapping the existing code at a higher level
to-spec (formerly to-prd)           → compressing settled decisions into a PRD/decision frame

                explore-and-frame
        explore → visualize → map context → compare options → frame decisions
```

It does not copy `brainstorming`’s heavy approval procedure for every task, and it keeps the flexibility of `openspec-explore`’s exploration stance. To keep exploration from ending vaguely, it adds `historical zoom-out`’s code-context mapping and `to-spec`’s documentation frame.

## Elements Taken From Each Reference

### `obra/superpowers/brainstorming`

Elements taken:

- Confirm intent, constraints, and success criteria before implementation.
- Ask one question at a time.
- Split possible approaches into 2–3 options with tradeoffs and a recommendation.
- Check the user’s goal and current project context first.
- Apply a YAGNI stance to cut unnecessary scope.

Adaptations:

- The original hard gate, spec storage, commit, and user-approval loop are not copied as-is.
- This skill is for exploration and framing, so documents are saved only when the user wants them.
- The question procedure is reduced from a checklist to “ask the one question that reduces the largest uncertainty.”

### `Fission-AI/OpenSpec` `openspec-explore`

Elements taken:

- The view that exploration is a stance, not a workflow.
- Explore mode for thinking, researching, forming hypotheses, comparing options, and summarizing without implementation.
- Keeping multiple threads open instead of forcing the user’s idea into one direction.
- Grounding code-related exploration in the actual codebase.
- The `Use ASCII diagrams liberally` principle.
- Visualizing problem space, current structure, options, risks, and unknowns.
- Offering to capture decisions instead of automatically saving them.

The visual side directly reflects these patterns:

| OpenSpec pattern | Form in this skill |
|---|---|
| architecture sketch | `System or flow map` |
| collaboration spectrum example | `Spectrum map` |
| option table | `Option comparison` |
| scope visualization | `Scope map` |
| decision path | `Decision tree` |

Adaptations:

- OpenSpec-specific CLI commands, change artifacts, `openspec status`, `proposal.md`, `design.md`, and other system dependencies were removed.
- Only visualization and exploration patterns that work in general codebases and general work conversations remain.
- “Update the OpenSpec artifact” is generalized into “offer to save a decision note or PRD.”

### `mattpocock/skills` historical `zoom-out` (removed)

Elements taken:

- Look one level above the details before diving into unfamiliar implementation.
- Identify related modules, callers, data flow, dependencies, and seams first.
- Explain using the project’s domain vocabulary.

Adaptations:

- The original is close to a very short instruction.
- This skill expands it into a `What To Investigate` section that makes code-exploration checks explicit.
- It connects that exploration to later option comparison and PRD/decision framing instead of stopping at explanation.

### `mattpocock/skills` `to-spec` (formerly `to-prd`)

Elements taken:

- Compress conversation and codebase understanding into a PRD-style document.
- Separate problem, goals, user stories, implementation decisions, and testing decisions.
- Write implementation decisions around modules, interfaces, boundaries, and data flow.
- Write testing decisions around external behavior, verification scope, and existing high-level testing seams, not implementation details.

Adaptations:

- The original includes publishing to an issue tracker; this skill does not require publishing.
- A PRD is not always produced. It is an option when the exploration result is stable enough or when the user asks for one.
- The intent to avoid excessive file paths and snippets is preserved, but generalized to allow paths when a decision is tied to specific files.

## Role Split Inside The Final Skill

```text
1. Entry Points
   - brainstorming requirement clarification
   - openspec-explore handling of many entry points

2. What To Investigate
   - historical zoom-out (removed) code-context mapping
   - openspec-explore codebase grounding

3. Questions
   - brainstorming one-question-at-a-time
   - questions focused on goal, constraints, and success criteria

4. Visual Thinking
   - openspec-explore ASCII-diagram-heavy exploration
   - flow, spectrum, option, scope, and decision-tree patterns

5. Comparing Approaches
   - brainstorming comparison of 2–3 approaches
   - constraint-driven recommendation

6. Framing The Result
   - to-spec (formerly to-prd) PRD structure
   - added decision frame for smaller tasks

7. Capturing Decisions
   - openspec-explore’s “offer instead of auto-saving” stance
```

## Intentionally Excluded

- Implementation-phase instructions
- Test-writing instructions
- OpenSpec-specific CLI usage
- GitHub issue publishing procedure
- Mandatory commit procedure
- A rule that every exploration must end in a PRD
- A procedure that forces a user-approval gate at every step

This skill handles only exploration and framing before implementation, not the entire implementation process.

## Reference Files

Review this skill again when these files change:

- `references/obra/superpowers/skills/brainstorming/SKILL.md`
- `references/obra/superpowers/skills/brainstorming/visual-companion.md`
- `references/obra/superpowers/skills/brainstorming/spec-document-reviewer-prompt.md`
- `references/Fission-AI/OpenSpec/src/core/templates/workflows/explore.ts`
- `references/Fission-AI/OpenSpec/openspec/explorations/explore-workflow-ux.md`
- `references/mattpocock/skills/skills/engineering/to-spec/SKILL.md`
- Historical upstream source for the removed `zoom-out` concept: https://github.com/mattpocock/skills/blob/694fa30311e02c2639942308513555e61ee84a6f/skills/engineering/zoom-out/SKILL.md (commit-pinned historical reference, not a current replacement)

## License Note

The reference repositories use the MIT License. If original text, checklists, templates, or scripts are substantially copied or modified into this repository, keep the notice in the root `NOTICE.md`.
