# Repository Guidelines

## Project Overview

This repository is a personal AI-agent configuration and first-party skill authoring repo. Canonical skill sources live in `in-progress/`; published/runtime copies live in `skills/`; external inspiration and provenance material lives in `references/` Git submodules.

## Architecture & Data Flow

- `publish_skills.py` is the main orchestration script. It discovers publishable skills under `in-progress/*/SKILL.md`, checks `.skill-lock.json`, removes unmanaged skill outputs from `skills/`, copies publishable skill directories into `skills/`, and updates each published `README.md` with referenced submodule commit metadata.
- Publishing is intentionally file-based and deterministic: paths are `pathlib.Path`, skill lists are sorted, and slow I/O work is parallelized with `ThreadPoolExecutor`.
- External material flows through `references/` only. If custom skill content copies or substantially derives from a reference repo, preserve the relevant MIT notice in `NOTICE.md` and document reference paths in the skill docs.
- Runtime consumption is via `setup_agents.py`, which links this repository to `~/.agents` and installs lock-managed skills.

## Key Directories

- `in-progress/`: first-party skill source of truth. Typical skill shape: `SKILL.md`, `SKILL.kr.md`, `README.md`, `README.kr.md`, plus optional `references/` and `scripts/`.
- `skills/`: published/runtime skill output. Prefer editing `in-progress/` and republishing instead of editing generated copies directly. Lock-managed external outputs are listed in `skills/.gitignore`.
- `references/`: external Git submodules (`mattpocock/skills`, `obra/superpowers`, `Fission-AI/OpenSpec`). Treat as vendored reference material, not first-party code.
- `.omp/`: harness integration. `.omp/lsp.yaml` starts Pyrefly and Ruff language servers through local `uv` tooling.

## Development Commands

```sh
# Populate external reference material
git submodule update --init --recursive

# Link this repo as the active agent config
uv run --script setup_agents.py

# Publish first-party skills from in-progress/ into skills/
uv run --script publish_skills.py

# Install missing lock-managed external skills only
uv run --script install_locked_skills.py

# Poe aggregate from pyproject.toml
uv run poe lint

# Individual tool commands; avoid invoking underscored Poe internals directly
uv run ruff format in-progress
uv run ruff check in-progress
uv run pyrefly check in-progress
uv run flake8 in-progress
```

For root Python script edits, run narrow direct checks with project-local tools, e.g. `uv run ruff check publish_skills.py install_locked_skills.py`. Use tools installed from `pyproject.toml` via `uv run` or Poe.

## Code Conventions & Common Patterns

- Python targets 3.14 behavior in tooling (`ruff.toml`, `pyrefly.toml`, `.python-version` is `3.14t`); `pyproject.toml` requires `>=3.13`.
- Formatting: Ruff, 88 columns, spaces, double quotes, preview formatting enabled. Ruff/Pyrefly exclude `skills/**` and `references/**`.
- Type style: keep annotations explicit. Pyrefly checks unannotated definitions and promotes many type issues to errors.
- Script style: stdlib-first, `pathlib.Path`, deterministic sorted filesystem lists, bounded `ThreadPoolExecutor` for slow independent I/O, small helpers for validation and subprocess calls.
- Error handling: fail fast with clear prefixed stderr messages plus `SystemExit(1)`; keep required vs optional subprocess behavior explicit (`run_stdout` vs `optional_stdout`).
- Markdown skill style: frontmatter, imperative headings, explicit Always/Never rules, concise examples, and adjacent reference docs instead of hidden assumptions. English and Korean files should stay aligned when both exist.

## Important Files

- `publish_skills.py`: Publish pipeline and reference-commit marker updater.
- `.skill-lock.json`: Lock file for protected skill roots.
- `README.md`: Repository purpose, submodule setup, and reference/license policy.
- `NOTICE.md`: Third-party MIT notice tracking for copied or derived material.
- `.gitmodules`: External reference repository declarations.
- `ruff.toml`: Lint and format policy.
- `pyrefly.toml`: Static typechecking policy.
- `.omp/lsp.yaml`: Pyrefly LSP launch configuration.
- `setup_agents.py`: Cross-platform setup entrypoint that links `~/.agents` to this repo and installs lock-managed skills.
- `skills/.gitignore`: Lists ignored published skill output directories.

## Runtime/Tooling Preferences

- Prefer `uv` for Python script/tool execution and lockfile-backed environments.
- Prefer `uv run poe lint` for the configured aggregate check. Use direct `uv run ruff ...`, `uv run pyrefly ...`, or `uv run flake8 ...` for narrow file- or tool-specific checks.
- Node/npm is required only for lock-managed skill installation through `npx skills add`.
- Keep `references/` initialized when updating skills that cite upstream material; publishing records referenced submodule commits in generated README marker blocks.
- Do not run checks over `references/**` or generated `skills/**` unless intentionally working inside external/generated trees.

## Testing & QA

- No first-party automated test suite or root `test` task is configured.
- For Python/script changes, run the narrowest relevant Ruff/Pyrefly/Flake8 checks and exercise changed behavior directly.
- For `publish_skills.py`, prefer temporary directories via `REPO_ROOT`, `IN_PROGRESS_DIR`, `SKILLS_DIR`, and `LOCK_FILE` instead of mutating real skill outputs.
- For `install_locked_skills.py`, verify lock parsing/missing-skill behavior with temporary `REPO_ROOT`/`LOCK_FILE`; avoid real global installs unless that is the behavior under test.
- Follow the repository's own skill guidance: behavior-first checks, public interfaces, fresh evidence before claiming done, and exact command/output scope in final reports.
