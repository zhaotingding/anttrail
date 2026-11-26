# GitHub Copilot

先确认使用的是 VS Code 中的哪种会话宿主，还是独立 Copilot CLI。它们可使用同一批项目 Skill，个人指令的发现方式随版本与宿主变化。

## 个人与项目 Skill

当前官方入口包括 `~/.copilot/skills/` 或 `~/.agents/skills/`。若 Codex 和当前 Copilot 都已识别后者，可共用一次安装。项目 `.agents/skills/` 可随 Git 提交，Copilot 也支持 `.github/skills/`。保留一个可发现的同名来源。独立安装到 Copilot 的示例目标如下，命令见[共用步骤](README.md)。

```powershell
$destination = Join-Path $env:USERPROFILE '.copilot/skills'
```

## 规则入口

- 作为团队约定，把项目正文保存在仓库 `AGENTS.md`。也可按团队已有机制使用 `.github/copilot-instructions.md`，就近定位同一份项目知识。
- 已配置的 Windows Copilot 环境验证过 `~/.copilot/copilot-instructions.md` 到共享全局正文的文件链接。按当前宿主的指令目录和诊断结果决定入口。
- 当前 VS Code 的 Copilot harness 支持 `~/.copilot/instructions/*.instructions.md`。较早的 Local 宿主曾使用 VS Code 用户 profile 下的 `instructions/*.instructions.md`。额外目录可能由编辑器转发，独立 CLI 与桌面会话须分别核对。

需要 `applyTo` 包装时，先从 AntTrail 根取得实际全局文件位置，再在当前宿主选定的 `instructions` 目录创建一个短入口。以下是对**新文件**的示例，已有同名文件请手动合并：

```powershell
$rules = (Resolve-Path -LiteralPath './global/AGENTS.md').Path.Replace('\','/')
$instructions = Join-Path $env:USERPROFILE '.copilot/instructions'
$target = Join-Path $instructions 'anttrail.instructions.md'
$lines = @('---','applyTo: "**"','---',"首次使用或全局正文有变更时，读取 [AntTrail 全局约定](<$rules>)。按其约定在回答中链接实际采用的 Skill，并说明读取状态。")
[IO.Directory]::CreateDirectory($instructions) | Out-Null
New-Item -ItemType File -Path $target -Value ($lines -join [Environment]::NewLine) -ErrorAction Stop
```

以用户的实际绝对路径生成短入口。新会话打开示例工作区，检查规则是否进入请求、项目 Skill 是否被实际读取，以及短链接是否可定位。历史 Windows 宿主测试确认过全局注入及部分实际读取，旧会话的缓存和跨轮显示曾有差异。公开版示例可以用[接力步骤](../README.md#用两个客户端接力)在目标版本复核。

[Copilot 官方 Skill 位置](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) · [VS Code 宿主与迁移](https://code.visualstudio.com/docs/agent-customization/migrate-customizations)
