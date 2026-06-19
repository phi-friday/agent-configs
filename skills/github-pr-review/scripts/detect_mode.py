#!/usr/bin/env python3
"""Detect explicit github-pr-review mode keywords in raw user input."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Final, Literal, NamedTuple

Mode = Literal["draft", "submit", "yolo"]
Separator = Literal["comma", "word"]

_MODE_KEYWORDS: Final[tuple[Mode, ...]] = ("draft", "submit", "yolo")


class _Classification(NamedTuple):
    mode: Mode | None
    keyword: str | None
    separator: Separator | None
    first_word: str | None
    reason: str


def _first_word(text: str) -> str | None:
    start = 0
    text_length = len(text)
    while start < text_length and text[start].isspace():
        start += 1

    if start == text_length:
        return None

    end = start + 1
    while end < text_length and not text[end].isspace():
        end += 1

    return text[start:end]


def _separator(first_word: str, keyword: Mode) -> Separator | None:
    if first_word == keyword:
        return "word"

    if first_word == f"{keyword},":
        return "comma"

    return None


def _classify(text: str) -> _Classification:
    first_word = _first_word(text)

    if first_word is None:
        return _Classification(
            mode=None,
            keyword=None,
            separator=None,
            first_word=None,
            reason="input is empty",
        )

    for keyword in _MODE_KEYWORDS:
        separator = _separator(first_word, keyword)
        if separator is not None:
            return _Classification(
                mode=keyword,
                keyword=keyword,
                separator=separator,
                first_word=first_word,
                reason=f"first word is explicit {keyword}",
            )

    lowered_first_word = first_word.lower()
    for keyword in _MODE_KEYWORDS:
        if lowered_first_word == keyword:
            return _Classification(
                mode=None,
                keyword=None,
                separator=None,
                first_word=first_word,
                reason=f"first word is not exact lowercase {keyword}",
            )

        if lowered_first_word == f"{keyword},":
            return _Classification(
                mode=None,
                keyword=None,
                separator=None,
                first_word=first_word,
                reason=f"first word is not exact lowercase {keyword}",
            )

        if first_word.startswith(keyword):
            return _Classification(
                mode=None,
                keyword=None,
                separator=None,
                first_word=first_word,
                reason=f"first word has unsupported suffix after {keyword}",
            )

    return _Classification(
        mode=None,
        keyword=None,
        separator=None,
        first_word=first_word,
        reason="no explicit mode keyword at start",
    )


def _emit_result(classification: _Classification) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "explicit": classification.mode is not None,
                "first_word": classification.first_word,
                "keyword": classification.keyword,
                "mode": classification.mode,
                "reason": classification.reason,
                "separator": classification.separator,
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


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Return the explicit github-pr-review mode keyword in raw user input."
        )
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Raw user input. Use -- before text that may start with a dash.",
    )
    return parser.parse_args(argv)


def _main(argv: list[str]) -> int:
    args = _parse_args(argv)
    raw_text = _raw_input_from_args(args.text)
    classification = _classify(raw_text)
    _emit_result(classification)
    return 0 if classification.mode is not None else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
