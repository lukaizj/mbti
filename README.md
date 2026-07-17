# MBTI · 给 AI 换一套「工作人格」

> 同一个 Agent，16 种推进方式。
> **先测你想怎么协作，再给 AI 一种恰到好处的工作风格。**

不是心理诊断，不是 cosplay。它只改变协作的节奏、视角和表达；**代码质量、安全边界与验证要求永远不变。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 亮点

- **先选再干活**：`/mbti` 首次启用时，4 题快速测试你的协作偏好，推荐结果自动生效。
- **随时掌控**：不想测试？直接手选 16 型；想安静？跳过；想换脑子？一句话切换。
- **人格不抢方向盘**：debug、review、coding 保留必要工程流程；人格只让每一步更像你喜欢的搭档。
- **可验证，不玄学**：人格定义可生成校验，关键选择/退出/适配器规则有回归检查。

## 30 秒上手

```text
/mbti
```

```text
1. 快速测试：4 题后推荐并默认启用
2. 直接选择：输入 INTJ / ENFP / …
3. 跳过：中性专业模式，直接开工
```

也可以直达：

```text
以 INTJ 模式规划 auth 重构
用 ENFP 人格脑暴 onboarding
切换人格 ISTJ
退出人格模式
```

测试只问「你希望怎么协作」，**不定义你是谁**。启用后随时能切换或退出。

## 它会改变什么？

| 会变 | 不会变 |
|---|---|
| 表达节奏、信息密度、先发散还是先收敛 | 事实、测试、项目规范与安全要求 |
| 规划和沟通的协作感 | 高影响操作仍需你的明确授权 |

例如：ENFP 可以让脑暴更有火花；但遇到线上 bug，仍然必须**复现 → 缩小范围 → 验证 → 修复**。

## 安装

```bash
git clone https://github.com/lukaizj/mbti.git ~/.claude/skills/mbti
```

确保目录中包含 `SKILL.md`。详细人格、任务适配器和行为边界见：
[persona-selection](references/persona-selection.md) ·
[task-adapters](references/task-adapters.md) ·
[behavior-contract](references/behavior-contract.md)

## 维护

```bash
python scripts/generate_personas.py --check
python scripts/validate_personas.py
python tests/test_protocol.py
```

MBTI 仅用于协作风格模拟，不用于能力评判、招聘筛选或心理诊断。
