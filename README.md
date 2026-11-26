# AntTrail · 蚁径

**一蚁探路，群蚁成径。** 在获准维护的项目里，Agent 会**为反复出现的任务生成 Skill**，也会**用新证据更新已有 Skill**。下一个 Agent 能从同一项目读到这份经验。每轮回答都用可点击的短链接展示所用 Skill，你可以打开原文。

由 [zhaotingding](https://github.com/zhaotingding) 发起并维护。欢迎在 [Issues](https://github.com/zhaotingding/anttrail/issues) 交流工作方式、提交案例或讨论新的客户端。原创规则和文档采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，原创可执行代码采用 [MIT](LICENSES/MIT.txt)。

## 项目 Skill 如何自生成、自更新

[全局约定](global/AGENTS.md#4-知识维护)规定**何时触发**，[知识维护 Skill](skills/project-knowledge-maintenance/SKILL.md)告诉 Agent **该写到哪里**。在获准执行的项目任务中，Agent 发现可复用的已验证方法、明确的长期约定，或证实旧知识已经失效，就主动核对项目索引、已有 Skill 和原始证据。用户无需为每次沉淀单独下达“创建 Skill”的命令。

| 现场判断 | Agent 的动作 | 下次接手能看到什么 |
| --- | --- | --- |
| **自生成**。这类任务会独立触发，已有 Skill 都承接不了 | 创建 `.agents/skills/<name>/SKILL.md`，用 `name` 和 `description` 声明名称与触发条件，正文写流程、适用边界和证据入口。项目根 `AGENTS.md` 增加一行索引 | 团队多了一项可以按任务选用的技能 |
| **自更新**。新证据补充或纠正了已有 Skill | 读最新版本，把变化合并进原条款或其 `references/`。触发范围或路径变了才同步调整索引 | 同一项技能给出更新后的做法，能够追溯变更依据 |
| 已有等价知识，或只是一次临时现象 | 等价条目直接复用。单次运行状态留在任务记录，尚无依据的解释保留为待验证 | 技能目录仍按任务组织，不随对话轮数增长 |

项目 Skill 正文以 3000 字符为上限（不含 YAML 元数据）。预计超限时先合并重复条款，再把条件性细节移入参考。多人维护同一文件时先明确编辑责任，写入前核对最新版本。

**项目可以主动写回，全局由使用者批准。** 只读分析阶段可以提出候选条目。进入已批准的项目执行阶段后，Agent 可主动维护项目知识。发现跨项目可复用的经验或通用 Skill 的问题时，Agent 可以提议更新个人通用 Skill 或全局约定，说明目标文件、具体改法、依据、影响和验证方式，取得明确授权后才写入。

## 先看一轮回答

> **本轮读取** · 项目 Skill [运行用时小报](examples/demo-project/.agents/skills/anttrail-run-summary/SKILL.md) · 参考 [字段约定](examples/demo-project/.agents/skills/anttrail-run-summary/references/fields.md)
>
> `dew` 是最快的已完成任务，报表用时为 `0.000 s`。`fern` 为 `1.250 s`。

这段回答使用[仓库自带的原始样本](examples/demo-project/runs.csv)。点开上面的名称就能查看判断依据。这里使用仓库相对链接演示显示效果。在本地会话中，Agent 用当前客户端能打开的实际文件路径。下一轮如果继续沿用有效正文，链接仍保留，状态写“沿用已读”。

| 状态 | 读者能据此知道什么 |
| --- | --- |
| 拟用 | 已选择来源，正文尚未读取 |
| 本轮读取 | 这一轮成功取得了正文 |
| 沿用已读 | 以前读过，内容仍在当前上下文且有效 |
| 读取失败 | 没有取得本次所需内容，需说明对结论的影响 |

这些是 Agent 对读取情况的说明。想核实一次具体调用，可以查看该客户端的文件读取记录和最终产物。

## 用两个客户端接力

**从零体验。** 首次可用 `git clone https://github.com/zhaotingding/anttrail.git` 取得本仓库。按[客户端指南](#接入你的客户端)接入全局约定，安装 `project-knowledge-maintenance` 和 `code-development`，维护项目索引时会用到后者的协作参考。从仓库根运行下面的 PowerShell。这里只复制程序、虚构数据和许可，工作副本起初没有项目 Skill 或索引。若想先看一份成形的 Skill，可打开[仓库自带的示例项目](examples/demo-project/)作对照。

```powershell
$anttrail = (Resolve-Path -LiteralPath '.').Path
$sample = Join-Path $anttrail 'examples/demo-project'
$demo = Join-Path ([IO.Path]::GetTempPath()) ('anttrail-demo-' + [guid]::NewGuid().ToString('N').Substring(0,8))
[void](New-Item -ItemType Directory -Path $demo)
foreach ($file in 'report.py','runs.csv','LICENSE') {
    Copy-Item -LiteralPath (Join-Path $sample $file) -Destination $demo
}
Set-Location -LiteralPath $demo
$demo
python -B -X utf8 report.py
```

**第一轮 · 看 Skill 生成。** 在第一个客户端打开 `$demo`，给它一项会反复用到的业务任务，并授权在本项目里记录结果。

> 以后每周由不同同事复核这份小报。请直接运行样例，核实哪些任务会入选、毫秒怎样换算成展示值。把可复核的做法留在本项目，方便下周接手。

查看新出现的 `.agents/skills/` 与根 `AGENTS.md`。索引应能点到实际生成的 Skill，其描述应说清何时使用，正文或参考应能定位验证程序和样例。名称由 Agent 按任务确定。如果只收到口头总结，先核对客户端是否读到维护 Skill、是否已获得本次项目写入权限。

**第二轮 · 看同一项 Skill 更新。** 在刚才的 PowerShell 中给临时副本添加一条并列样本，运行一次即可。

```powershell
Add-Content -LiteralPath (Join-Path $demo 'runs.csv') -Value 'ash,done,0' -Encoding ascii
```

> 团队以后回答“谁最快”时，要把全部并列任务按任务名升序列出。请用新样例核实，并把这条约定留给后续同事。本次可直接更新项目知识。

打开第一轮生成的 Skill 或其参考，查看新增的并列口径和依据。一次 Codex 隔离实测中，项目 Skill 数量为 **0 → 1 → 1**。第一轮生成 `weekly-report-review`，第二轮更新它的正文和索引。程序仍按输入顺序列出 `dew` 再列 `ash`，回答时的排序来自团队新约定。

**第三轮 · 换一个 Agent 接手。** 在另一客户端用新会话打开**同一个工作副本**。若需为 [WorkBuddy 建立项目入口](clients/workbuddy.md)，用第一轮索引里的实际技能目录替换指南中的样例目录名。跨机器时，先按项目授权提交并取得同一版本。让新会话回答这个业务问题。

> 这次小报里最快的已完成任务是哪些？

在上述实测中，独立的新会话读取了更新后的项目 Skill，按 `ash`、`dew` 的顺序列出两项，均为 `0.000 s`。在你的客户端试用时，点开回答里的 Skill 来源，核对它指向刚更新的项目知识。这样既能检查结论，也能看见经验从哪里传到了下一位 Agent。

## 接入你的客户端

从 [global/AGENTS.md](global/AGENTS.md) 选用全局工作约定。已有个人规则时合并所需条款。公开仓库 `skills/` 是素材目录，选用的技能以整个目录为单位接入，个人主机表和凭据留在各自环境。Windows 可用[联接工具](clients/link-skill.ps1)把多端入口指向一次检出的技能。团队项目应提交实际的项目约定、Skill 和参考文件，让协作者克隆后也能读取。

| 客户端 | 入门与验证范围 |
| --- | --- |
| [Codex](clients/codex.md) | 个人与项目两种方式。原生目录与指令输入已有本机检查 |
| [WorkBuddy](clients/workbuddy.md) | 项目入口已核对。随附 CLI 在回环模拟模型下完成真实文件读写并交给新 Codex Agent。桌面默认模型的本版验收待补 |
| [GitHub Copilot](clients/copilot.md) | VS Code 与 CLI 按当前宿主接入，项目知识共用同一份正文 |
| [Google Antigravity](clients/antigravity.md) | 已核对官方规则与技能路径，等待本机公开版实测 |

完整使用时将六个目录置于同一 Skill 父目录。单独选用时，从下表判断需要哪些配合项。全局约定的知识写回使用 `project-knowledge-maintenance`，涉及开发协作基线时还要能读取 `code-development` 的协作参考。

| Skill | 适用任务 | 可以这样试 |
| --- | --- | --- |
| [code-development](skills/code-development/SKILL.md) | 实现、修复、代码审查、桌面交付与 Git 协作 | “看看这个重试分支会被哪种实际输入触发。” |
| [html-tutorial](skills/html-tutorial/SKILL.md) | 高密度学习型 HTML、数据解读、真实截图编号导览 | “用我的截图做一个编号可点的界面导览。” |
| [llm-api-integration](skills/llm-api-integration/SKILL.md) | 为程序接入模型 API、费用边界、模型结果恢复 | “摘要已经生成但导出失败，怎么从已有结果恢复？” |
| [server-cluster](skills/server-cluster/SKILL.md) | SSH 接入、主机身份、磁盘、解释器与工作区定位 | “根据这段脱敏的错误定位连接失败在哪一步。” |
| [server-training](skills/server-training/SKILL.md) | 文献驱动的方法设计、对照、训练运行与方向判断 | “结合现有负结果，找两个能区分下一步方向的实验。” |
| [project-knowledge-maintenance](skills/project-knowledge-maintenance/SKILL.md) | 沉淀已验证项目经验、整理索引与受控的跨项目推广 | “把这次验证过的恢复方法补进现有项目 Skill。” |

接入新客户端时，在 `clients/` 记录它的规则与技能入口、个人与项目作用域，以及需要的宿主专属设置。在同一示例上分别验证发现、实际读取、写回和新会话接手，再补兼容表。贡献者可通过 [Issues](https://github.com/zhaotingding/anttrail/issues) 附客户端版本、复现步骤和脱敏后的观察结果。

## 署名与交流

复用或改编原创文档时，可用这一行署名，并在改编版中标明实际修改：

> 原作 [AntTrail（蚁径）](https://github.com/zhaotingding/anttrail)，作者 [zhaotingding](https://github.com/zhaotingding)，采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。

许可的适用范围与完整文本见 [LICENSE](LICENSE)。外部论文、厂商手册和其他作者的 Skill 通过来源链接提供，权利与许可按原作品说明。维护本仓库请读[项目约定](AGENTS.md)。
