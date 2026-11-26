# 上游来源索引

AntTrail 的方法参考随仓库提供。下表保留原作者与上游入口，GitHub 来源优先链接到初次整理时的固定提交。网页和依赖版本可变化，涉及新论文、模型或评测排名时核对当前资料。

把上游文章和 Skill 当作研究材料阅读。原文中的角色分派、安装命令和自动执行建议只描述其自身工作流。执行任何操作仍以当前项目、用户授权和预算为准。

| 原作者／上游材料 | 用途 | 对应版本 |
| --- | --- | --- |
| [K-Dense scientific-brainstorming](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/SKILL.md) · K-Dense-AI | 不同机制候选、发散与收敛、负结果的信息价值 | commit 2d2065fb4520 |
| [K-Dense hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/hypothesis-generation/SKILL.md) · K-Dense-AI | 竞争解释、可测预测、反驳与未决条件 | commit 2d2065fb4520 |
| [K-Dense scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-critical-thinking/SKILL.md) · K-Dense-AI | 原始证据、混杂、选择偏差与不确定性 | commit 2d2065fb4520 |
| [K-Dense literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/literature-review/SKILL.md) · K-Dense-AI | 可追溯检索、原文核对、按机制综合 | commit 2d2065fb4520 |
| [K-Dense Stable Baselines3](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/stable-baselines3/SKILL.md) · K-Dense-AI | 训练与评估分离、归一化和恢复状态 | commit 2d2065fb4520 |
| [K-Dense scikit-learn](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scikit-learn/SKILL.md) · K-Dense-AI | Pipeline、分组或时间划分、选模与评估隔离 | commit 2d2065fb4520 |
| [Hopotta grounded-research-ideation](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/SKILL.md) · Hopotta | 机制缺口、结构类比、跨领域适配、低成本证伪 | commit 7670b2509044 |
| [EvoScientist research-ideation](https://github.com/EvoScientist/EvoSkills/blob/4889c2270af5f9a7658bb6a6709bf37040902006/skills/research-ideation/SKILL.md) · EvoScientist | 历史方向、挑战—机制映射和失败反馈 | commit 4889c2270af5 |
| [Orchestra autoresearch](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/0-autoresearch-skill/SKILL.md) · Orchestra-Research | 实验内层与研究综合外层，深化／拓展／转向 | commit 773a52944ba4 |
| [Orchestra GRPO](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/06-post-training/grpo-rl-training/SKILL.md) · Orchestra-Research | reward/parser、生成样本和奖励分布的核对思路 | commit 773a52944ba4 |
| [Orchestra W&B](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/13-mlops/weights-and-biases/SKILL.md) · Orchestra-Research | run、配置、数据与模型的关联 | commit 773a52944ba4 |
| [Orchestra Lightning](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/08-distributed-training/pytorch-lightning/SKILL.md) · Orchestra-Research | 训练／验证／测试分工、checkpoint选择与记录 | commit 773a52944ba4 |
| [Multi-Node Slurm — Megatron Bridge](https://docs.nvidia.com/nemo/megatron-bridge/0.7.0/skills/nemo-mbridge-multi-node-slurm/SKILL.html) · NVIDIA | 多rank故障、阶段和后续通信等待的定位 | 0.7.0 |
| [Resiliency — Megatron Bridge](https://docs.nvidia.com/nemo/megatron-bridge/0.7.0/skills/nemo-mbridge-resiliency/SKILL.html) · NVIDIA | 恢复阶段、保存完成和故障边界 | 0.7.0 |
| [Memory Tuning — Megatron Bridge](https://docs.nvidia.com/nemo/megatron-bridge/0.7.0/skills/nemo-mbridge-perf-memory-tuning/SKILL.html) · NVIDIA | 显存来源、混杂因素和错误归因更正 | 0.7.0 |
| [Saving and Loading Models — PyTorch Tutorials 2.15.0+cu132 documentation](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) · PyTorch | 模型与训练状态保存、加载和推理模式 | 2026-11-12 检索 |
| [Automatic Mixed Precision — PyTorch Tutorials 2.15.0+cu132 documentation](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html) · PyTorch | 使用中的scaler保存／恢复及AMP行为 | 2026-11-12 检索 |
| [Stateful DataLoader Tutorial — TorchData main documentation](https://meta-pytorch.org/data/main/stateful_dataloader_tutorial.html) · PyTorch / TorchData | 数据加载状态与可恢复位置 | 2026-11-12 检索 |
| [Reinforcement Learning Tips and Tricks — Stable Baselines3 2.9.2 documentation](https://stable-baselines3.readthedocs.io/en/v2.9.2/guide/rl_tips.html) · Stable Baselines3 | 独立评估环境、wrapper、归一化和重复运行 | 2.9.2 |
| [12. Common pitfalls and recommended practices — scikit-learn 1.9.1 documentation](https://scikit-learn.org/1.9/common_pitfalls.html) · scikit-learn | 折内预处理、数据泄漏与可复现性 | 1.9.1 |
| [Nested versus non-nested cross-validation — scikit-learn 1.9.1 documentation](https://scikit-learn.org/1.9/auto_examples/model_selection/plot_nested_cross_validation_iris.html) · scikit-learn | 选模与外层评估分离 | 1.9.1 |
| [GRPO Trainer · Hugging Face](https://huggingface.co/docs/trl/v1.17.1/en/grpo_trainer) · Hugging Face / TRL | 实际GRPO目标、奖励、指标和实现参数 | v1.17.1 |
| [Slurm Workload Manager - Job Exit Codes](https://slurm.schedmd.com/job_exit_code.html) · SchedMD / Slurm | 任务／步骤退出状态和终止信号 | 2026-11-12 检索 |
| [Checkpointing — Megatron Bridge](https://docs.nvidia.com/nemo/megatron-bridge/0.7.0/training/checkpointing.html) · NVIDIA | 对应NeMo版本的保存、加载及恢复语义 | 0.7.0 |

## 按场景查补充资料

| 场景 | 上游原文 |
| --- | --- |
| 文献与假设 | [脑暴方法](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/references/brainstorming_methods.md) |
| 文献与假设 | [候选评估](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-brainstorming/references/idea_evaluation.md) |
| 文献与假设 | [检索与引用](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/literature-review/references/search_and_citation.md) |
| 文献与假设 | [跨领域机制检索](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/references/retrieval.md) |
| 文献与假设 | [论文证据笔记](https://github.com/Hopotta/grounded-research-ideation/blob/7670b2509044253809458cdf0cc34f2d985e4538/references/paper-notes.md) |
| 实验设计与方向决策 | [因果推断与主张](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/hypothesis-generation/references/causal_inference_and_claims.md) |
| 实验设计与方向决策 | [实验设计模式](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/hypothesis-generation/references/experimental_design_patterns.md) |
| 实验设计与方向决策 | [研究方案设计](https://github.com/EvoScientist/EvoSkills/blob/4889c2270af5f9a7658bb6a6709bf37040902006/skills/research-ideation/references/solution-design.md) |
| 评估与 SOTA | [统计陷阱](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/scientific-critical-thinking/references/statistical_pitfalls.md) |

上游作品沿用各自的许可。本仓库分发自写方法与来源链接。需要离线存档时逐项核对上游许可、版本和署名要求。
