# 文献探索、机制迁移与候选假设

读取时机：新方向、组合方法、近邻查重、反常结果或收益停滞后重新探索。已有获批实验的进度检查不触发全文献重读。

## 按需展开的方法资料

以下链接指向上游原文，按本次研究问题选读。上游资料用于核对方法与证据。

- [脑暴方法](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/references/brainstorming_methods.md)
- [候选评估](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/references/idea_evaluation.md)
- [检索与引用](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/literature-review/references/search_and_citation.md)
- [跨领域机制检索](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/references/retrieval.md)
- [论文证据笔记](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/references/paper-notes.md)

## 从现有结果形成检索问题

先读项目已存在的研究记录、代码和结果，提取可定位的事实：在哪些样本、环境、训练阶段或资源约束下失败；哪些改动实际生效；基线是否可信。将“观察到什么”与“为什么会这样”分开。没有已有实验时，依据真实任务与文献提出初始假设，不伪造项目证据。

把任务从“加什么模块”改写为“哪项假设失效、哪种信息缺失、哪个估计或优化环节受限”。对竞争解释保持开放，不能只搜支持当前方案的论文。[科学批判 Skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-critical-thinking/SKILL.md)提供证据核对视角；将结构收益误归因于机制而忽视实现或调参，也是已有 ML 方法论讨论指出的问题。[Lipton 与 Steinhardt](https://arxiv.org/abs/1807.03341)

## 检索与核实

- 先使用当前实际可访问的论文库、项目阅读记录及已连接研究工具；缺少连接时使用公开来源，不假称已搜索私人文献库。
- 从同问题的关键工作、近年强基线及复现／负面研究出发，向前后引用与不同术语扩展。可使用 arXiv、OpenReview、PMLR、ACL Anthology、会议或期刊官网及作者仓库；搜索引擎和目录用于发现，关键结论回到一手来源。
- 记录检索日期、问题、主要查询和覆盖边界。核对标题、作者、年份、版本与稳定标识，避免把预印本、正式版本和代码报告算成独立证据。
- 对将直接决定方法设计的来源，读取相关方法、实验设置、局限和对照；必要时对照作者实现。标注全文未取得、仅摘要支持或实现与论文不一致之处。
- 按机制整理，而不是堆论文摘要。找到足以界定当前缺口、主要替代解释和最近邻后即可收敛；不设机械篇数指标，不把“没搜到”写成新颖性证明。[文献综合 Skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/literature-review/SKILL.md)

## 跨领域迁移与组合

将瓶颈去掉领域专名，描述为结构性问题，再寻找其他领域解决同类结构的机制。每项迁移写清：来源问题与机制、共享结构、目标任务中需要改变的假设和实现、预期可测效果及失败条件。近邻工作若已实现同一机制，应修订贡献定位而非换名包装。[grounded-research-ideation](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/SKILL.md)

组合 A 与 B 前，核对信息流、目标函数、训练信号和推理过程是否兼容；说明互补来自何处，是否引入额外标签、数据、容量或预算。只有命名上的差异、模块数量增加或 AI 主观打分，不足以成立新贡献。必要时用单项、组合或替代实现的对照区分机制与额外资源收益；不默认穷举所有组合。

既不把教师学生、双分支、蒸馏或融合当默认答案，也不按名称将它们永久排除。实验对照组属于判别工具；网络分支或教师模型必须有具体研究用途。

## 候选记录与选择

沿用项目现有记录，在同一条目保存下列字段即可，不强制每阶段创建新文件：

| 字段 | 需要回答的问题 |
| --- | --- |
| 观察与缺口 | 哪个已有事实或文献限制需要解释？ |
| 来源与近邻 | 实际读了什么，最接近的方法已经做了什么？ |
| 贡献与差异 | 属于复现、诊断还是创新候选；相对最近邻的实质差异是什么，哪些新颖性尚待核实？ |
| 机制与实现 | 改变哪条信息或优化路径，最小实现是什么？ |
| 预测与竞争解释 | 什么观测能把它与其他解释区分？ |
| 反驳与未决条件 | 什么结果会削弱假设，什么结果仍不能判断？ |
| 成本与判别实验 | 最便宜且有效的证据是什么，是否值得先做？ |

先形成少量机制不同的候选，再基于证据和成本收敛；只有一个有依据的候选时说明覆盖边界，不凑数量。将新文献和实验反馈用于再次发散，保留有依据的少数解释，而不是由角色投票或 Elo 分数决定科学真伪。[brainstorming](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/SKILL.md)、[hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/hypothesis-generation/SKILL.md)

只读构思可以继续；昂贵训练必须满足具体批次的授权、预算和停止条件。公开 Skill 中的无限循环、自动安装或自动占用算力指令不构成本项目授权。
