# 供应商能力与配置差异

读取时机：新增／切换供应商或模型、选择协议，或需要确认 Schema、图片、工具、Flex、服务端状态与恢复。2026-11-13 核对下列官方资料；属于文档能力记录，未验证账号权限、真实调用或费用。

## 按实际能力构造请求

能力归属于“供应商 + endpoint + 模型 + API／SDK 版本”，不归属于一个显示名称。只核对本次需要的能力，保留已知有效实现，不为增加供应商而重写现有程序或新建通用网关。

| 对象 | 已有依据 | 对应用的影响 |
| --- | --- | --- |
| OpenAI 官方 | 新项目推荐 Responses；Flex 按模型和账号条件使用 | 个人新接入优先 Responses + 可用 Flex；已有明确协议和任务延迟要求优先 |
| DeepSeek 官方 | 已提供 Responses 和 Chat 接口；Responses 是部分能力兼容 | 不能固定认定“仅支持 Chat”，也不能将 OpenAI 全部参数直接透传 |
| 兼容网关或其他供应商 | 请求格式相似不足以证明后端能力 | 分别核对实际模型映射、服务等级、返回事件、usage 和恢复；模型名含 GPT 不证明走官方服务 |

## OpenAI 官方

- 新项目按[Responses 迁移说明](https://developers.openai.com/api/docs/guides/migrate-to-responses)选型；Chat Completions 仍有既有用途，不自动迁移有效客户端。
- `service_tier="flex"` 是请求参数，不是模型名后缀。模型支持、实际采用档位和最终账单分别确认；[Flex](https://developers.openai.com/api/docs/guides/flex-processing)的明确容量拒绝与提交后断线采用不同处理。
- 文本 Schema、工具函数、图片和流式分别验证。结构化输出的拒绝、截断和领域一致性检查见[协议参考](protocols-and-completion.md)，不能只检查 JSON 能否解析。
- 服务端存储、按 ID 查询、多轮关联及后台取消按[Responses](https://developers.openai.com/api/reference/resources/responses/methods/create)与[后台模式](https://developers.openai.com/api/docs/guides/background)实际契约确认。`store=False` 或无可查询 ID 的请求不能套用 GET 恢复；本地取消传输不证明服务端停止计费。

## DeepSeek 官方 Responses

依据：[DeepSeek Responses 兼容表](https://api-docs.deepseek.com/guides/responses_api/)，核对日期 2026-11-13。SDK 示例的 base URL 是 `https://api.deepseek.com`；具体路径由 SDK 按其契约拼接。

| 能力 | 该文档当前记录 | 实现要求 |
| --- | --- | --- |
| input／instructions／stream／max_output_tokens | 支持 | 使用 Responses 请求与事件格式；不是更换 Chat URL 后仍发送 messages |
| 流结束 | completed／incomplete／failed，无 `[DONE]` | 文字 delta 不是最终结果，处理对应终态 |
| text.format、reasoning.effort | 文档列为支持；其他同组字段可能无效 | 按模型核对 Schema 与推理参数；不要把参数接受等同语义生效 |
| service_tier | 不支持 | 不向它套用 OpenAI Flex 参数或价格 |
| previous_response_id／conversation／store／background | 不支持；响应 store 固定 false | 对话历史和必要恢复证据由应用管理，不假定服务端保存／后台查询 |
| 工具与图片 | 按模型、类型部分支持 | 逐项核对实际需要的工具和输入，不把所有 OpenAI 内置工具视为可用 |

官方表指出不支持的参数可能被静默忽略。因此成功响应不能证明每个发送字段都有效；请求构造应主动省略已知不支持字段。特别是 `developer` message 的处理与官方 OpenAI 不完全相同，不能仅凭角色字段名称推断相同语义。

既有 Chat 接入可继续使用其协议。DeepSeek [JSON Output](https://api-docs.deepseek.com/guides/json_mode/)的 `json_object` 要求与严格 Schema 区分；其文档提示即使 finish_reason 为 stop，content 也可能只有空白，程序仍要验证有效业务结果。工具回合参照[Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)，不混用思考字段。

## 记录与更新方式

对选定档案保留已确认的 provider、端点、协议、模型、必需能力、限制、来源和核对日期；未知标未知，不为填表测试所有组合。凭据引用放在受控配置里，不写密钥。

模型 ID、别名指向与退役时间按供应商官方模型页和弃用公告核对，示例名称不承诺长期有效。模型失效时说明受影响能力和可选迁移，不静默替换模型、改变费用或丢弃原任务状态；迁移按已有授权范围执行。

新增模型、切换供应商、升级影响请求的 SDK 或出现参数拒绝／异常忽略时复核对应文档及实际请求。价格与容量按当时模型页核对；历史客户端快照见[项目适配](client-and-project-adapters.md)，不把旧 UI 数字当模型规格。稳定流程按本地参考执行，不要求每次普通调用重读全部外网资料。
