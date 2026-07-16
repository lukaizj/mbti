# Trigger Tests — 触发词与激活回归

手工或与 Agent 对话时对照。期望：识别触发 → 加载正确文件 → 声明激活。

## T1 显式类型码

| # | 用户输入 | 期望 |
|---|---------|------|
| T1.1 | `以 INTJ 模式重构 auth` | 激活 INTJ，读 `personas/INTJ.md`，task≈coding/planning |
| T1.2 | `用 enfp 人格写 onboarding` | 大小写归一为 ENFP |
| T1.3 | `/workmode ESTP --task debug` | ESTP + debug adapter |
| T1.4 | `/mbti INTP` | 激活 INTP |

## T2 中文触发

| # | 用户输入 | 期望 |
|---|---------|------|
| T2.1 | `切换人格 ISTJ` | 切到 ISTJ，一句确认 |
| T2.2 | `退出人格模式` | 清除 active_type |
| T2.3 | `人格模式帮我看看这段代码` | 未指定类型 → persona-selection |
| T2.4 | `用守卫者那种稳妥方式改` | 引导 SJ 组（ISTJ/ISFJ/ESTJ/ESFJ） |

## T3 英文触发

| # | 用户输入 | 期望 |
|---|---------|------|
| T3.1 | `persona mode ENTJ` | 激活 ENTJ |
| T3.2 | `work mode: review as INFJ` | INFJ + review |
| T3.3 | `--blend INTJ+ENFP` | blend 规则：行为 INTJ、语气可混 ENFP |

## T4 无效输入

| # | 用户输入 | 期望 |
|---|---------|------|
| T4.1 | `用 XXXX 人格` | 拒绝非法码，列 16 型 |
| T4.2 | `用 I 人格` | 要求完整四字母 |
| T4.3 | `--blend A+B+C` | 拒绝，最多 2 型 |

## T5 Quiz

| # | 用户输入 | 期望 |
|---|---------|------|
| T5.1 | `--quiz` | 四道 E/I S/N T/F J/P 题 |
| T5.2 | Quiz 后用户改选 | 以用户最终选择为准 |

## T6 项目默认

| # | 条件 | 期望 |
|---|------|------|
| T6.1 | 存在 `.persona-workmode` 内容 `INTJ` 且用户未指定 | 默认 INTJ 并告知 |
| T6.2 | 用户显式给了 ENFP | 覆盖文件默认 |
