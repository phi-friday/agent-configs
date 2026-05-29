# Repository Guidelines

## Project Overview

This repository holds personal AI-agent configuration and custom skills. First-party skill work is organized locally, with external reference repositories vendored as Git submodules under `references/` for inspiration, comparison, and license provenance.

## Architecture & Data Flow

- `publish_skills.py` is the main orchestration script. It discovers publishable skills under `in-progress/*/SKILL.md`, checks `.skill-lock.json`, removes unmanaged skill outputs from `skills/`, copies publishable skill directories into `skills/`, and updates each published `README.md` with referenced submodule commit metadata.
- Publishing is intentionally file-based and deterministic: paths are `pathlib.Path`, skill lists are sorted, and slow I/O work is parallelized with `ThreadPoolExecutor`.
- External material flows through `references/` only. If custom skill content copies or substantially derives from a reference repo, preserve the relevant MIT notice in `NOTICE.md` and document reference paths in the skill docs.
- Runtime consumption is via `setup.sh`, which links this repository to `~/.agents`.

## Key Directories

- `in-progress/`: Draft first-party skills. Typical shape: `SKILL.md`, `SKILL.kr.md`, `README.md`, `README.kr.md`, and optional `references/` support docs/scripts.
- `skills/`: Published skill output directories used by agent tooling. Current published folders are ignored by `skills/.gitignore`; treat generated output carefully and prefer editing source material before publishing.
- `references/`: External Git submodules (`mattpocock/skills`, `obra/superpowers`, `Fission-AI/OpenSpec`). Do not treat their source or tests as first-party code.
- `.omp/`: Harness/tooling integration; `.omp/lsp.yaml` starts Pyrefly LSP through `uvx`.

## Development Commands

```sh
# Populate external reference material
git submodule update --init --recursive

# Link this repo as the active agent config
./setup.sh

# Publish skills from in-progress/ into skills/; this removes unmanaged skill outputs
uv run --script publish_skills.py

# Python lint/format
ruff check .
ruff check . --fix
ruff format .

# Pyrefly language server command used by the harness
uvx pyrefly lsp
```

Before running `publish_skills.py`, check `.skill-lock.json`; the script refuses to overwrite lock-managed skill roots and deletes unmanaged existing directories in `skills/`.

## Code Conventions & Common Patterns

- Python targets 3.14 (`ruff.toml`, `pyrefly.toml`); `publish_skills.py` uses a PEP 723 `uv` script header and stdlib-only dependencies.
- Formatting: Ruff, 88 columns, spaces, double quotes, preview formatting enabled. Ruff and Pyrefly exclude `skills/**` and `references/**`.
- Type style: keep annotations explicit; Pyrefly checks unannotated definitions and promotes many type issues to errors.
- Error handling: use small validation helpers and fail fast with clear stderr messages plus `SystemExit(1)`.
- Shelling out: centralize subprocess calls behind helpers (`run_stdout`, `optional_stdout`) and use required vs optional command behavior intentionally.
- Determinism: sort filesystem-derived lists before acting; keep generated Markdown marker blocks stable.
- Markdown skills commonly use frontmatter, imperative headings, explicit Always/Never rules, examples, and adjacent reference docs rather than hidden implementation assumptions.

## Important Files

- `publish_skills.py`: Publish pipeline and reference-commit marker updater.
- `.skill-lock.json`: Lock file for protected skill roots.
- `README.md`: Repository purpose, submodule setup, and reference/license policy.
- `NOTICE.md`: Third-party MIT notice tracking for copied or derived material.
- `.gitmodules`: External reference repository declarations.
- `ruff.toml`: Lint and format policy.
- `pyrefly.toml`: Static typechecking policy.
- `.omp/lsp.yaml`: Pyrefly LSP launch configuration.
- `setup.sh`: Creates `~/.agents` symlink to this repo.
- `skills/.gitignore`: Lists ignored published skill output directories.

## Runtime/Tooling Preferences

- Prefer `uv`/`uvx` for Python script and tool execution when commands are not already installed.
- Required local tools for normal maintenance: `git`, `uv`, `ruff`, and Pyrefly tooling.
- Keep `references/` initialized when updating skills that cite upstream material; `publish_skills.py` records referenced submodule HEAD commits in published README files.
- Do not run checks over `references/**` or generated `skills/**` unless intentionally working inside those external/generated trees.

## Testing & QA

- No first-party automated test suite or test runner is defined at the repository root.
- External tests under `references/**` belong to their upstream repositories and are reference material only.
- For Python changes, run the narrowest relevant Ruff/Pyrefly checks and exercise the changed behavior directly. For `publish_skills.py`, prefer temporary directories via `REPO_ROOT`, `IN_PROGRESS_DIR`, `SKILLS_DIR`, and `LOCK_FILE` rather than mutating real skill outputs.
- Follow the repository's TDD guidance in `in-progress/test-driven-development/`: test observable behavior through public interfaces, cover edge/error cases, avoid private-method and call-order assertions, and do not add test-only production branches.
