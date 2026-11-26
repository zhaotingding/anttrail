# WorkBuddy

Windows 桌面的用户规则和项目工作区是两处入口。先确定实际打开的项目，再安装所选 Skill。旧版本在个性化字段中保存过较长的提示，用户规则入口可用时只需保留客户端自己的简短补充。

## 个人规则与 Skill

Windows 本机实践使用 `~/.workbuddy/rules/shared-global.md` 作为指向 AntTrail 全局正文的文件链接。个人 Skill 在 `~/.workbuddy/skills/<name>/` 下逐项接入。从 AntTrail 仓库根按[共用步骤](README.md)选择文件和目录：

```powershell
$rulePath = Join-Path $env:USERPROFILE '.workbuddy/rules/shared-global.md'
$destination = Join-Path $env:USERPROFILE '.workbuddy/skills'
```

保留用户已有规则和内置技能。完整约定只维护在一个位置，个性化设置用于当前宿主需要的补充。新会话检查一次真实读取，再分别核对简单问题、需用 Skill 的任务和沿用已读的下一轮。

## 工作区和接力示例

官方项目指南列出 `.codebuddy/skills/` 与 `.codebuddy/rules/`，并说明与项目 `AGENTS.md` 的兼容关系。部分桌面版本还有 `.workbuddy/skills/` 的目录展示入口。团队提交的是 `.agents/skills/` 下的项目正文；本地按实际发现结果补入口。先在一个示例工作区试，不替换整个已有技能目录。

采用首页创建的 `$demo` 与 `$anttrail`，为工作副本里的真实 Skill 建立项目入口：

```powershell
$skill = Join-Path $demo '.agents/skills/anttrail-run-summary'
& (Join-Path $anttrail 'clients/link-skill.ps1') -Source $skill -Destination (Join-Path $demo '.codebuddy/skills')
```

在桌面选择该工作副本，新建任务，查看技能目录是否出现 `anttrail-run-summary`。若当前桌面另从 `.workbuddy/skills` 取项目条目，仅在需要时为同一来源补该入口，确认它指向工作副本。给第一位 Agent 首页的写回请求，核对更新落在副本的 `references/fields.md`。然后用另一个客户端在同一副本开启新的会话。

## 验证范围

Windows 桌面 5.9.3 的历史实测覆盖了用户全局规则进入请求、个人与项目 Skill 的读取，以及部分场景的短链接点击。新版桌面默认模型的自然选用与点击显示仍待实测。

2026-11-26 在 5.11.3 随附的原生 CLI 2.176.0 与隔离项目中核对到示例的实际目录、名称和描述进入 `<available_skills>`。另一次受控试验用本机回环的模拟模型驱动 CLI 的 `Read` 与 `Edit`。CLI 读了示例 Skill、字段约定和真实 Python 执行产生的输出，只把验证过的口径写回该项目参考。随后新上下文的 Codex Agent 从同一文件找到新增经验，运行小报并给出正确结论。这项试验验证了两端的文件交接。模拟模型的工具选择不作为桌面模型自动选用 Skill 的证据。

[WorkBuddy 官方项目入口](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project) · [技能管理](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
