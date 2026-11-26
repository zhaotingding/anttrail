# 字段约定

输入表有 `run`、`state`、`elapsed_ms` 三列。小报只收录 `state=done` 的任务。输入耗时以毫秒计，输出以秒计，保留三位小数。比较快慢时使用耗时数值。

复核入口是项目根的 [report.py](../../../../report.py) 和 [runs.csv](../../../../runs.csv)。
