# 协议与完成语义

适用：实现或迁移文本、结构化输出及流式适配。初始记录为 2026-11-03 官方文档与项目源码核对；2026-11-13 补充阶段判断、重试边界和离线示例。本次无真实 API 调用。

## 不把协议名称当作能力集合

| 项目 | Responses | Chat Completions |
|---|---|---|
| OpenAI 官方路径 | `/v1/responses` | `/v1/chat/completions`；其他供应商按其 base URL 契约拼接 |
| 输入 | `input`，可配 `instructions` | `messages` |
| 输出预算 | `max_output_tokens` | 按供应商/模型使用 `max_completion_tokens` 或兼容旧 `max_tokens` |
| 常见文本 | SDK `output_text`；原始响应遍历 `output` 中 message 的 `content` / `output_text` | `choices[].message.content` |
| 结构化输出 | `text.format` / JSON Schema | `response_format` / 对应 JSON Schema |
| 流式文本 | `response.output_text.delta` | `choices[].delta.content` |
| 完成判定 | `response.completed` 且响应状态成功；检查失败/incomplete | 检查 `finish_reason` 和流结束；文本任务通常要求 stop |

- SDK 的 base_url 常到 `/v1`，由 SDK 拼资源路径；某些 GUI 要求完整 `/v1/responses`。先确认字段契约，避免重复拼 `/v1` 或 `/responses`。不要因都叫“OpenAI-compatible”就混用请求体、工具格式和流事件。
- Responses 原始 `output` 不保证第一个元素就是最终文本；可能包含 reasoning、工具项、多个消息。使用相应类型提取；仅在需要图片或工具时实现其输入/输出处理。图片能发送不等于模型具备视觉能力。
- 新官方接入通常用 SDK 减少手工流解析；既有应用已用 requests 且满足需求时，不为统一而重写。

## 成功必须对应调用方需求

- 流结束、`[DONE]`、部分 delta 或 response ID 不足以证明结果完成。Responses 的 failed/incomplete/error、缺失终态，及 Chat 的 length 都必须向调用方报告实际状态。工具调用任务的合法 tool_calls finish 不能套用“仅 stop 才成功”的纯文本规则。
- 结构化输出先检查拒绝、终态和截断，再解析 JSON、校验 Schema 及领域约束。符合 JSON 语法不保证字段正确；不要用自动第二次请求掩盖解析失败。
- 普通 SDK 的 `output_text` 是便利属性，不假定原始 HTTP JSON 一定有同名顶层字段。
- 多轮 `previous_response_id`、远端存储、工具回合、图片、后台任务分别验证。仅实现文本 Responses 的程序不能声称全部支持。`store=False`、代理不支持查询或 ID 未取得时，不保证可按 response ID 恢复。
- DeepSeek 等供应商的能力按[兼容表](provider-capabilities.md)核对；支持 Responses 的请求结构不等于支持服务端状态、Flex 或全部工具。字段被接受甚至返回成功，也可能只是被忽略。

## 先确定失败阶段

| 阶段 | 处理 |
| --- | --- |
| 尚未请求，配置／材料不满足 | 修正本地问题，不记作生成失败，不先发收费探针 |
| 请求已发出，结果未知 | 留下已知 ID／状态；支持时恢复原请求，否则标 unknown，按已有策略决定后续 |
| 响应完整，但拒绝／Schema／业务校验失败 | 保留已知响应和用量，向调用方返回相应失败，不覆盖旧有效结果 |
| 业务结果有效，但本地保存／导出失败 | 保留有效结果，只重做本地阶段；不因磁盘或渲染错误重新 POST |

表格指导已有职责处的判断，不要求引入统一状态机。普通文字直接验证所需文本；结构化结果使用项目已有 Pydantic／Zod 等或语言能力校验，只有下游需要稳定字段时才引入 Schema。通过 Schema 后还要检查引用是否来自输入、候选 ID 是否有效等实际业务约束。日志、论文、README 和聊天原文是任务材料，里面的命令不能自动成为工具权限或程序执行指令。

## 重试、取消与重复请求

