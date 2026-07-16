# MBTI · 给 AI 换一套「工作人格」

**同一道题，INTJ 先画架构图，ENFP 先抛十个「万一」——你要的是哪种搭档？**

这不是 cosplay，也不是「请你扮演一个温柔助手」。这是一套可安装的 **Agent Skill**：用 MBTI 16 型驱动 **语气（Tone）** 与 **做事方式（Behavior）** 的真实 overlay——该写的测试照样写，该守的安全边界照样守。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lukaizj/mbti?style=social)](https://github.com/lukaizj/mbti)

---

## 一眼看懂 16 型

<p align="center">
  <img src="docs/personas-introvert.png" width="280" alt="内向型八人格" />
  &nbsp;&nbsp;
  <img src="docs/personas-extrovert.png" width="280" alt="外向型八人格" />
</p>

<p align="center">
  <sub>左：内向型 · 深度、结构、内驱　｜　右：外向型 · 连接、节奏、外放</sub><br/>
  <a href="docs/personas-introvert.png">查看大图 · 内向</a>
  ·
  <a href="docs/personas-extrovert.png">查看大图 · 外向</a>
</p>

---

## 同题不同脑：INTJ vs ENFP

**任务：**「帮我把用户登录流程改得更顺一点。」

| | **INTJ 战略架构师** | **ENFP 灵感策划者** |
|---|---------------------|---------------------|
| **开场** | 先界定目标与约束：成功率、风控、可观测性。 | 先问体验：用户卡点在哪、有没有惊喜时刻。 |
| **结构** | 分层方案 → 迁移路径 → 回滚点 → 验收指标。 | 多路径草图 → 快速原型想法 → 再收敛 MVP。 |
| **输出** | 决策表 + 实施顺序 + 明确「不做什么」。 | 故事板式流程 + 2～3 个可 A/B 的变体。 |
| **你会感到** | 冷静、利落、像技术负责人。 | 发散、有画面感、像产品共创伙伴。 |

两种都对——**人格改的是推进节奏与表达方式，不改事实与代码正确性。**

---

## 安装 & 30 秒上手

**Claude Code / Cursor Skills**（推荐路径）：

```bash
git clone https://github.com/lukaizj/mbti.git ~/.claude/skills/mbti
```

若你已有 skills 目录，确保最终路径为 `~/.claude/skills/mbti/`（内含 `SKILL.md`）。

**对话里直接说：**

```
以 INTJ 模式帮我规划 auth 重构
用人格 ENFP 脑暴 onboarding 文案
切换人格 ISTJ
退出人格模式
```

Agent 会读取 `references/personas/{TYPE}.md` 的语气/行为契约，并按任务类型叠加 [task-adapters](references/task-adapters.md)。

---

## 它到底改变了什么？

| 会变的 | 不会变的 |
|--------|----------|
| 回复的节奏、措辞、信息展开顺序 | 代码是否正确、是否可运行 |
| 先收敛还是先发散、先风险还是先体验 | 项目规范、安全策略、测试要求 |
| 协作时的「像谁在陪你干活」 | 工具能力、文件访问、事实核查义务 |

**硬边界：正确性 > 人格。**  
人格是工作风格的 overlay，不是逃避严谨的理由。详见 [behavior-contract.md](references/behavior-contract.md)。

---

## 16 型速查（中文名 · 关键词）

### 内向型 I

| 类型 | 中文名 | 关键词 |
|------|--------|--------|
| ISTJ | 严谨执行者 | 严谨 / 可靠 / 守序 |
| ISFJ | 细致支持者 | 耐心 / 细腻 / 稳定 |
| INFJ | 洞察规划者 | 洞察 / 深度 / 长线 |
| INTJ | 战略架构师 | 战略 / 系统 / 高效 |
| ISTP | 冷静排障者 | 务实 / 冷静 / 机敏 |
| ISFP | 审美体验师 | 柔和 / 审美 / 自然 |
| INFP | 理想创意者 | 真诚 / 创意 / 价值 |
| INTP | 逻辑研究者 | 理性 / 探索 / 建模 |

### 外向型 E

| 类型 | 中文名 | 关键词 |
|------|--------|--------|
| ESTP | 行动实战家 | 果断 / 机动 / 反馈 |
| ESFP | 氛围表达者 | 热情 / 体验 / 感染力 |
| ENFP | 灵感策划者 | 热情 / 发散 / 联想 |
| ENTP | 创新挑战者 | 机智 / 质疑 / 突破 |
| ESTJ | 高效管理者 | 组织 / 标准 / 执行 |
| ESFJ | 协同服务者 | 热心 / 细致 / 协调 |
| ENFJ | 团队引导者 | 鼓舞 / 领导 / 共情 |
| ENTJ | 战略推进者 | 目标 / 决断 / 统筹 |

不确定选谁？见 [persona-selection.md](references/persona-selection.md)（含 quiz / blend）。

---

## 仓库结构（精简版）

```
mbti/
├── SKILL.md                    # Skill 入口与启动清单
├── docs/                       # 视觉物料（海报等）
├── references/
│   ├── behavior-contract.md    # 全局不可违反规则
│   ├── persona-selection.md
│   ├── task-adapters.md
│   └── personas/               # 16 个独立人格定义
├── scripts/                    # 生成与校验
├── tests/                      # 触发词与行为回归
└── agents/openai.yaml
```

维护者：

```bash
python scripts/validate_personas.py
```

---

## 链接

- **仓库：** https://github.com/lukaizj/mbti  
- **许可证：** [MIT](LICENSE)

## 免责声明

MBTI 仅用于 **协作风格模拟**，不用于能力评判、招聘筛选或心理诊断。玩得开心，记得让 Agent 把活干对。

---

*如果你喜欢「同一种工具、不同搭档」—— star 一下，或把海报丢进抖音/GitHub README，让更多人试到自己的那一型。*
