#!/usr/bin/env -S uv run --script --python 3.14t
# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = []
# ///
# ruff: noqa: T201,D103

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from itertools import groupby
from pathlib import Path
from typing import NoReturn


@dataclass(frozen=True, slots=True)
class LockedSkill:
    name: str
    source: str
    skill_path: str
    ref: str | None = None
    source_type: str | None = None


type CommandRunner = Callable[[list[str]], None]
type JsonValue = (
    str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]
)


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


def install_source(skill: LockedSkill, repo_root: Path | None = None) -> str:
    if skill.source_type == "local":
        source_path = Path(skill.source).expanduser()
        if not source_path.is_absolute():
            if repo_root is None:
                return skill.source
            source_path = repo_root / source_path
        return str(source_path.resolve())

    if skill.ref is None:
        return skill.source

    if "#" in skill.ref:
        fail(f"invalid ref for lock-managed skill {skill.name}: {skill.ref}")

    _, separator, existing_ref = skill.source.rpartition("#")
    if not separator:
        return f"{skill.source}#{skill.ref}"
    if existing_ref == skill.ref:
        return skill.source

    fail(
        "conflicting refs for lock-managed skill "
        f"{skill.name}: source has {existing_ref}, metadata has {skill.ref}"
    )


def locked_skill_from_metadata(
    name: str, metadata: dict[str, JsonValue]
) -> LockedSkill | None:
    raw_source = metadata.get("source")
    raw_source_url = metadata.get("sourceUrl")
    source = None
    if isinstance(raw_source, str) and raw_source:
        source = raw_source
    elif isinstance(raw_source_url, str) and raw_source_url:
        source = raw_source_url

    skill_path = metadata.get("skillPath")
    raw_ref = metadata.get("ref")
    raw_source_type = metadata.get("sourceType")
    if source is None or not isinstance(skill_path, str) or not skill_path:
        return None
    if raw_ref is not None and (not isinstance(raw_ref, str) or not raw_ref):
        fail(f"invalid ref for lock-managed skill {name}")
    if raw_source_type is not None and (
        not isinstance(raw_source_type, str) or not raw_source_type
    ):
        fail(f"invalid sourceType for lock-managed skill {name}")

    return LockedSkill(
        name=name,
        source=source,
        skill_path=skill_path,
        ref=raw_ref,
        source_type=raw_source_type,
    )


def locked_skills(lock_file: Path) -> list[LockedSkill]:
    if not lock_file.is_file():
        fail(f"missing skill lock file: {lock_file}")

    with lock_file.open("r", encoding="utf-8") as file:
        lock = json.load(file)

    if not isinstance(lock, dict):
        return []

    skills = lock.get("skills", {})
    if not isinstance(skills, dict):
        return []

    locked: list[LockedSkill] = []
    for name, raw_metadata in skills.items():
        if not isinstance(name, str) or not name:
            continue
        if not isinstance(raw_metadata, dict):
            continue

        skill = locked_skill_from_metadata(name, raw_metadata)
        if skill is not None:
            locked.append(skill)

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
        "--agent",
        "codex",
        "--yes",
        "--full-depth",
    ]


def run_command(args: list[str], cwd: Path) -> None:
    if not args:
        fail("missing command")

    executable = shutil.which(args[0])
    if executable is None:
        fail("missing npx executable; install Node.js/npm before running setup")

    try:
        subprocess.run([executable, *args[1:]], cwd=cwd, check=True)  # noqa: S603
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

    missing_with_sources = sorted(
        ((install_source(skill, repo_root), skill) for skill in missing),
        key=lambda item: (item[0], item[1].name),
    )
    for source, source_skills_iter in groupby(
        missing_with_sources, key=lambda item: item[0]
    ):
        source_skills = [skill for _, skill in source_skills_iter]
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
