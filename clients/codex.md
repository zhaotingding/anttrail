# Codex

## 放到哪里

| 作用域 | 规则 | Skill 父目录 |
| --- | --- | --- |
| 个人 | Codex home 下的 `AGENTS.md`。默认 `~/.codex/AGENTS.md`，自定义 `CODEX_HOME` 时使用该位置 | 当前官方指南列出 `~/.agents/skills/` |
| 项目 | 项目根 `AGENTS.md`，有子目录约定时按实际 cwd 加载 | 项目 `.agents/skills/` |

先查看当前配置中的 `AGENTS.override.md` 和 Skill 目录，选一个有效位置。Windows 安装方法见[共用步骤](README.md)。个人规则示例：

```powershell
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$rulePath = Join-Path $codexRoot 'AGENTS.md'
$destination = Join-Path $env:USERPROFILE '.agents/skills'
```

Windows 上有版本也会从 `CODEX_HOME/skills` 发现个人技能。若你的工作配置已经采用该位置，可沿用它。先验证一个来源，再接入其他 Skill。

## 在项目中验证

打开[用时小报](../examples/demo-project/)的工作副本。新会话中给出 README 的小报问题。若使用 CLI，可在该工作目录运行 `codex debug prompt-input`（支持此诊断的版本），只检查示例 Skill 的名称、描述、路径和项目约定。诊断输出可能包含其他个人指令，应在本地查看。真实选用与回答另从文件读取记录和小报实测判断。

本版在 Windows 的 Codex CLI `0.171.0-alpha.13.2` 用隔离配置实测。把六个公开 Skill 联接到临时 `CODEX_HOME/skills` 后，六个条目的描述与真实目标、示例项目 Skill、全局和项目规则正文都进入原生输入。只在临时用户目录的 `.agents/skills` 放置联接时，该隔离试验只列出了项目 Skill。不同 Windows 用户目录解析与版本按使用者当前客户端复核。

[官方全局与项目规则](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [官方本地 Skill 发现位置](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
