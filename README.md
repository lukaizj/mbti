# MBTI

以 MBTI 16 型人格驱动 AI Agent 的**语气**与**工作行为**——不是角色扮演，而是可验证的工作模式 overlay。

## 快速开始

```
以 INTJ 模式帮我规划 auth 重构
用人格 ENFP 脑暴 onboarding
切换人格 ISTJ
退出人格模式
```

Agent 会加载 `references/personas/{TYPE}.md` 中的语气契约与行为契约，并按任务叠加 [task-adapters](references/task-adapters.md)。

## 目录结构

```
mbti/
├── SKILL.md                 # Agent 入口与启动清单
├── references/
│   ├── behavior-contract.md # 全局不可违反规则
│   ├── persona-selection.md # 选择、quiz、blend
│   ├── task-adapters.md     # coding / review / docs / ...
│   └── personas/            # 16 个独立人格定义
├── scripts/
│   ├── generate_personas.py # 从内嵌数据再生 personas/
│   └── validate_personas.py # CI 校验人格库完整性
├── tests/                   # 触发词与行为回归用例
└── agents/openai.yaml       # OpenAI 兼容 agent 接口
```

## 设计原则

1. **双轨**：Tone（用户可见）+ Behavior（任务怎么推进）
2. **overlay**：人格不牺牲正确性、安全、项目规范
3. **模块化**：每人格一文件，便于单独迭代
4. **可测**：`validate_personas.py` + `tests/` 回归

## 维护

```bash
# 校验 16 型文件是否齐全、结构是否正确
python scripts/validate_personas.py

# 修改 scripts/generate_personas.py 后重新生成
python scripts/generate_personas.py
python scripts/validate_personas.py
```

## 16 型索引

| 组 | 类型 |
|----|------|
| NT | INTJ INTP ENTJ ENTP |
| NF | INFJ INFP ENFJ ENFP |
| SJ | ISTJ ISFJ ESTJ ESFJ |
| SP | ISTP ISFP ESTP ESFP |

## 免责声明

MBTI 仅作**协作风格模拟**，不用于能力评判、招聘或心理诊断。
