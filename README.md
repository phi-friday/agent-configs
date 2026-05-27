# Agent Configs

[English](README.md) | [한국어](README.kr.md)

Personal agent configuration and first-party AI-agent skills.

## Skills

First-party skill sources live under [`in-progress/`](./in-progress/). Approved skills are published into [`skills/`](./skills/) by [`publish-skills.py`](./publish-skills.py); generated skill output should not be edited directly.

Current first-party skills:

- [`explore-and-frame`](./in-progress/explore-and-frame/): explore ambiguous work, map code context, compare options, and frame decisions before implementation.
- [`parallel-execution`](./in-progress/parallel-execution/): split independent work across subagents while keeping integration and final verification with the controller.
- [`quality-gates`](./in-progress/quality-gates/): require fresh evidence before claiming work is done, fixed, passing, reviewed, or ready to merge.
- [`root-cause-debugging`](./in-progress/root-cause-debugging/): confirm the real root cause of bugs, regressions, flakes, and integration failures before fixing them.
- [`test-driven-development`](./in-progress/test-driven-development/): implement features, fixes, refactors, and behavior changes test-first.

Each first-party skill keeps an English skill definition and README alongside Korean versions (`SKILL.kr.md`, `README.kr.md`).

Some or all custom skills in this repository may be inspired by, adapted from, or derived from works in the external reference repositories listed below. Those upstream works are licensed under the MIT License, and their copyright and license notices must be preserved when their work is copied, modified, or substantially incorporated here.

## External references

The repositories under [`references/`](./references/) are external Git submodules used as reference material while building custom skills for this repository. They are not authored by this repository unless explicitly stated otherwise.

| Path | Source | License |
|---|---|---|
| [`references/mattpocock/skills`](./references/mattpocock/skills) | <https://github.com/mattpocock/skills> | MIT |
| [`references/obra/superpowers`](./references/obra/superpowers) | <https://github.com/obra/superpowers> | MIT |
| [`references/Fission-AI/OpenSpec`](./references/Fission-AI/OpenSpec) | <https://github.com/Fission-AI/OpenSpec> | MIT |

Clone with submodules:

```sh
git clone --recurse-submodules <repo-url>
```

Initialize submodules after cloning:

```sh
git submodule update --init --recursive
```

## License notices

Each external reference repository keeps its own MIT license file inside its submodule directory.

For custom skills or other files in this repository that copy, modify, or substantially incorporate material from those references, preserve the relevant upstream copyright and MIT license notice. See [`NOTICE.md`](./NOTICE.md) for third-party notice tracking.
