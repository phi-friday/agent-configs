# Agent Configs

Personal agent configuration and custom skills.

## Custom skills

Custom skills maintained for this repository live under [`skills/`](./skills/).

Some or all of the custom skills in this repository may be inspired by, adapted from, or derived from works in the external reference repositories listed below. Those upstream works are licensed under the MIT License, and their copyright and license notices must be preserved when their work is copied, modified, or substantially incorporated here.

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

This repository's own license is not declared unless a top-level `LICENSE` file is added.
