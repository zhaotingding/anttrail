# AntTrail · 蚁径

**一蚁探路，群蚁成径。** 一个 Agent 把验证过的方法写回项目 Skill，下一个 Agent 从同一个项目接手。每轮回答把采用的 Skill 做成可点击的短链接，你可以随时打开原文。

由 [zhaotingding](https://github.com/zhaotingding) 发起并维护。欢迎在 [Issues](https://github.com/zhaotingding/anttrail/issues) 交流工作方式、提交案例或讨论新的客户端。原创规则和文档采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，原创可执行代码采用 [MIT](LICENSES/MIT.txt)。

## 先看一轮回答

> **本轮读取** · 项目 Skill [运行用时小报](examples/demo-project/.agents/skills/anttrail-run-summary/SKILL.md) · 参考 [字段约定](examples/demo-project/.agents/skills/anttrail-run-summary/references/fields.md)
>
> `dew` 是最快的已完成任务，报表用时为 `0.000 s`。`fern` 为 `1.250 s`。

点开上面的名称就能看到这项判断依据什么。这里使用仓库相对链接演示显示效果。在本地会话中，Agent 用当前客户端能打开的实际文件路径。下一轮如果继续沿用有效正文，链接仍保留，状态写“沿用已读”。

| 状态 | 读者能据此知道什么 |
| --- | --- |
| 拟用 | 已选择来源，正文尚未读取 |
| 本轮读取 | 这一轮成功取得了正文 |
| 沿用已读 | 以前读过，内容仍在当前上下文且有效 |
| 读取失败 | 没有取得本次所需内容，需说明对结论的影响 |

这些是 Agent 对读取情况的说明。想核实一次具体调用，可以查看该客户端的文件读取记录和最终产物。

## 用两个客户端接力

首次可用 `git clone https://github.com/zhaotingding/anttrail.git` 取得本仓库。从检出根运行以下 PowerShell。它将含隐藏技能目录的示例复制到新的临时工作区，使用 Python 3 标准库。两个客户端都打开 **同一个示例工作区**。

```powershell
$anttrail = (Resolve-Path -LiteralPath '.').Path
$demo = Join-Path ([IO.Path]::GetTempPath()) ('anttrail-demo-' + [guid]::NewGuid().ToString('N').Substring(0,8))
Copy-Item -LiteralPath './examples/demo-project' -Destination $demo -Recurse -Force
Set-Location -LiteralPath $demo
$demo
python -B -X utf8 report.py
```

1. 在第一个客户端打开 `$demo`。用 WorkBuddy 时，先按其[项目入口说明](clients/workbuddy.md)把这个副本中的 Skill 接入当前工作区。给 Agent 一个有明确写入范围的请求：
   > 请直接用项目的小报程序核实，已完成但用时为零的任务在结果里怎么处理。把经验证、值得复用的结论记在本项目恰当的位置，方便别人接手。
2. 打开临时副本中的 `.agents/skills/anttrail-run-summary/references/fields.md`。原版记录了字段、状态和单位，验证后的新条目应说明零用时样本的处理，指出可复核的数据和命令。下次遇到相同事实时复用已有条目。这个已获准的本地更新就是“自学习”。
3. 在另一个客户端用**新会话**打开同一份副本，只问：
   > 看一下这个项目的小报，哪项已完成任务最快？
4. 点开第二位 Agent 显示的项目 Skill 和字段约定，核对它读取的是第一位刚更新的文件。用 `python report.py` 对照答案。跨机器协作时，由项目负责人按权限把这次知识更新提交到团队共享的分支，接手方取得同一版本再继续。

复制好示例后即可先体验项目级接力。跨项目采用完整工作约定时，再按下面的入口安装。

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

## 谁能更新什么

- **项目经验**留在项目的 `.agents/skills/`，根 `AGENTS.md` 放稳定约定和简短索引。资料随 Git 交接。每轮按任务读需要的正文与参考。
- **跨项目经验**先成为可审核的提议。列出目标文件、具体改法、依据、影响和验证方式，取得维护者对该方案的明确授权再写入。各客户端原有权限仍生效。
- **多人一起改**时，明确同一文件的编辑责任，写入前读取最新版本。一次提交围绕一个目的。保留有关的已验证事实和用户修改，合并重复条目。客户端之间通过文件与版本交接。

接入新客户端时，在 `clients/` 记录它的规则与技能入口、个人与项目作用域，以及需要的宿主专属设置。在同一示例上分别验证发现、实际读取、写回和新会话接手，再补兼容表。贡献者可通过 [Issues](https://github.com/zhaotingding/anttrail/issues) 附客户端版本、复现步骤和脱敏后的观察结果。

## 署名与交流

复用或改编原创文档时，可用这一行署名，并在改编版中标明实际修改：

> 原作 [AntTrail（蚁径）](https://github.com/zhaotingding/anttrail)，作者 [zhaotingding](https://github.com/zhaotingding)，采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。

许可的适用范围与完整文本见 [LICENSE](LICENSE)。外部论文、厂商手册和其他作者的 Skill 通过来源链接提供，权利与许可按原作品说明。维护本仓库请读[项目约定](AGENTS.md)。
