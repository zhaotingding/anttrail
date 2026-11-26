# 把同一份正文接入客户端

先把 AntTrail 克隆到一个将长期保留的位置，再在客户端适用的目录建立入口。个人目录放跨项目默认偏好，项目根 `AGENTS.md` 和项目 Skill 放团队约定。Skills 的 `name`、`description` 和正文分别负责发现、选用和执行。[Agent Skills 规范](https://agentskills.io/specification)

## Windows 安装一个 Skill

从 AntTrail 根打开 PowerShell，按对应客户端指南设置 `$destination`。先预览，再安装。

```powershell
$anttrail = (Resolve-Path -LiteralPath '.').Path
$destination = Join-Path $env:USERPROFILE '.agents/skills'  # Codex 文档路径，其他客户端见各自指南
$source = Join-Path $anttrail 'skills/html-tutorial'
& ./clients/link-skill.ps1 -Source $source -Destination $destination -WhatIf
& ./clients/link-skill.ps1 -Source $source -Destination $destination
```

工具在目标位置创建一个和技能同名的目录联接。目标已有真实目录或指向另一来源时，它停止并保留原内容。再次安装同一目标会复用已有联接。要装全部六项，在已确认的目标父目录逐项运行：

```powershell
Get-ChildItem -LiteralPath (Join-Path $anttrail 'skills') -Directory | ForEach-Object {
    & (Join-Path $anttrail 'clients/link-skill.ps1') -Source $_.FullName -Destination $destination
}
```

先检查客户端已有的技能列表。同一客户端若同时搜索两个个人入口，只选其中一个放置同名 Skill。需要实体文件时，在使用者选定且无冲突的位置复制完整技能目录。目录联接需要本机文件系统支持，符号链接的权限由系统决定。在其他系统上使用客户端支持的原生路径与链接方式，并在该环境验证。

## 接入全局约定

客户端指南给出全局文件的位置。已有配置时先对照 [AntTrail 正文](../global/AGENTS.md)合并需要的条款，保留使用者自己的补充。空目标可从同一检出创建文件符号链接。下面给出 Windows 写法，先在客户端指南中确定此处的 `$rulePath`：

```powershell
$rulesSource = (Resolve-Path -LiteralPath (Join-Path $anttrail 'global/AGENTS.md')).Path
if (Get-Item -LiteralPath $rulePath -Force -ErrorAction SilentlyContinue) {
    throw "入口已存在，请先核对或手动合并：$rulePath"
}
[IO.Directory]::CreateDirectory((Split-Path -Parent $rulePath)) | Out-Null
New-Item -ItemType SymbolicLink -Path $rulePath -Target $rulesSource
```

一些客户端要求带前置元数据的专属指令文件，按该端指南生成短入口。若客户端只支持内容快照，记录采用的上游版本，下次升级时对照最新内容合并。复制到仓库中的团队规则使用真实文本与项目相对引用。

## 更新、验收和退出

1. 在 AntTrail 检出查看 Git 差异并选定版本；入口跟随该检出的内容。先复核已有自己的修改，再更新或快进。换目录前重新核对链接目标。
2. 在新会话从客户端原生列表找名称与描述，给一个自然任务并观察它是否读取正确正文和参考。检查显示的短链接能否打开对应文件，再检查动作和结果。读到“拟用”只表示将要读取。
3. 移除安装时先用 `Get-Item -LiteralPath <入口> -Force` 核实类型和目标，只移除自己创建的文件链接或目录联接。保留源目录、使用者已有技能和规则。手动合并过的文件只撤回本次加入的段落。