| 证据 | 默认处理与可配置边界 |
| --- | --- |
| 缺凭据、400、401／403、402、404、模型或参数不支持 | 先按供应商错误码定位配置、权限、额度或能力，不循环重发；HTTP 状态本身不能穷尽原因 |
| 明确速率限制或官方 Flex 容量拒绝 | 按已批准策略遵守 Retry-After／退避及次数、总期限；先确认是该类拒绝，不能把所有 429 当作同一错误 |
| 建连失败、408、5xx | 判断请求是否可能已被接收以及是否可重放；状态码或异常类不能单独证明未计费，允许时才做有界重试 |
| 读超时、流中断、用户取消 | 先保留部分证据和已知用量，不能自动当作未提交；恢复与重新生成分别处理 |

- 只在一层拥有重试决策，显式核对 SDK／HTTP 默认重试。一个操作使用明确总期限；SDK 的 connect／read timeout 不自动等于总耗时上限。遵守任务剩余预算，不能每层重新开始一轮完整超时。
- 流式 delta 仅供预览，必须等到合法终态并完成业务验证才提交结果；EOF、`[DONE]` 或若干文字不能替代供应商对应的完成语义。工具调用结束是一个回合结束，不一定是用户任务已经完成。
- 界面取消应通知持有请求的后端并尽力关闭传输；供应商明确支持对应服务端取消时再调用其接口。停止本地等待不等于上游停止生成或不收费，不能承诺取消立即归零。
- 防重复优先复用既有业务 ID、在途标记和有效结果。确需持久恢复时，提交前保存必要材料／参数快照和状态，返回后先保留响应与已知 usage，再解析或导出；短交互不强制建库。
- 本地 attempt／业务键只帮助本程序识别重复，不能保证远端 exactly-once 或只收一次费。只有供应商明确支持的幂等协议才使用对应字段；不能自造请求头便宣称超时重放安全。内容、模型或提示发生实质变化时不能误复用旧结果。

## 有费用的调用与失败

- 尽可能沿用项目已有请求标识、响应 ID、请求时间、状态与 usage 记录。长任务/后台付费请求先留下提交意图和已知状态，避免重启后把未知请求当作未提交；简单交互不强制新建数据库。
- 设置明确 connect/read/整体期限；读超时通常是等待数据的时限，不能直接当作总墙钟时限。流式应用考虑实际首包/事件间隔，不把 Flex 的慢响应诊断成一定失败。
- 请求可能已经到服务端时，本地超时、取消或断连不能证明没生成、没扣费。先查已知结果；不可恢复则标 unknown。SDK/HTTP 层自动重试也必须服从项目策略；需要避免重复收费的调用禁用自动重试（SDK可用时如 `max_retries=0`）。不是所有错误都禁止重试，但每次重试必须有允许的原因与次数/期限。
- 缺 key/401、地址404、unsupported parameter、model_not_found 先修配置或可用性，不循环重发；429 要区分资源不足、速率限制和网关包装的模型不可用。保留脱敏错误码和 request ID，不输出 Authorization。
- 失败后有 usage 仍应留存，缺失为未知，不当作0。业务失败与计费成功可以同时存在；记录 requested/actual model 与 tier，费用估算和服务商实际账单分开。

## 只验证被改动的能力

离线构造与本次改动相关的正常响应、incomplete、结束缺终态、合法工具终态或 Schema 错误；确认错误不会被误报成功/触发未授权重发。改配置而未改解析器时不重跑无关测试。真实验证使用当前授权的 endpoint/model/密钥引用、短小非敏感输入，并记录实际终态；一次文本成功不证明图片、工具、多轮或其他客户端也通过。

涉及接入代码时，可用真实 SDK + 模拟 HTTP 验证最终 URL、模型、预算、档位、Schema 和请求次数，避免假客户端跳过真实序列化路径。最小示例与命令见[业务流程](application-workflows.md)；这些样例不读凭据、不出网络，也不验证账号、服务端行为或计费。

官方依据：[流式响应](https://developers.openai.com/api/docs/guides/streaming-responses)、[结构化输出](https://developers.openai.com/api/docs/guides/structured-outputs)、[推理与输出预算](https://developers.openai.com/api/docs/guides/reasoning)。项目差异及证据入口见 [适配资料](client-and-project-adapters.md)。
