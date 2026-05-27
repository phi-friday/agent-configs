#!/usr/bin/env -S uv run --script --python 3.14t
# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = []
# ///
# ruff: noqa: T201,D103

from __future__ import annotations

import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

START_MARKER = "<!-- publish-skills:reference-commits:start -->"
END_MARKER = "<!-- publish-skills:reference-commits:end -->"


def log(message: str) -> None:
    print(f"[publish-skills] {message}")


def fail(message: str) -> None:
    print(f"[publish-skills] {message}", file=sys.stderr)
    raise SystemExit(1)


def require_dir(path: Path, label: str) -> None:
    if not path.is_dir():
        fail(f"missing {label}: {path}")


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        fail(f"missing {label}: {path}")


def run_stdout(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        args, cwd=cwd, check=True, stdout=subprocess.PIPE, text=True
    )
    return completed.stdout.strip()


def optional_stdout(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        args, cwd=cwd, check=False, capture_output=True, text=True
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def repo_paths() -> tuple[Path, Path, Path, Path]:
    script_dir = Path(__file__).resolve().parent
    repo_root = Path(os.environ.get("REPO_ROOT", script_dir)).resolve()
    in_progress_dir = Path(
        os.environ.get("IN_PROGRESS_DIR", repo_root / "in-progress")
    ).resolve()
    skills_dir = Path(os.environ.get("SKILLS_DIR", repo_root / "skills")).resolve()
    lock_file = Path(
        os.environ.get("LOCK_FILE", repo_root / ".skill-lock.json")
    ).resolve()

    legacy_lock = repo_root / "skill-lock.json"
    if not lock_file.is_file() and legacy_lock.is_file():
        lock_file = legacy_lock

    return repo_root, in_progress_dir, skills_dir, lock_file


def locked_skill_roots(lock_file: Path) -> set[str]:
    with lock_file.open("r", encoding="utf-8") as file:
        lock = json.load(file)

    roots: set[str] = set()
    skills = lock.get("skills", {})
    if not isinstance(skills, dict):
        return roots

    for name, metadata in skills.items():
        if isinstance(name, str) and name:
            roots.add(name.split("/", 1)[0])

        if not isinstance(metadata, dict):
            continue

        skill_path = metadata.get("skillPath")
        if not isinstance(skill_path, str):
            continue

        parts = Path(skill_path).parts
        if len(parts) >= 2 and parts[0] == "skills":
            roots.add(parts[1])

    return roots


def publishable_skills(in_progress_dir: Path) -> list[str]:
    return sorted(
        child.name
        for child in in_progress_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    )


def existing_skill_roots(skills_dir: Path) -> list[str]:
    return sorted(child.name for child in skills_dir.iterdir() if child.is_dir())


def submodule_paths(repo_root: Path) -> list[str]:
    gitmodules = repo_root / ".gitmodules"
    if not gitmodules.is_file():
        return []

    output = optional_stdout(
        [
            "git",
            "config",
            "--file",
            str(gitmodules),
            "--get-regexp",
            r"^submodule\..*\.path$",
        ],
        cwd=repo_root,
    )
    paths: list[str] = []
    for line in output.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            paths.append(parts[1])
    return sorted(paths)


def referenced_submodules(readme_text: str, submodules: list[str]) -> list[str]:
    referenced_paths = set(re.findall(r"`(references/[^`]+)`", readme_text))
    selected: list[str] = []
    for submodule in submodules:
        prefix = f"{submodule}/"
        if any(
            path == submodule or path.startswith(prefix) for path in referenced_paths
        ):
            selected.append(submodule)
    return selected


def worker_count(item_count: int) -> int:
    if item_count <= 0:
        return 1
    return min(item_count, (os.cpu_count() or 1) + 4, 32)


def run_threaded(items: Iterable[str], task: Callable[[str], None]) -> None:
    item_list = list(items)
    if not item_list:
        return

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count(len(item_list))
    ) as executor:
        futures = [executor.submit(task, item) for item in item_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def submodule_commits(repo_root: Path, submodules: list[str]) -> dict[str, str]:
    if not submodules:
        return {}

    def commit_for(submodule: str) -> tuple[str, str]:
        commit = run_stdout(
            ["git", "-C", str(repo_root / submodule), "rev-parse", "HEAD"],
            cwd=repo_root,
        )
        return submodule, commit

    commits: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count(len(submodules))
    ) as executor:
        futures = [executor.submit(commit_for, submodule) for submodule in submodules]
        for future in concurrent.futures.as_completed(futures):
            submodule, commit = future.result()
            commits[submodule] = commit
    return commits


