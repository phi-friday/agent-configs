#!/usr/bin/env python3
"""Classify whether a raw user request enables github-pr-review YOLO mode."""

from __future__ import annotations

import argparse
import json
import sys
from typing import NamedTuple


class _Classification(NamedTuple):
    is_yolo: bool
    first_word: str | None
    reason: str


_SELF_TEST_CASES = (
    ("yolo", True),
    ("yolo review PR #123", True),
    ("yolo #123 리뷰하고 올려", True),
    ("review PR #123", False),
    ("draft부터 submit까지 한번에 진행", False),
    ("사용자 검수 없이 제출", False),
    ("auto submit all findings", False),
    ("yolox", False),
    ("yolomode", False),
    ("yolo모드로 진행", False),
    ("yolo, review PR #123", False),
    ("YOLO", False),
    ("XXX yolo", False),
    ("", False),
)


def _first_word(text: str) -> str | None:
    words = text.split(maxsplit=1)
    if not words:
        return None
    return words[0]


def _classify(text: str) -> _Classification:
    first_word = _first_word(text)

    if first_word == "yolo":
        return _Classification(
            is_yolo=True, first_word=first_word, reason="first word is exact yolo"
        )

    if first_word is None:
        return _Classification(is_yolo=False, first_word=None, reason="input is empty")

    if first_word.lower() == "yolo":
        return _Classification(
            is_yolo=False,
            first_word=first_word,
            reason="first word is not exact lowercase yolo",
        )

    if "yolo" in text:
        return _Classification(
            is_yolo=False,
            first_word=first_word,
            reason="yolo appears but is not the exact first word",
        )

    return _Classification(
        is_yolo=False, first_word=first_word, reason="first word is not yolo"
    )


def _emit_result(classification: _Classification) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "is_yolo": classification.is_yolo,
                "first_word": classification.first_word,
                "reason": classification.reason,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    sys.stdout.write("\n")


def _raw_input_from_args(text_parts: list[str]) -> str:
    if text_parts:
        return " ".join(text_parts)
    return sys.stdin.read()


def _run_self_test() -> int:
    failures: list[str] = []

    for raw_text, expected in _SELF_TEST_CASES:
        actual = _classify(raw_text).is_yolo
        if actual != expected:
            failures.append(f"{raw_text!r}: expected {expected}, got {actual}")

    if failures:
        for failure in failures:
            sys.stderr.write(f"self-test failed: {failure}\n")
        return 1

    sys.stdout.write("ok: detect_yolo_mode self-test passed\n")
    return 0


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Return whether raw user input enables github-pr-review YOLO mode."
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Run built-in classifier examples."
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Raw user input. Use -- before text that may start with a dash.",
    )
    return parser.parse_args(argv)


def _main(argv: list[str]) -> int:
    args = _parse_args(argv)

    if args.self_test:
        return _run_self_test()

    raw_text = _raw_input_from_args(args.text)
    classification = _classify(raw_text)
    _emit_result(classification)
    return 0 if classification.is_yolo else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
