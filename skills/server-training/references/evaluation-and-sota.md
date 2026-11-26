# 公平评估、领域差异与 SOTA 声明

读取时机：复现与选模、分析效果、比较方法、准备主要研究结论。最新 SOTA 在做比较时重新查证，不把本文件的历史检索日期当作实时排名。

## 按需展开的方法资料

以下链接指向上游原文，按本次研究问题选读。上游资料用于核对方法与证据。

- [统计陷阱](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-critical-thinking/references/statistical_pitfalls.md)

## 比较合同

固定任务、数据版本与划分、样本独立单位、允许的数据和预训练资源、指标实现与方向、训练／搜索／推理预算、checkpoint 选择及测试次数。论文值、作者代码复现值和本项目复现值分别标明，不能混成同一基线。

验证集用于开发和选择，最终测试用于确认；需要测试时调参、在线适应或转导的研究，必须事先声明其协议并公平应用到比较方法。测试集已被反复用于选方法时，不能继续把它称为独立确认集。

基线应足够强且合理调优。报告搜索机会与总成本，包括失败和探索运行；不给新方法大量搜索、却拿未调优基线直接比较。[Dodge 等](https://aclanthology.org/D19-1224/)

## 领域分支

| 任务 | 必须核对的差异 |
| --- | --- |
| 深度学习、CV／NLP | 数据与标签泄漏、预训练数据、增强、模型容量、训练步数、评测 mode、阈值与 checkpoint 选择；按视频／主体等真实独立单位划分，不把近重复片段当独立数据 |
| 传统 ML、表格与时序 | 预处理和特征选择只在训练折拟合；分组和时间边界符合问题；需要估计选模后泛化时使用合适的外层评估，而非把内层最佳 CV 分数当最终性能 |
| 强化学习 | 环境版本、wrapper、奖励、终止／截断与 bootstrap、评估归一化、评估策略、episode 定义；同时比较环境交互量与计算预算 |
| LLM 强化学习／后训练 | 独立核对 reward/parser 与真实正确率；检查生成样本、格式奖励、长度、奖励分布及参考策略偏离；单一 loss 或 reward 曲线不能代表能力提升 |

传统 ML 的 Pipeline 与内外层隔离遵循实际数据独立性，而不是默认随机打散所有样本。[scikit-learn 数据泄漏指南](https://scikit-learn.org/1.9/common_pitfalls.html)、[嵌套交叉验证](https://scikit-learn.org/1.9/auto_examples/model_selection/plot_nested_cross_validation_iris.html)

RL 的训练与评估环境应分开；恢复模型时核对归一化统计、replay 与采样状态。环境检查器只能检查部分接口约定，不能证明奖励正确或问题可学。更多 episode 不等于更多独立训练重复。[SB3 评估建议](https://stable-baselines3.readthedocs.io/en/v2.9.2/guide/rl_tips.html)、[Henderson 等](https://arxiv.org/html/1709.06560v3)

GRPO 的关键区别之一是省去独立 critic/value model，不是普遍省去 reward model。不同目标中的 loss 与 KL 不能混为一谈，奖励组内标准差为零还可能来自全对或全错。[DeepSeekMath](https://arxiv.org/html/2402.03300v3)、[TRL GRPO 文档](https://huggingface.co/docs/trl/v1.17.1/en/grpo_trainer)

## 效应与不确定性

- 先说明独立重复单位和比较是否配对。样本、episode、frame、fold 与训练 seed 不能任意互换，避免伪重复。
- 报告实际效应与不确定性，说明误差条代表什么。根据指标、层级和重复数选择区间或检验，不机械对所有任务用同一统计方法。
- 跨 RL 任务汇总时可考虑性能分布、稳健汇总和分层区间；单个点估计可能使排序不稳定，不凭一次最好成绩下结论。[Agarwal 等与 rliable](https://github.com/google-research/rliable)
- 探索中尝试了很多候选时，报告选择过程，保留独立确认；事后挑选的子集提升只作为探索发现。预算不足以可靠估计时直接说明，不能把小样本不显著当作等效。

## 什么时候可以说超过 SOTA

1. 在当前检索日期明确基准与协议，实际核对最接近的强结果和资源条件，列明可比与不可比差异。
2. 本方法和强基线均有可信实现与选择过程；收益不只是额外数据、预训练、容量或搜索预算未披露造成的优势。
3. 主要结果与独立确认、效应不确定性和必要机制对照相符；同时报告失败、成本和适用限制。
4. 比较只覆盖一项任务或某个资源约束时，将声明限定在该范围。条件不满足时用“本协议下优于所复现基线”“存在初步增益”或“证据尚不足”，不将研究目标写成已实现结果。

可复现报告应足以理解主要实验、选择过程、不确定性及计算资源；不同场景允许说明未完成项，而不是伪造齐全。[NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist)
