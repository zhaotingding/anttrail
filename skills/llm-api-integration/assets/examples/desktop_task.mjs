// SPDX-License-Identifier: MIT
// Copyright (c) 2026 zhaotingding
// 离线桌面业务示例：无网络、无凭据、无 Electron 依赖。
// generate 是现有后端调用并负责保留必要响应/用量，validate 校验，apply 写回。
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';

export async function runTask({ generate, validate, apply, publish, signal }) {
  if (signal.aborted) return { state: 'cancelled', remoteState: 'not_submitted' };
  let stage = 'request';
  let value;
  try {
    publish({ state: 'waiting' });
    const response = await generate({
      signal,
      onDelta: text => { if (!signal.aborted) publish({ state: 'preview', text }); },
    });
    // 取消已发出后不再写回，但不能据此推断服务端取消或免计费。
    if (signal.aborted) {
      publish({ state: 'cancelled' });
      return { state: 'cancelled', response };
    }
    stage = 'validation';
    value = validate(response);
    stage = 'apply';
    await apply(value);
    publish({ state: 'ready' });
    return { state: 'completed', value };
  } catch (error) {
    const state = stage === 'apply' ? 'delivery_failed' :
      stage === 'request' && signal.aborted ? 'cancelled' : 'failed';
    publish({ state, stage });
    // 写回失败保留已验证的 value，调用方可以只重试 apply(value)。
    return { state, stage, value, error };
  }
}

async function check(caseName) {
  const controller = new AbortController();
  const events = [];
  let requests = 0;
  let writes = 0;
  let saved = '原有有效结果';
  if (caseName === 'cancel_before') controller.abort();
  const result = await runTask({
    signal: controller.signal,
    publish: event => events.push(event),
    generate: async ({ signal, onDelta }) => {
      requests += 1;
      onDelta('正在生成的预览');
      assert.equal(saved, '原有有效结果');
      if (caseName === 'cancel_during') {
        controller.abort();
        assert.equal(signal.aborted, true);
      }
      return { status: caseName === 'incomplete' ? 'incomplete' : 'completed', text: '新结果' };
    },
    validate: response => {
      if (response.status !== 'completed' || !response.text.trim()) throw new Error('结果未通过验证');
      return response.text;
    },
    apply: async value => {
      if (caseName === 'export_failed') throw new Error('模拟导出失败');
      saved = value;
      writes += 1;
    },
  });
  if (caseName === 'success') {
    assert.equal(result.state, 'completed');
    assert.equal(saved, '新结果');
    assert.equal(writes, 1);
    assert.deepEqual(events.map(event => event.state), ['waiting', 'preview', 'ready']);
  } else if (caseName === 'export_failed') {
    assert.equal(result.state, 'delivery_failed');
    assert.equal(saved, '原有有效结果');
    assert.equal(result.value, '新结果');
    saved = result.value; // 已有结果本地重写，不再请求模型。
    assert.equal(requests, 1);
  } else {
    assert.equal(result.state, caseName === 'incomplete' ? 'failed' : 'cancelled');
    assert.equal(saved, '原有有效结果');
    assert.equal(writes, 0);
  }
  assert.equal(requests, caseName === 'cancel_before' ? 0 : 1);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const cases = ['success', 'incomplete', 'export_failed', 'cancel_before', 'cancel_during'];
  for (const name of cases) await check(name);
  console.log(JSON.stringify({ offlineCases: cases.length, passed: true, network: 'none', credentialAccess: 'none' }));
}
