#!/usr/bin/env python3
"""Validate the MBTI persona library and generated-document consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from generate_personas import PERSONAS, render

ROOT = Path(__file__).resolve().parent.parent
PERSONAS_DIR = ROOT / "references" / "personas"
README = ROOT / "README.md"

CANONICAL_PERSONAS = {persona["code"]: persona for persona in PERSONAS}
REQUIRED_CODES = frozenset(CANONICAL_PERSONAS)
VALID_GROUPS = frozenset({"NT", "NF", "SJ", "SP"})

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


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)

    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in frontmatter:
            errors.append(f"{path.name}: missing frontmatter key '{key}'")

    code = frontmatter.get("code", path.stem)
    if code != path.stem:
        errors.append(f"{path.name}: code '{code}' != filename stem '{path.stem}'")
    if code not in REQUIRED_CODES:
        errors.append(f"{path.name}: invalid code '{code}'")
        return errors

    expected = CANONICAL_PERSONAS[code]
    if frontmatter.get("group") not in VALID_GROUPS:
        errors.append(f"{path.name}: invalid group '{frontmatter.get('group')}'")
    elif frontmatter.get("group") != expected["group"]:
        errors.append(
            f"{path.name}: group '{frontmatter.get('group')}' != canonical '{expected['group']}'"
        )

    for label_key in ("label_zh", "label_en"):
        if frontmatter.get(label_key) != expected[label_key]:
            errors.append(
                f"{path.name}: {label_key} '{frontmatter.get(label_key)}' "
                f"!= canonical '{expected[label_key]}'"
            )

    if text != render(expected):
        errors.append(f"{path.name}: differs from scripts/generate_personas.py")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section '{section}'")

    if "## 语气契约" in text and "**禁止**" not in text:
        errors.append(f"{path.name}: 语气契约 should include **禁止**")
    if "## 工作行为契约" in text and "**默认顺序**" not in text:
        errors.append(f"{path.name}: 工作行为契约 should include **默认顺序**")

    return errors


def validate_readme() -> list[str]:
    if not README.exists():
        return ["README.md: missing"]

    text = README.read_text(encoding="utf-8")
    if "## 16 型速查" not in text:
        return []

    errors: list[str] = []
    for code, persona in CANONICAL_PERSONAS.items():
        expected_row = f"| {code} | {persona['label_zh']} |"
        if expected_row not in text:
            errors.append(f"README.md: missing canonical row '{expected_row}'")
    return errors


def main() -> int:
    if not PERSONAS_DIR.is_dir():
        print(f"ERROR: personas dir not found: {PERSONAS_DIR}", file=sys.stderr)
        return 1

    files = sorted(PERSONAS_DIR.glob("*.md"))
    found = {path.stem for path in files}
    errors: list[str] = []

    missing = REQUIRED_CODES - found
    extra = found - REQUIRED_CODES
    if missing:
        errors.append(f"missing persona files: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected persona files: {sorted(extra)}")

    for path in files:
        errors.extend(validate_file(path))
    errors.extend(validate_readme())

    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(files)} persona files and README labels validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
