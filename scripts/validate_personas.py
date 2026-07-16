#!/usr/bin/env python3
"""Validate mbti persona library."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONAS_DIR = ROOT / "references" / "personas"

REQUIRED_CODES = frozenset(
    {
        "ISTJ",
        "ISFJ",
        "INFJ",
        "INTJ",
        "ISTP",
        "ISFP",
        "INFP",
        "INTP",
        "ESTP",
        "ESFP",
        "ENFP",
        "ENTP",
        "ESTJ",
        "ESFJ",
        "ENFJ",
        "ENTJ",
    }
)

REQUIRED_FRONTMATTER_KEYS = frozenset(
    {
        "code",
        "label_zh",
        "label_en",
        "group",
        "tone_temperature",
        "planning_style",
        "risk_posture",
    }
)

REQUIRED_SECTIONS = [
    "## 一句话",
    "## 核心倾向",
    "## 语气契约",
    "## 工作行为契约",
    "## 任务偏好",
    "## 维度旋钮",
    "## 示例",
    "## 反模式",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KV_RE = re.compile(r"^([a-z_]+):\s*(.+)$", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    data: dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in fm:
            errors.append(f"{path.name}: missing frontmatter key '{key}'")

    code = fm.get("code", path.stem)
    if code != path.stem:
        errors.append(f"{path.name}: code '{code}' != filename stem '{path.stem}'")
    if code not in REQUIRED_CODES:
        errors.append(f"{path.name}: invalid code '{code}'")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section '{section}'")

    if "## 语气契约" in text and "**禁止**" not in text:
        errors.append(f"{path.name}: 语气契约 should include **禁止**")

    if "## 工作行为契约" in text and "**默认顺序**" not in text:
        errors.append(f"{path.name}: 工作行为契约 should include **默认顺序**")

    return errors


def main() -> int:
    if not PERSONAS_DIR.is_dir():
        print(f"ERROR: personas dir not found: {PERSONAS_DIR}", file=sys.stderr)
        return 1

    files = sorted(PERSONAS_DIR.glob("*.md"))
    found = {p.stem for p in files}
    errors: list[str] = []

    missing = REQUIRED_CODES - found
    extra = found - REQUIRED_CODES
    if missing:
        errors.append(f"missing persona files: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected persona files: {sorted(extra)}")

    for path in files:
        errors.extend(validate_file(path))

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: {len(files)} persona files validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