def reference_commit_block(commits: dict[str, str], submodules: list[str]) -> str:
    commit_lines = [
        f"- `{submodule}`: `{commits[submodule]}`" for submodule in submodules
    ]

    return "\n".join([
        START_MARKER,
        "## Reference Commits",
        "",
        "Published against these submodule commits.",
        "",
        *commit_lines,
        END_MARKER,
    ])


def remove_existing_commit_block(text: str) -> str:
    pattern = re.compile(
        rf"\n*{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\n*", re.DOTALL
    )
    return pattern.sub("\n", text).rstrip() + "\n"


def with_reference_commit_block(text: str, block: str) -> str:
    if START_MARKER in text and END_MARKER in text:
        without_old = remove_existing_commit_block(text).rstrip()
        return f"{without_old}\n\n{block}\n"

    if "\n## License Note" in text:
        return (
            text.replace(
                "\n## License Note", f"\n\n{block}\n\n## License Note", 1
            ).rstrip()
            + "\n"
        )

    license_match = re.search(
        r"\nLicense notices for the original repositories are covered by .*\n?\Z", text
    )
    if license_match:
        return (
            text[: license_match.start()].rstrip()
            + f"\n\n{block}\n\n"
            + text[license_match.start() :].lstrip()
        ).rstrip() + "\n"

    return text.rstrip() + f"\n\n{block}\n"


def update_reference_commits(
    readme_path: Path, submodules: list[str], commits: dict[str, str]
) -> None:
    if not readme_path.is_file():
        return

    text = readme_path.read_text(encoding="utf-8")
    selected = referenced_submodules(text, submodules)
    if not selected:
        updated = remove_existing_commit_block(text)
    else:
        updated = with_reference_commit_block(
            text, reference_commit_block(commits, selected)
        )
    readme_path.write_text(updated, encoding="utf-8")


def publish() -> None:
    repo_root, in_progress_dir, skills_dir, lock_file = repo_paths()

    require_dir(in_progress_dir, "in-progress directory")
    require_dir(skills_dir, "skills directory")
    require_file(lock_file, "skill lock file")

    locked_roots = locked_skill_roots(lock_file)
    in_progress_skills = publishable_skills(in_progress_dir)
    if not in_progress_skills:
        fail(f"no publishable skills found under {in_progress_dir}")

    for skill in in_progress_skills:
        if skill in locked_roots:
            fail(f"refusing to overwrite lock-managed skill: skills/{skill}")

    submodules = submodule_paths(repo_root)
    commits = submodule_commits(repo_root, submodules)

    existing_skills = existing_skill_roots(skills_dir)
    removable_skills = [skill for skill in existing_skills if skill not in locked_roots]

    for skill in existing_skills:
        if skill in locked_roots:
            log(f"preserve lock-managed skills/{skill}")
        else:
            log(f"remove unmanaged skills/{skill}")

    run_threaded(removable_skills, lambda skill: shutil.rmtree(skills_dir / skill))

    def publish_skill(skill: str) -> None:
        source = in_progress_dir / skill
        destination = skills_dir / skill
        shutil.copytree(source, destination, symlinks=True, copy_function=shutil.copy2)
        update_reference_commits(destination / "README.md", submodules, commits)

    for skill in in_progress_skills:
        log(f"publish {skill}")

    run_threaded(in_progress_skills, publish_skill)

    log(f"published {len(in_progress_skills)} skill(s)")


if __name__ == "__main__":
    publish()
