#!/usr/bin/env -S uv run --script --python 3.14t
# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = []
# ///
# ruff: noqa: T201,D103

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from itertools import groupby
from pathlib import Path
from typing import NoReturn, cast


@dataclass(frozen=True, slots=True)
class LockedSkill:
    name: str
    source: str
    skill_path: str


type CommandRunner = Callable[[list[str]], None]


def log(message: str) -> None:
    print(f"[install-locked-skills] {message}")


def fail(message: str) -> NoReturn:
    print(f"[install-locked-skills] {message}", file=sys.stderr)
    raise SystemExit(1)


def repo_paths() -> tuple[Path, Path]:
    script_dir = Path(__file__).resolve().parent
    repo_root = Path(os.environ.get("REPO_ROOT", script_dir)).resolve()
    lock_file = Path(
        os.environ.get("LOCK_FILE", repo_root / ".skill-lock.json")
    ).resolve()

    legacy_lock = repo_root / "skill-lock.json"
    if not lock_file.is_file() and legacy_lock.is_file():
        lock_file = legacy_lock

    return repo_root, lock_file


def source_arg(metadata: dict[str, object]) -> str | None:
    source = metadata.get("source")
    if isinstance(source, str) and source:
        return source

    source_url = metadata.get("sourceUrl")
    if isinstance(source_url, str) and source_url:
        return source_url

    return None


def locked_skills(lock_file: Path) -> list[LockedSkill]:
    if not lock_file.is_file():
        fail(f"missing skill lock file: {lock_file}")

    with lock_file.open("r", encoding="utf-8") as file:
        lock = cast("dict[str, object]", json.load(file))

    skills = lock.get("skills", {})
    if not isinstance(skills, dict):
        return []

    locked: list[LockedSkill] = []
    for name, raw_metadata in skills.items():
        if not isinstance(name, str) or not name:
            continue
        if not isinstance(raw_metadata, dict):
            continue

        metadata = cast("dict[str, object]", raw_metadata)
        source = source_arg(metadata)
        skill_path = metadata.get("skillPath")
        if source is None or not isinstance(skill_path, str) or not skill_path:
            continue

        locked.append(LockedSkill(name=name, source=source, skill_path=skill_path))

    return sorted(locked, key=lambda skill: skill.name)


def local_skill_file(repo_root: Path, skill: LockedSkill) -> Path:
    return repo_root / "skills" / skill.name / "SKILL.md"


def worker_count(item_count: int) -> int:
    if item_count <= 0:
        return 1
    return min(item_count, (os.cpu_count() or 1) + 4, 32)


def is_local_skill_installed(repo_root: Path, skill: LockedSkill) -> bool:
    return local_skill_file(repo_root, skill).is_file()


def missing_locked_skills(repo_root: Path, lock_file: Path) -> list[LockedSkill]:
    skills = locked_skills(lock_file)
    with ThreadPoolExecutor(max_workers=worker_count(len(skills))) as executor:
        installed = executor.map(partial(is_local_skill_installed, repo_root), skills)

    return [skill for skill, exists in zip(skills, installed) if not exists]


def install_command(source: str, skills: list[LockedSkill]) -> list[str]:
    skill_names = [skill.name for skill in skills]
    return [
        "npx",
        "--yes",
        "skills",
        "add",
        source,
        "--skill",
        *skill_names,
        "--global",
        "--yes",
        "--full-depth",
    ]


def run_command(args: list[str], cwd: Path) -> None:
    try:
        subprocess.run(args, cwd=cwd, check=True)  # noqa: S603
    except FileNotFoundError:
        fail("missing npx executable; install Node.js/npm before running setup")


def install_missing_locked_skills(
    *, repo_root: Path, lock_file: Path, runner: CommandRunner | None = None
) -> list[LockedSkill]:
    missing = missing_locked_skills(repo_root, lock_file)
    if not missing:
        log("all lock-managed skills are installed")
        return []

    def command_runner(args: list[str]) -> None:
        if runner is not None:
            runner(args)
            return
        run_command(args, cwd=repo_root)

    missing_by_source = groupby(
        sorted(missing, key=lambda skill: (skill.source, skill.name)),
        key=lambda skill: skill.source,
    )
    for source, source_skills_iter in missing_by_source:
        source_skills = list(source_skills_iter)
        skill_names = ", ".join(skill.name for skill in source_skills)
        log(f"install missing lock-managed skill(s): {skill_names}")
        try:
            command_runner(install_command(source, source_skills))
        except subprocess.CalledProcessError as error:
            fail(
                "failed to install lock-managed skill(s) "
                f"({error.returncode}): {skill_names}"
            )

    return missing


def main() -> None:
    repo_root, lock_file = repo_paths()
    install_missing_locked_skills(repo_root=repo_root, lock_file=lock_file)


if __name__ == "__main__":
    main()
