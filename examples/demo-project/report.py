# SPDX-License-Identifier: MIT
# Copyright (c) 2026 zhaotingding
"""从示例 CSV 打印已完成任务及其用时。仅使用 Python 标准库。"""
import csv
from pathlib import Path


def completed_runs(path):
    with path.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            if row["state"] == "done":
                yield row["run"], int(row["elapsed_ms"])


if __name__ == "__main__":
    sample = Path(__file__).with_name("runs.csv")
    for name, milliseconds in completed_runs(sample):
        print(f"{name}: {milliseconds / 1000:.3f} s")
