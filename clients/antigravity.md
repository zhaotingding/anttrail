# Google Antigravity

**接入状态为官方文档已核对，公开版尚待本机实测。** 首次验证时记录 App、IDE 或 CLI、版本、操作系统和所选模型。订阅档位可作为实测环境的一项说明。

## 安装位置

| 作用域 | 一种官方规则入口 | Skill 目录 |
| --- | --- | --- |
| 个人 | `~/.gemini/AGENTS.md` | `~/.gemini/config/skills/<name>/` |
| 工作区 | 项目根 `AGENTS.md` | `.agents/skills/<name>/` |

Google 也支持其他全局规则位置，已有 `GEMINI.md` 或已有规则时先查当前实际加载的文件，合并选中的约定。上表给出一个最短路径；App、IDE 和 CLI 的附加兼容位置按当前版本查询。

Windows 下可按[共用步骤](README.md)接入一个 Skill，先检查实际目录能否识别链接；需要实体目录时复制完整技能包。`$rulePath` 仅在该入口空闲且打算使用共享规则时用于创建文件链接。

```powershell
$rulePath = Join-Path $env:USERPROFILE '.gemini/AGENTS.md'
$destination = Join-Path $env:USERPROFILE '.gemini/config/skills'
```

## 首次实机验收

1. 打开用时小报工作副本，确认全局与项目规则可读，示例 Skill 出现在原生列表中。
2. 在新会话给出首页的自然问题，查看实际选择、读取和链接。点击 Skill 名称，再打开字段参考，核对目标确属同一份项目知识。
3. 对已批准的项目经验运行写回演练，然后用另一客户端检查它。若使用原生 `/learn`，核对提议的文本、目的地与作用域后再批准。跨项目规则的更新仍需具体授权。
4. 只将实际走通的层级记入兼容记录，如实留下入口、版本、链接显示或选用方面的差异。

[官方规则路径](https://antigravity.google/docs/rules/) · [官方技能路径](https://antigravity.google/docs/skills/) · [学习提议流程](https://antigravity.google/docs/commands/learn/)
