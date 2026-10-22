#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""备份考研高数学习数据。

用法：
    python backup_data.py                 # 备份到 data/backup/YYYY-MM-DD/
    python backup_data.py --dest D:/某处   # 额外备份一份到异地目录

行为：
    - 只复制 4 个必需数据文件，不删除、不改写原文件
    - 同名快照已存在时直接覆盖当天快照（当天重复执行为幂等）
    - 打印每个文件的字符数，便于肉眼确认快照完整
    - 必需文件不全时打印 BACKUP_INCOMPLETE 并以非零码退出，
      使自动化调用不会把不完整快照当成成功

退出码：
    0  完整备份成功（若指定 --dest，本地与异地均成功）
    1  找不到数据目录 DATA_DIR
    2  必需文件全部缺失，快照为空
    3  必需文件部分缺失，快照不完整
    4  目标目录不可用（无法创建或不可写）
"""

import argparse
import datetime
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"

FILES = ["学习进度.md", "错题档案.md", "每日学习记录.md", "讲义索引.md"]

# 退出码
EXIT_OK = 0
EXIT_NO_DATA_DIR = 1
EXIT_EMPTY = 2
EXIT_INCOMPLETE = 3
EXIT_DEST_UNUSABLE = 4


def snapshot(target_dir, label):
    """把必需文件复制到 target_dir。

    返回 (字符总数, 缺失文件名列表, 错误信息或 None)。
    """
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return 0, [], "无法创建%s目录 %s（%s）" % (label, target_dir, e.strerror or e)
    if not target_dir.is_dir():
        return 0, [], "%s路径不是目录：%s" % (label, target_dir)

    total = 0
    missing = []
    for name in FILES:
        src = DATA_DIR / name
        if not src.exists():
            missing.append(name)
            print("  缺失：%s（跳过）" % name)
            continue
        dst = target_dir / name
        try:
            shutil.copy2(str(src), str(dst))
            chars = len(dst.read_text(encoding="utf-8"))
        except OSError as e:
            return total, missing, "写入%s失败：%s（%s）" % (label, dst, e.strerror or e)
        total += chars
        print("  %-16s %6d 字符" % (name, chars))
    return total, missing, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=None, help="异地备份根目录（可选）")
    ap.add_argument("--today", default=None, help="覆盖日期 YYYY-MM-DD，默认取系统时间")
    args = ap.parse_args()

    if not DATA_DIR.is_dir():
        print("BACKUP_FAILED: 找不到数据目录 %s" % DATA_DIR)
        print("备份失败：请检查 data/ 是否存在，或先按文档初始化")
        return EXIT_NO_DATA_DIR

    today = args.today or datetime.date.today().isoformat()

    print("[本地快照] %s" % (DATA_DIR / "backup" / today))
    n1, missing, err = snapshot(DATA_DIR / "backup" / today, "本地")
    if err:
        print("BACKUP_FAILED: %s" % err)
        return EXIT_DEST_UNUSABLE

    n2 = 0
    if args.dest:
        dest_root = Path(args.dest).expanduser()
        print("[异地快照] %s" % (dest_root / today))
        n2, missing2, err = snapshot(dest_root / today, "异地")
        if err:
            print("BACKUP_FAILED: %s" % err)
            print("本地已写入 %d 字符，异地未完成，异地备份视为失败。" % n1)
            return EXIT_DEST_UNUSABLE
        for m in missing2:
            if m not in missing:
                missing.append(m)

    if missing:
        tag = "BACKUP_INCOMPLETE" if (n1 > 0 or n2 > 0) else "BACKUP_EMPTY"
        print("\n%s: 缺少 %d 个必需文件：%s" % (tag, len(missing), "、".join(missing)))
        print("本地 %d 字符%s" % (n1, "，异地 %d 字符" % n2 if args.dest else ""))
        if n1 == 0 and n2 == 0:
            print("警告：快照为空，请检查数据目录")
            return EXIT_EMPTY
        print("警告：快照不完整，恢复时会缺文件。请补回缺失文件后重跑。")
        return EXIT_INCOMPLETE

    print("\n完成：本地 %d 字符%s" % (n1, "，异地 %d 字符" % n2 if args.dest else ""))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
