#!/usr/bin/env python3
"""Regression checks for the documented MBTI skill protocol.

The skill executes through prompt instructions rather than a runtime parser. These checks keep
its fixtures and mandatory protocol language from silently drifting apart.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"


def require(text: str, fragment: str, path: Path, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing required protocol text: {fragment!r}")


def main() -> int:
    fixtures = json.loads((TESTS / "protocol-fixtures.json").read_text(encoding="utf-8"))
    skill_path = ROOT / "SKILL.md"
    selection_path = ROOT / "references" / "persona-selection.md"
    contract_path = ROOT / "references" / "behavior-contract.md"
    adapters_path = ROOT / "references" / "task-adapters.md"
    trigger_path = TESTS / "trigger-tests.md"
    behavior_tests_path = TESTS / "behavior-tests.md"

    skill = skill_path.read_text(encoding="utf-8")
    selection = selection_path.read_text(encoding="utf-8")
    contract = contract_path.read_text(encoding="utf-8")
    adapters = adapters_path.read_text(encoding="utf-8")
    triggers = trigger_path.read_text(encoding="utf-8")
    behavior_tests = behavior_tests_path.read_text(encoding="utf-8")
    errors: list[str] = []

    valid_types = fixtures["valid_types"]
    if len(valid_types) != 16 or len(set(valid_types)) != 16:
        errors.append("protocol-fixtures.json: valid_types must list 16 unique MBTI codes")

    quiz = fixtures["quiz"]
    if "".join(quiz["all_answers"]) != quiz["expected_type"]:
        errors.append("protocol-fixtures.json: complete quiz answers must compose expected_type")
    if quiz["expected_type_when_partial"] is not None:
        errors.append("protocol-fixtures.json: partial quiz answers must not infer a type")

    valid_blend = fixtures["blend"]["valid"].split("+")
    if len(valid_blend) != 2 or any(code not in valid_types for code in valid_blend):
        errors.append("protocol-fixtures.json: valid blend must contain two valid types")
    if len(fixtures["blend"]["invalid_too_many"].split("+")) <= 2:
        errors.append("protocol-fixtures.json: invalid_too_many must contain more than two types")
    if all(code in valid_types for code in fixtures["blend"]["invalid_member"].split("+")):
        errors.append("protocol-fixtures.json: invalid_member must contain an invalid type")

    required_skill_fragments = [
        "用户调用 `/mbti`",
        "测试 / 手选 / 不启用",
        "behavior_type",
        "tone_type",
        "explicit_off",
        "adapter** 默认仅作用于当前请求",
        "人格模式**不能扩大工具权限**",
    ]
    for fragment in required_skill_fragments:
        require(skill, fragment, skill_path, errors)

    required_selection_fragments = [
        "快速测试",
        "直接选人格类型",
        "跳过人格模式",
        "默认激活",
        "不臆测缺失维度",
        "退出后本会话不再自动读取该文件",
    ]
    for fragment in required_selection_fragments:
        require(selection, fragment, selection_path, errors)

    for fragment in fixtures["required_rules"].values():
        target = contract if fragment != fixtures["required_rules"]["exit_suppression"] else skill
        require(target, fragment, contract_path if target is contract else skill_path, errors)

    for fragment in ["## ui", "重构", "用户显式 `--task` 总是优先"]:
        require(adapters, fragment, adapters_path, errors)

    for transition in fixtures["state_transitions"]:
        if transition["name"] == "exit clears state and suppresses project default":
            require(contract, "设置本会话 `explicit_off=true`", contract_path, errors)
        if transition["name"] == "single switch clears blend":
            require(skill, "切换为单人格会清除旧 blend", skill_path, errors)
        if transition["name"] == "skip does not use project default":
            require(selection, "不猜测人格、不静默采用项目默认", selection_path, errors)

    for fragment in ["首次启用：测试、手选和跳过", "退出后发送普通任务", "用 ENFP debug 模式"]:
        require(triggers, fragment, trigger_path, errors)

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    for fragment in ["先测你想怎么协作", "快速测试", "随时掌控", "人格不抢方向盘"]:
        require(readme, fragment, readme_path, errors)

    for fragment in ["adapter 优先于人格偏好", "prototype 不冒充交付", "UI adapter 验收"]:
        require(behavior_tests, fragment, behavior_tests_path, errors)

    if errors:
        print("PROTOCOL TEST FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("OK: MBTI protocol fixtures and mandatory rules are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
