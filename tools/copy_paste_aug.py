"""离线 Copy-Paste 增强: 故障小块 -> 正常背景 -> 存为 fault 类。"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rope_train.copy_paste import augment


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patches", default="patches")
    ap.add_argument("--normal", default="dataset_cls/train/normal")
    ap.add_argument("--out", default="dataset_cls/train/fault")
    ap.add_argument("--count", type=int, default=50)
    a = ap.parse_args()
    n = augment(a.patches, a.normal, a.out, a.count)
    print(f"生成 {n} 张合成故障样本 -> {a.out}")


if __name__ == "__main__":
    main()
