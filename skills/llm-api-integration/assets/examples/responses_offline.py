# SPDX-License-Identifier: MIT
# Copyright (c) 2026 zhaotingding
"""纯离线示例：真实 SDK + MockTransport，不读取实际凭据或发起网络请求。

依赖 openai、httpx、pydantic；在已具备依赖的项目环境运行。
本示例运行不联网；首次安装依赖可能需要联网，不会由本脚本自动安装。
已验证版本及运行命令见 references/application-workflows.md。

演示字段不是生产默认值。接入项目时复用其凭据读取、日志和存储职责，
不要将此文件的内存列表、虚构模型或测试环境隔离照搬成通用框架。
"""

import json
from unittest.mock import patch

# 隔离 SDK 的环境默认项；不枚举或复制实际环境变量。
with patch("os.environ", {}):
    import httpx
    from openai import APITimeoutError, OpenAI, RateLimitError
    from pydantic import BaseModel, ConfigDict, ValidationError


class Summary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str
    source_ids: list[str]


MATERIAL = [{"id": "m1", "text": "离线示例：先验证结果，再写入笔记。"}]
PROFILES = {
    "openai": {"base_url": "https://openai.example.invalid/v1", "path": "/v1/responses"},
    "deepseek": {"base_url": "https://deepseek.example.invalid", "path": "/responses"},
}


def request_fields(provider):
    """同一业务契约，按供应商添加实际支持的参数。"""
    request = {
        "model": "offline-example-model",
        "input": "只根据材料生成摘要和来源 ID：" + json.dumps(MATERIAL, ensure_ascii=False),
        "max_output_tokens": 256,
        "text": {"format": {"type": "json_schema", "name": "summary", "strict": True,
                            "schema": Summary.model_json_schema()}},
    }
    if provider == "openai":
        request.update(service_tier="flex", store=False)
    # DeepSeek 不透传 Flex、store、background 或 previous_response_id。
    return request


def remember_response(response, received):
    received.append({"id": response.id, "status": response.status,
                     "usage": response.usage.model_dump() if response.usage else None,
                     "raw": response.model_dump()})


def accept_response(response, received):
    """先保留响应证据，再验证结果；写回由调用者负责。"""
    remember_response(response, received)
    if response.status != "completed":
        raise ValueError("响应未完成：" + str(response.status))
    for item in response.output:
        if item.type == "message" and any(part.type == "refusal" for part in item.content):
            raise ValueError("模型拒绝了请求")
    parsed = Summary.model_validate_json(response.output_text)
    allowed_ids = {item["id"] for item in MATERIAL}
    if not parsed.summary.strip() or not parsed.source_ids or not set(parsed.source_ids) <= allowed_ids:
        raise ValueError("摘要为空或来源不属于本次材料")
    return parsed


def generate_summary(client, provider, received):
    return accept_response(client.responses.create(**request_fields(provider)), received)


def stream_summary(client, provider, received, previews):
    with client.responses.create(**request_fields(provider), stream=True) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                previews.append(event.delta)  # 只用于预览，不用部分文本完成业务写回。
            elif event.type in {"response.created", "response.in_progress"}:
                remember_response(event.response, received)
            elif event.type in {"response.completed", "response.incomplete", "response.failed"}:
                # 收到终态立即保留并判定，不再依赖连接 EOF。
                return accept_response(event.response, received)
            elif event.type == "error":
                raise ValueError("流返回错误事件")
    raise ValueError("流结束但缺少完成状态")


def fixture(case, provider):
    content = {"summary": "验证后再保存笔记。", "source_ids": ["m1"]}
    if case == "bad_schema":
        content.pop("summary")
    elif case == "bad_source":
        content["source_ids"] = ["unknown-source"]
    elif case == "blank":
        content["summary"] = "  "
    part = {"type": "output_text", "text": json.dumps(content), "annotations": []}
    if case == "refusal":
        part = {"type": "refusal", "refusal": "示例拒绝"}
    payload = {
        "id": "resp_offline", "object": "response", "created_at": 0,
        "model": "offline-example-model", "status": "completed", "error": None,
        "incomplete_details": None,
        "output": [{"id": "msg_offline", "type": "message", "status": "completed",
                    "role": "assistant", "content": [part]}],
        "usage": {"input_tokens": 20, "output_tokens": 10, "total_tokens": 30,
                  "input_tokens_details": {"cached_tokens": 0},
                  "output_tokens_details": {"reasoning_tokens": 0}},
        "service_tier": "flex" if provider == "openai" else None,
    }
    if case == "incomplete":
        payload.update(status="incomplete", incomplete_details={"reason": "max_output_tokens"})
    elif case == "failed":
        payload.update(status="failed", error={"code": "server_error", "message": "offline failure"})
    elif case == "missing_usage":
        payload["usage"] = None
    return payload


