#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""due_review.py — 只读脚本：输出到期复习、已学待验/待复习、需回炉清单与最近学习块。

设计约束：
- 只依赖 Python 标准库（3.8+）；
- 严格只读，不创建/修改/删除任何文件；
- 任何异常都降级为一行 DUE_REVIEW_FAILED: <原因> 并以退出码 0 结束，
  由调用方改用 Read 直接读文件，流程不中断。

用法：
    python due_review.py [--data-dir DIR] [--today YYYY-MM-DD]
"""

import os
import re
import sys
import argparse
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DEFAULT_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)

STATUS_PENDING = ("已学待验", "待复习", "复习中")


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return strip_comments(f.read())


def strip_comments(text):
    """移除 HTML 注释块，避免把模板示例当成真实记录。"""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def split_row(line):
    """把 markdown 表格行拆成单元格列表。"""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_table_line(line):
    return line.strip().startswith("|")


def is_separator(cells):
    return all(set(c) <= set("-: ") and c != "" for c in cells)


def parse_tables(text):
    """解析文档中所有 markdown 表格，返回 [{header: [...], rows: [[...]]}]。"""
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if not is_table_line(lines[i]):
            i += 1
            continue
        header = split_row(lines[i])
        rows = []
        i += 1
        if i < len(lines) and is_table_line(lines[i]) and is_separator(split_row(lines[i])):
            i += 1
        while i < len(lines) and is_table_line(lines[i]):
            cells = split_row(lines[i])
            if not is_separator(cells):
                rows.append(cells)
            i += 1
        tables.append({"header": header, "rows": rows})
    return tables


def find_table(tables, must_have, must_not_have=()):
    for t in tables:
        h = t["header"]
        if all(k in h for k in must_have) and not any(k in h for k in must_not_have):
            return t
    return None


def cell(row, header, name, default="-"):
    try:
        idx = header.index(name)
    except ValueError:
        return default
    if idx >= len(row):
        return default
    v = row[idx].strip()
    return v if v else default


def parse_date(s):
    s = (s or "").strip()
    if not s or s == "-":
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def snapshot_block(text):
    """取 ## 状态快照 段内的 - key：value 行。"""
    out = {}
    inside = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## "):
            inside = "状态快照" in s
            continue
        if inside and s.startswith("- "):
            body = s[2:]
            for sep in ("：", ":"):
                if sep in body:
                    k, v = body.split(sep, 1)
                    out[k.strip()] = v.strip()
                    break
    return out


REQUIRED_SNAPSHOT_KEYS = [
    "考试类别", "备考阶段", "当前章节", "当前知识点", "当前讲次",
    "当前梯度", "最近学习日期", "待复测", "未完成任务", "数据版本",
]


def last_day_heading(text):
    last = None
    for line in text.splitlines():
        if line.startswith("## ") and "状态快照" not in line:
            last = line[3:].strip()
    return last


def learning_blocks(text, limit=3):
    """返回最后 limit 个学习块：标题 + 关键 bullet。"""
    blocks = []
    cur = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## "):
            if cur is not None:
                blocks.append(cur)
            cur = {"title": s[3:].strip(), "fields": {}}
            continue
        if cur is not None and s.startswith("- "):
            body = s[2:]
            for sep in ("：", ":"):
                if sep in body:
                    k, v = body.split(sep, 1)
                    cur["fields"][k.strip()] = v.strip()
                    break
    if cur is not None:
        blocks.append(cur)
    return blocks[-limit:]


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
    ap.add_argument("--today", default=None)
    args = ap.parse_args()

    today = parse_date(args.today) if args.today else datetime.date.today()
    if today is None:
        print("DUE_REVIEW_FAILED: --today 无法解析为日期")
        return

    data_dir = args.data_dir
    p_prog = os.path.join(data_dir, "学习进度.md")
    p_err = os.path.join(data_dir, "错题档案.md")
    p_day = os.path.join(data_dir, "每日学习记录.md")

    missing = [p for p in (p_prog, p_err) if not os.path.isfile(p)]
    if missing:
        print("DUE_REVIEW_FAILED: 缺少文件 " + "、".join(os.path.basename(m) for m in missing))
        return

    prog_text = read_text(p_prog)
    snap = snapshot_block(prog_text)
    missing_keys = [k for k in REQUIRED_SNAPSHOT_KEYS if k not in snap]

    # 台账
    prog_tables = parse_tables(prog_text)
    ledger = find_table(prog_tables, must_have=("ID", "next_review"))
    due, pending, rework = [], [], []
    if ledger is not None:
        h = ledger["header"]
        for row in ledger["rows"]:
            kid = cell(row, h, "ID")
            if kid == "-":
                continue
            status = cell(row, h, "状态")
            d = parse_date(cell(row, h, "next_review"))
            label = "%s(%s D=%s B=%s)" % (
                kid, cell(row, h, "知识点"), cell(row, h, "D"), cell(row, h, "B"))
            if d is not None:
                delta = (d - today).days
                if delta <= 0:
                    due.append("%s 逾期%d天 状态=%s" % (label, -delta, status))
            if status in STATUS_PENDING:
                pending.append(label + " 状态=" + status)
            elif status == "需回炉":
                rework.append(label)

    # 错题
    err_tables = parse_tables(read_text(p_err))
    err = find_table(err_tables, must_have=("ID", "next_review"))
    if err is not None:
        h = err["header"]
        for row in err["rows"]:
            eid = cell(row, h, "ID")
            if eid == "-":
                continue
            status = cell(row, h, "状态")
            if status in ("已归档",):
                continue
            d = parse_date(cell(row, h, "next_review"))
            if d is None:
                continue
            delta = (d - today).days
            if delta <= 0:
                due.append("%s %s 逾期%d天 类型=%s 状态=%s" % (
                    eid, cell(row, h, "知识点ID"), -delta,
                    cell(row, h, "错误类型"), status))

    last_day = "-"
    blocks = []
    if os.path.isfile(p_day):
        day_text = read_text(p_day)
        last_day = last_day_heading(day_text) or "-"
        blocks = learning_blocks(day_text, limit=3)

    print("TODAY=%s" % today.isoformat())
    print("DATA_DIR=%s" % data_dir)
    print("[到期复习] 共 %d 项" % len(due))
    for x in due:
        print("  - " + x)
    if not due:
        print("  - 无")
    print("[已学待验·待复习] 共 %d 项" % len(pending))
    for x in pending:
        print("  - " + x)
    print("[需回炉] 共 %d 项" % len(rework))
    for x in rework:
        print("  - " + x)
    print("统计 到期=%d 待验或待复习=%d 回炉=%d" % (len(due), len(pending), len(rework)))
    if missing_keys:
        print("SNAPSHOT_INCOMPLETE: 缺 " + "、".join(missing_keys))
    else:
        print("SNAPSHOT=OK 当前=%s 梯度=%s 最近=%s" % (
            snap.get("当前知识点", "-"), snap.get("当前梯度", "-"),
            snap.get("最近学习日期", "-")))
    print("LAST_DAY=%s" % last_day)
    print("[最近学习块] 共 %d 个" % len(blocks))
    for b in blocks:
        f = b["fields"]
        print("  * %s" % b["title"])
        print("    可用/实际=%s 计时来源=%s" % (
            f.get("可用/实际", "未记录"), f.get("计时来源", "未记录")))
        print("    未完成=%s 原因=%s" % (
            f.get("未完成", "未记录"), f.get("未完成原因", "未记录")))



if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # 任何异常都降级，不中断调用方流程
        print("DUE_REVIEW_FAILED: %s: %s" % (type(e).__name__, e))
    sys.exit(0)
