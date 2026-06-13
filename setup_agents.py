#!/usr/bin/env -S uv run --script --python 3.14t
# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = []
# ///
# ruff: noqa: T201,D103

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

from install_locked_skills import install_missing_locked_skills

LOG_PREFIX = "[setup-agents]"


def log(message: str) -> None:
    print(f"{LOG_PREFIX} {message}")


def fail(message: str) -> NoReturn:
    print(f"{LOG_PREFIX} {message}", file=sys.stderr)
    raise SystemExit(1)


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def default_link_path() -> Path:
    return Path.home() / ".agents"


def is_same_directory(left: Path, right: Path) -> bool:
    try:
        return left.samefile(right)
    except OSError:
        return False


def create_windows_junction(target: Path, link_path: Path) -> None:
    command = os.environ.get("COMSPEC", "cmd.exe")
    try:
        subprocess.run(  # noqa: S603
            [command, "/c", "mklink", "/J", os.fspath(link_path), os.fspath(target)],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        fail(
            "failed to create directory junction "
            f"({error.returncode}): {link_path} -> {target}"
        )


def create_directory_link(target: Path, link_path: Path) -> None:
    try:
        link_path.symlink_to(target, target_is_directory=True)
    except OSError as error:
        if os.name != "nt":
            fail(f"failed to create symlink: {link_path} -> {target}: {error}")

        log(f"symlink failed; creating Windows directory junction instead: {error}")
        create_windows_junction(target, link_path)


def ensure_agent_link(target: Path, link_path: Path) -> None:
    log(f"script dir: {target}")
    log(f"link path : {link_path}")

    if link_path.exists() or link_path.is_symlink():
        if link_path.is_dir() and is_same_directory(link_path, target):
            log("link path already points to this repo")
            return

        fail(f"link path already exists: {link_path}")

    log("creating link...")
    create_directory_link(target, link_path)

    if not link_path.is_dir() or not is_same_directory(link_path, target):
        fail(f"created link does not point to this repo: {link_path}")


def lock_file_for(root: Path) -> Path:
    lock_file = root / ".skill-lock.json"
    legacy_lock = root / "skill-lock.json"
    if not lock_file.is_file() and legacy_lock.is_file():
        return legacy_lock
    return lock_file


def install_lock_managed_skills(root: Path) -> None:
    log("installing lock-managed skills...")
    install_missing_locked_skills(repo_root=root, lock_file=lock_file_for(root))


def main() -> None:
    root = repo_root()
    link_path = default_link_path()

    ensure_agent_link(root, link_path)
    install_lock_managed_skills(root)

    log("done")
    log(f"{link_path} -> {root}")


if __name__ == "__main__":
    main()