def exercise(provider, case):
    requests, received = [], []

    def handle(request):
        # 观察真实 SDK 最终构造的路径和字段，不打印鉴权头。
        body = json.loads(request.content)
        requests.append(body)
        assert request.method == "POST" and request.url.path == PROFILES[provider]["path"]
        assert request.url.host.endswith(".example.invalid")
        assert body["max_output_tokens"] == 256 and "messages" not in body
        assert body["text"]["format"]["schema"]["additionalProperties"] is False
        if provider == "openai":
            assert body["service_tier"] == "flex" and body["store"] is False
        else:
            assert not {"service_tier", "store", "background", "previous_response_id"} & body.keys()
        if case == "timeout":
            raise httpx.ReadTimeout("offline unknown response", request=request)
        if case == "rate_limit":
            return httpx.Response(429, headers={"retry-after": "2"},
                                  json={"error": {"message": "offline limit", "type": "rate_limit_error", "code": "rate_limit_exceeded"}})
        return httpx.Response(200, json=fixture(case, provider))

    expected_errors = {"incomplete": ValueError, "failed": ValueError, "refusal": ValueError,
                       "bad_schema": ValidationError, "bad_source": ValueError, "blank": ValueError,
                       "timeout": APITimeoutError, "rate_limit": RateLimitError}
    # 客户端只拥有 MockTransport；环境项为空，认证值是无效的离线占位值。
    with patch("os.environ", {}):
        with httpx.Client(transport=httpx.MockTransport(handle), trust_env=False) as transport:
            with OpenAI(api_key="offline-not-a-key", base_url=PROFILES[provider]["base_url"],
                        max_retries=0, timeout=2, http_client=transport) as client:
                try:
                    result = generate_summary(client, provider, received)
                except tuple(set(expected_errors.values())) as error:
                    assert case in expected_errors and isinstance(error, expected_errors[case]), (case, type(error))
                else:
                    assert case not in expected_errors and result.source_ids == ["m1"]
    assert len(requests) == 1, "错误不应触发 SDK 隐式重发"
    if case in {"timeout", "rate_limit"}:
        assert not received  # 没有响应对象时，不捏造 usage=0。
    elif case == "missing_usage":
        assert received[0]["usage"] is None
    else:
        assert received[0]["usage"]["total_tokens"] == 30
    return {"provider": provider, "case": case, "post_count": len(requests), "checked": True}


def exercise_stream(case):
    requests, received, previews = [], [], []

    def handle(request):
        body = json.loads(request.content)
        requests.append(body)
        assert body["stream"] is True and body["service_tier"] == "flex"
        delta = {"type": "response.output_text.delta", "sequence_number": 0,
                 "item_id": "msg_offline", "output_index": 0, "content_index": 0,
                 "delta": "仅供预览的部分文本", "logprobs": []}
        initial = fixture("complete", "openai")
        initial.update(status="in_progress", output=[], usage=None)
        created = {"type": "response.created", "sequence_number": 0, "response": initial}
        chunks = ["event: response.created\ndata: " + json.dumps(created) + "\n\n",
                  "event: response.output_text.delta\ndata: " + json.dumps(delta) + "\n\n"]
        if case != "missing_terminal":
            payload = fixture(case, "openai")
            kind = "response." + payload["status"]
            chunks.append("event: " + kind + "\ndata: " + json.dumps({"type": kind, "sequence_number": 1, "response": payload}) + "\n\n")
        class EventStream(httpx.SyncByteStream):
            def __iter__(self):
                for chunk in chunks:
                    yield chunk.encode()
                if case == "terminal_then_error":
                    raise httpx.ReadError("不应在已收到终态后继续读取")
        return httpx.Response(200, headers={"content-type": "text/event-stream"}, stream=EventStream())

    with patch("os.environ", {}):
        with httpx.Client(transport=httpx.MockTransport(handle), trust_env=False) as transport:
            with OpenAI(api_key="offline-not-a-key", base_url=PROFILES["openai"]["base_url"],
                        max_retries=0, timeout=2, http_client=transport) as client:
                try:
                    result = stream_summary(client, "openai", received, previews)
                except ValueError:
                    assert case in {"incomplete", "failed", "missing_terminal"}
                else:
                    assert case in {"complete", "terminal_then_error"} and result.source_ids == ["m1"]
    assert len(requests) == 1 and previews
    if case == "missing_terminal":
        assert len(received) == 1 and received[0]["id"] == "resp_offline"
        assert received[0]["status"] == "in_progress" and received[0]["usage"] is None
    else:
        assert received[-1]["usage"]["total_tokens"] == 30
    return True


if __name__ == "__main__":
    cases = ["complete", "missing_usage", "incomplete", "failed", "refusal",
             "bad_schema", "bad_source", "blank", "timeout", "rate_limit"]
    results = [exercise(provider, case) for provider in PROFILES for case in cases]
    streams = [exercise_stream(case) for case in ["complete", "incomplete", "failed", "missing_terminal", "terminal_then_error"]]
    print(json.dumps({"offline_cases": len(results), "passed": all(row["checked"] for row in results),
                      "stream_cases": len(streams), "stream_passed": all(streams),
                      "network": "MockTransport only", "credential_access": "none"}, ensure_ascii=False))
